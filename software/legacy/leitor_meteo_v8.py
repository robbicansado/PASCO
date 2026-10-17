import serial
import time
import csv
from datetime import datetime
import matplotlib.pyplot as plt
from collections import deque
from statistics import median

# ============================================================
# PASCO - METEO V8
# Filtro de outliers + suavizacao
# ============================================================

PORTA = "COM5"
BAUDRATE = 9600

MAX_PONTOS = 200

# Tamanho da janela para mediana
JANELA_FILTRO = 5

# Salto maximo plausivel entre leituras consecutivas
# acima disso, marcamos como outlier
SALTO_MAXIMO = 1.5

# Parametros da classificacao termica
LIMIAR_ESTADO = 0.08
JANELA_TENDENCIA = 12


# ============================================================
# CONEXAO SERIAL
# ============================================================

ser = serial.Serial(
    PORTA,
    BAUDRATE,
    timeout=0.2
)

time.sleep(2)

print("======================================")
print(" PASCO - METEO V8")
print(" Filtro de outliers + mediana")
print("======================================")
print(f"Porta: {PORTA}")
print(f"Baud rate: {BAUDRATE}")
print("Ctrl+C para encerrar.\n")


# ============================================================
# CSV
# ============================================================

agora = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

nome_arquivo = f"pasco_meteo_v8_{agora}.csv"

arquivo = open(
    nome_arquivo,
    "w",
    newline="",
    encoding="utf-8"
)

writer = csv.writer(arquivo)

writer.writerow([
    "tempo_s",
    "temperatura_bruta_C",
    "temperatura_filtrada_C",
    "delta_T_C",
    "estado",
    "outlier"
])


# ============================================================
# DADOS
# ============================================================

tempos = deque(maxlen=MAX_PONTOS)
temperaturas_filtradas = deque(maxlen=MAX_PONTOS)

janela_filtro = deque(maxlen=JANELA_FILTRO)

inicio = time.time()

temperatura_inicial = None
temperatura_minima = None
temperatura_maxima = None

ultima_temperatura_valida = None


# ============================================================
# GRAFICO
# ============================================================

plt.ion()

fig, ax = plt.subplots(figsize=(11, 6))

linha_grafico, = ax.plot([], [], linewidth=2)

ax.set_title(
    "PASCO - Temperatura em tempo real | METEO V8"
)

ax.set_xlabel("Tempo (s)")
ax.set_ylabel("Temperatura (C)")
ax.grid(True)

painel = ax.text(
    0.02,
    0.97,
    "Aguardando dados...",
    transform=ax.transAxes,
    verticalalignment="top",
    fontsize=11,
    bbox=dict(
        boxstyle="round",
        alpha=0.75
    )
)

plt.show(block=False)


# ============================================================
# ESTADO TERMICO
# ============================================================

def calcular_estado():

    if len(temperaturas_filtradas) < JANELA_TENDENCIA:
        return "ESTABILIZANDO"

    recentes = list(
        temperaturas_filtradas
    )[-JANELA_TENDENCIA:]

    metade = len(recentes) // 2

    media_inicio = (
        sum(recentes[:metade])
        / len(recentes[:metade])
    )

    media_final = (
        sum(recentes[metade:])
        / len(recentes[metade:])
    )

    variacao = media_final - media_inicio

    if variacao > LIMIAR_ESTADO:
        return "AQUECENDO"

    if variacao < -LIMIAR_ESTADO:
        return "RESFRIANDO"

    return "ESTAVEL"


# ============================================================
# AQUISICAO
# ============================================================

