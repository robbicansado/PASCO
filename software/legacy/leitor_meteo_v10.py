import serial
import time
import csv
from datetime import datetime
import matplotlib.pyplot as plt
from collections import deque
from statistics import median

# ============================================================
# PASCO - METEO V10
# Versao final da etapa de temperatura
# ============================================================

PORTA = "COM5"
BAUDRATE = 9600

MAX_PONTOS = 250

# Filtro
JANELA_FILTRO = 5

# Janela aproximada usada para calcular tendencia
JANELA_TENDENCIA = 30

# Taxa abaixo deste valor e considerada estabilidade
# unidade: graus Celsius por minuto
LIMIAR_TAXA = 0.30


# ============================================================
# SERIAL
# ============================================================

ser = serial.Serial(
    PORTA,
    BAUDRATE,
    timeout=0.2
)

time.sleep(2)

print("======================================")
print(" PASCO - METEO V10")
print(" Temperatura + taxa de variacao")
print("======================================")
print(f"Porta: {PORTA}")
print(f"Baud rate: {BAUDRATE}")
print("Ctrl+C para encerrar.\n")


# ============================================================
# CSV
# ============================================================

agora = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

nome_arquivo = f"pasco_meteo_v10_{agora}.csv"

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
    "taxa_C_min",
    "estado"
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
    [], [],
    linewidth=2,
    label="Temperatura filtrada"
)

linha_bruta, = ax.plot(
    [], [],
    linewidth=1,
    alpha=0.30,
    label="Temperatura bruta"
)

ax.set_title(
    "PASCO - Temperatura em tempo real | METEO V10"
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
# CALCULO DA TAXA
# ============================================================

def calcular_taxa():

    if len(temperaturas_filtradas) < JANELA_TENDENCIA:
        return None

    temps = list(temperaturas_filtradas)[
        -JANELA_TENDENCIA:
    ]

    ts = list(tempos)[
        -JANELA_TENDENCIA:
    ]

    metade = len(temps) // 2

    temp_inicio = sum(
        temps[:metade]
    ) / metade

    temp_final = sum(
        temps[metade:]
    ) / (len(temps) - metade)

    tempo_inicio = sum(
        ts[:metade]
    ) / metade

    tempo_final = sum(
        ts[metade:]
    ) / (len(ts) - metade)

    delta_tempo = tempo_final - tempo_inicio

    if delta_tempo <= 0:
        return None

    # C/s
    taxa = (
        temp_final - temp_inicio
    ) / delta_tempo

    # C/min
    return taxa * 60


# ============================================================
# CLASSIFICACAO
# ============================================================

def calcular_estado(taxa):

    if taxa is None:
        return "ESTABILIZANDO"

    if taxa > LIMIAR_TAXA:
        return "AQUECENDO"

    if taxa < -LIMIAR_TAXA:
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
        # FILTRO DE MEDIANA
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

        tempos.append(tempo_atual)
        temperaturas_brutas.append(temperatura_bruta)
        temperaturas_filtradas.append(temperatura_filtrada)


        # ----------------------------------------------------
        # TAXA E ESTADO
        # ----------------------------------------------------

        taxa = calcular_taxa()
        estado = calcular_estado(taxa)


        # ----------------------------------------------------
        # TERMINAL
        # ----------------------------------------------------

        if taxa is None:
            texto_taxa = "---"
        else:
            texto_taxa = f"{taxa:+.2f} C/min"

        print(
            f"{tempo_atual:7.1f} s | "
            f"T: {temperatura_filtrada:6.2f} C | "
            f"dT: {delta_T:+6.2f} C | "
            f"taxa: {texto_taxa} | "
            f"{estado}"
        )


        # ----------------------------------------------------
        # CSV
        # ----------------------------------------------------

        writer.writerow([
            round(tempo_atual, 3),
            temperatura_bruta,
            temperatura_filtrada,
            round(delta_T, 3),
            "" if taxa is None else round(taxa, 4),
            estado
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

            valores = (
                list(temperaturas_brutas)
                + list(temperaturas_filtradas)
            )

            minimo = min(valores)
            maximo = max(valores)

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
            f"Tempo:               {tempo_atual:.1f} s\n"
            f"Taxa:                {texto_taxa}\n\n"
            f"Estado: {estado}"
        )

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