import serial
import time
import csv
from datetime import datetime
import matplotlib.pyplot as plt
from collections import deque

# ============================================================
# PASCO - METEO V7
# Temperatura em tempo real
# ============================================================

PORTA = "COM5"
BAUDRATE = 9600

MAX_PONTOS = 200

# Parametros para classificacao da tendencia
LIMIAR = 0.05
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
print(" PASCO - METEO V7")
print("======================================")
print(f"Porta: {PORTA}")
print(f"Baud rate: {BAUDRATE}")
print("Aguardando dados do METEO...")
print("Ctrl+C para encerrar.\n")


# ============================================================
# CSV
# ============================================================

agora = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

nome_arquivo = (
    f"pasco_meteo_{agora}.csv"
)

arquivo = open(
    nome_arquivo,
    "w",
    newline="",
    encoding="utf-8"
)

writer = csv.writer(arquivo)

writer.writerow([
    "tempo_s",
    "temperatura_C",
    "delta_T_C",
    "estado"
])


# ============================================================
# DADOS
# ============================================================

tempos = deque(maxlen=MAX_PONTOS)
temperaturas = deque(maxlen=MAX_PONTOS)

inicio = time.time()

temperatura_inicial = None
temperatura_minima = None
temperatura_maxima = None


# ============================================================
# GRAFICO
# ============================================================

plt.ion()

fig, ax = plt.subplots(figsize=(11, 6))

linha_grafico, = ax.plot([], [])

ax.set_title(
    "PASCO - Experimento de Temperatura | METEO"
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

    if len(temperaturas) < JANELA_TENDENCIA:
        return "ESTABILIZANDO"

    recentes = list(temperaturas)[
        -JANELA_TENDENCIA:
    ]

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

    if variacao > LIMIAR:
        return "AQUECENDO"

    if variacao < -LIMIAR:
        return "RESFRIANDO"

    return "ESTAVEL"


# ============================================================
# AQUISICAO
# ============================================================

try:

    while True:

        # Mantem a janela responsiva SEMPRE
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

            temperatura = float(
                linha_serial
                .split(":")[-1]
                .strip()
            )

        except ValueError:
            continue


        # ----------------------------------------------------
        # TEMPO
        # ----------------------------------------------------

        tempo_atual = time.time() - inicio


        # ----------------------------------------------------
        # ESTATISTICAS
        # ----------------------------------------------------

        if temperatura_inicial is None:

            temperatura_inicial = temperatura
            temperatura_minima = temperatura
            temperatura_maxima = temperatura

        temperatura_minima = min(
            temperatura_minima,
            temperatura
        )

        temperatura_maxima = max(
            temperatura_maxima,
            temperatura
        )

        delta_T = (
            temperatura
            - temperatura_inicial
        )


        # ----------------------------------------------------
        # ARMAZENAMENTO
        # ----------------------------------------------------

        tempos.append(tempo_atual)
        temperaturas.append(temperatura)

        estado = calcular_estado()


        # ----------------------------------------------------
        # TERMINAL
        # ----------------------------------------------------

        print(
            f"{tempo_atual:7.1f} s | "
            f"T: {temperatura:6.2f} C | "
            f"dT: {delta_T:+6.2f} C | "
            f"{estado}"
        )


        # ----------------------------------------------------
        # CSV
        # ----------------------------------------------------

        writer.writerow([
            round(tempo_atual, 3),
            temperatura,
            round(delta_T, 3),
            estado
        ])

        arquivo.flush()


        # ----------------------------------------------------
        # GRAFICO
        # ----------------------------------------------------

        linha_grafico.set_data(
            list(tempos),
            list(temperaturas)
        )

        if len(tempos) >= 2:

            ax.set_xlim(
                min(tempos),
                max(tempos) + 1
            )

            minimo = min(temperaturas)
            maximo = max(temperaturas)

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
            f"Temperatura atual:   {temperatura:.2f} C\n"
            f"Temperatura inicial: {temperatura_inicial:.2f} C\n"
            f"Minima:              {temperatura_minima:.2f} C\n"
            f"Maxima:              {temperatura_maxima:.2f} C\n"
            f"Delta T:             {delta_T:+.2f} C\n"
            f"Tempo:               {tempo_atual:.1f} s\n\n"
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