try:

    while True:

        plt.pause(0.01)

        linha_serial = (
            ser.readline()
            .decode(errors="ignore")
            .strip()
        )

        if not linha_serial:
            continue

        if "Meteo -> T(C):" not in linha_serial:
            continue

        try:

            temperatura_bruta = float(
                linha_serial
                .split(":")[-1]
                .strip()
            )

        except ValueError:
            continue


        tempo_atual = time.time() - inicio


        # ----------------------------------------------------
        # DETECCAO DE OUTLIER
        # ----------------------------------------------------

        outlier = False

        if ultima_temperatura_valida is not None:

            salto = abs(
                temperatura_bruta
                - ultima_temperatura_valida
            )

            if salto > SALTO_MAXIMO:
                outlier = True


        # ----------------------------------------------------
        # FILTRO
        # ----------------------------------------------------

        if not outlier:

            ultima_temperatura_valida = temperatura_bruta

            janela_filtro.append(
                temperatura_bruta
            )

        if len(janela_filtro) == 0:
            continue

        temperatura_filtrada = median(
            janela_filtro
        )


        # ----------------------------------------------------
        # ESTATISTICAS
        # ----------------------------------------------------

        if temperatura_inicial is None:

            temperatura_inicial = temperatura_filtrada
            temperatura_minima = temperatura_filtrada
            temperatura_maxima = temperatura_filtrada

        temperatura_minima = min(
            temperatura_minima,
            temperatura_filtrada
        )

        temperatura_maxima = max(
            temperatura_maxima,
            temperatura_filtrada
        )

        delta_T = (
            temperatura_filtrada
            - temperatura_inicial
        )


        # ----------------------------------------------------
        # ARMAZENAMENTO
        # ----------------------------------------------------

        tempos.append(tempo_atual)

        temperaturas_filtradas.append(
            temperatura_filtrada
        )

        estado = calcular_estado()


        # ----------------------------------------------------
        # TERMINAL
        # ----------------------------------------------------

        marcador = ""

        if outlier:
            marcador = " | OUTLIER"

        print(
            f"{tempo_atual:7.1f} s | "
            f"bruto: {temperatura_bruta:6.2f} C | "
            f"filtrado: {temperatura_filtrada:6.2f} C | "
            f"dT: {delta_T:+6.2f} C | "
            f"{estado}"
            f"{marcador}"
        )


        # ----------------------------------------------------
        # CSV
        # ----------------------------------------------------

        writer.writerow([
            round(tempo_atual, 3),
            temperatura_bruta,
            temperatura_filtrada,
            round(delta_T, 3),
            estado,
            outlier
        ])

        arquivo.flush()


        # ----------------------------------------------------
        # GRAFICO
        # ----------------------------------------------------

        linha_grafico.set_data(
            list(tempos),
            list(temperaturas_filtradas)
        )

        if len(tempos) >= 2:

            ax.set_xlim(
                min(tempos),
                max(tempos) + 1
            )

            minimo = min(
                temperaturas_filtradas
            )

            maximo = max(
                temperaturas_filtradas
            )

            intervalo = maximo - minimo

            margem = max(
                0.5,
                intervalo * 0.20
            )

            ax.set_ylim(
                minimo - margem,
                maximo + margem
            )


        # ----------------------------------------------------
        # PAINEL
        # ----------------------------------------------------

        texto = (
            f"Temperatura atual:   {temperatura_filtrada:.2f} C\n"
            f"Temperatura inicial: {temperatura_inicial:.2f} C\n"
            f"Minima:              {temperatura_minima:.2f} C\n"
            f"Maxima:              {temperatura_maxima:.2f} C\n"
            f"Delta T:             {delta_T:+.2f} C\n"
            f"Tempo:               {tempo_atual:.1f} s\n\n"
            f"Estado: {estado}"
        )

        if outlier:
            texto += "\nLeitura espuria ignorada"

        painel.set_text(texto)

        fig.canvas.draw_idle()
        fig.canvas.flush_events()


# ============================================================
# ENCERRAMENTO
# ============================================================

except KeyboardInterrupt:

    print("\nAquisicao encerrada.")

finally:

    ser.close()
    arquivo.close()

    print(f"Dados salvos em: {nome_arquivo}")

    plt.ioff()
    plt.show()