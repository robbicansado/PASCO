import serial
import time
import csv
from datetime import datetime
import matplotlib.pyplot as plt
from collections import deque
from statistics import median

# ============================================================
# PASCO - METEO V9
# Mediana movel + deteccao informativa de outliers
# ============================================================

PORTA = "COM5"
BAUDRATE = 9600

MAX_PONTOS = 200

# Janela usada para suavizar a curva
JANELA_FILTRO = 5

# Se a leitura bruta se afastar muito da mediana recente,
# ela sera marcada como suspeita, mas NAO sera descartada.
LIMIAR_OUTLIER = 2.0

# Classificacao de tendencia termica
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
print(" PASCO - METEO V9")
print(" Mediana movel + analise de tendencia")
print("======================================")
print(f"Porta: {PORTA}")
print(f"Baud rate: {BAUDRATE}")
print("Ctrl+C para encerrar.\n")


# ============================================================
# CSV
# ============================================================

agora = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

nome_arquivo = f"pasco_meteo_v9_{agora}.csv"

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
    "outlier_suspeito"
])


# ============================================================
# DADOS
# ============================================================

tempos = deque(maxlen=MAX_PONTOS)

temperaturas_brutas = deque(maxlen=MAX_PONTOS)
temperaturas_filtradas = deque(maxlen=MAX_PONTOS)

janela_filtro = deque(maxlen=JANELA_FILTRO)

inicio = time.time()

temperatura_inicial = None
temperatura_minima = None
temperatura_maxima = None


# ============================================================
# GRAFICO
# ============================================================

plt.ion()

fig, ax = plt.subplots(figsize=(11, 6))

linha_filtrada, = ax.plot(
    [],
    [],
    linewidth=2,
    label="Temperatura filtrada"
)

linha_bruta, = ax.plot(
    [],
    [],
    linewidth=1,
    alpha=0.35,
    label="Temperatura bruta"
)

ax.set_title(
    "PASCO - Temperatura em tempo real | METEO V9"
)

ax.set_xlabel("Tempo (s)")
ax.set_ylabel("Temperatura (C)")
ax.grid(True)
ax.legend(loc="lower right")

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

        # Mantem a janela responsiva
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
        # MEDIANA DE REFERENCIA / OUTLIER
        # ----------------------------------------------------

        outlier = False

        if len(janela_filtro) >= 3:

            mediana_anterior = median(
                janela_filtro
            )

            diferenca = abs(
                temperatura_bruta
                - mediana_anterior
            )

            if diferenca > LIMIAR_OUTLIER:
                outlier = True


        # ----------------------------------------------------
        # FILTRO
        #
        # Diferente da V8, TODAS as leituras entram.
        # Portanto o sistema nunca fica preso numa leitura antiga.
        # ----------------------------------------------------

        janela_filtro.append(
            temperatura_bruta
        )

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

        tempos.append(
            tempo_atual
        )

        temperaturas_brutas.append(
            temperatura_bruta
        )

        temperaturas_filtradas.append(
            temperatura_filtrada
        )

        estado = calcular_estado()


        # ----------------------------------------------------
        # TERMINAL
        # ----------------------------------------------------

        marcador = ""

        if outlier:
            marcador = " | OUTLIER SUSPEITO"

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

        linha_bruta.set_data(
            list(tempos),
            list(temperaturas_brutas)
        )

        linha_filtrada.set_data(
            list(tempos),
            list(temperaturas_filtradas)
        )

        if len(tempos) >= 2:

            ax.set_xlim(
                min(tempos),
                max(tempos) + 1
            )

            todos_valores = (
                list(temperaturas_brutas)
                + list(temperaturas_filtradas)
            )

            minimo = min(
                todos_valores
            )

            maximo = max(
                todos_valores
            )

            intervalo = maximo - minimo

            margem = max(
                0.5,
                intervalo * 0.15
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

            texto += (
                "\n\nLeitura bruta suspeita:"
                f" {temperatura_bruta:.2f} C"
            )

        painel.set_text(
            texto
        )

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