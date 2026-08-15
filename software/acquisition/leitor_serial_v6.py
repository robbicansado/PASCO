import serial
import matplotlib.pyplot as plt
from collections import deque
import time
import csv
from datetime import datetime

PORTA = "COM5"
BAUD = 9600

# Correcao provisoria. Ainda precisa de calibracao experimental.
CORRECAO = 16.0

# Variacao usada para decidir se esta aquecendo/resfriando
LIMIAR_ESTADO = 0.03

ser = serial.Serial(PORTA, BAUD, timeout=1)

tempos = deque(maxlen=150)
temperaturas = deque(maxlen=150)

# Usado para calcular tendencia recente
historico_estado = deque(maxlen=15)

inicio = time.time()

temperatura_inicial = None
temperatura_minima = None
temperatura_maxima = None

nome_csv = (
    "dados_temperatura_"
    + datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    + ".csv"
)

arquivo_csv = open(
    nome_csv,
    "w",
    newline="",
    encoding="utf-8"
)

writer = csv.writer(arquivo_csv)

writer.writerow([
    "tempo_s",
    "temperatura_bruta_C",
    "temperatura_corrigida_C",
    "delta_T_C",
    "estado"
])

# -------------------------
# GRAFICO
# -------------------------

plt.ion()

fig, ax = plt.subplots(figsize=(10, 6))

linha_grafico, = ax.plot([], [])

ax.set_title("PASCO - Experimento de Temperatura")
ax.set_xlabel("Tempo (s)")
ax.set_ylabel("Temperatura (C)")
ax.grid(True)

# Painel de informacoes
painel = ax.text(
    0.02,
    0.97,
    "",
    transform=ax.transAxes,
    verticalalignment="top",
    bbox=dict(boxstyle="round", alpha=0.8)
)

print("====================================")
print(" PASCO - ANALISE DE TEMPERATURA")
print("====================================")
print()
print(f"Arquivo: {nome_csv}")
print("Correcao provisoria: +16 C")
print("Ctrl+C para encerrar.")
print()

try:

    while True:

        linha = ser.readline().decode(
            errors="ignore"
        ).strip()

        if "Meteo -> T(C):" not in linha:
            continue

        try:

            temperatura_bruta = float(
                linha.split(":")[-1].strip()
            )

        except ValueError:
            continue

        temperatura = (
            temperatura_bruta + CORRECAO
        )

        tempo = time.time() - inicio

        # -------------------------
        # ESTATISTICAS
        # -------------------------

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

        delta_t = (
            temperatura
            - temperatura_inicial
        )

        tempos.append(tempo)
        temperaturas.append(temperatura)

        historico_estado.append(temperatura)

        # -------------------------
        # ESTADO TERMICO
        # -------------------------

        estado = "ESTAVEL"

        if len(historico_estado) >= 10:

            diferenca = (
                historico_estado[-1]
                - historico_estado[0]
            )

            if diferenca > LIMIAR_ESTADO:

                estado = "AQUECENDO"

            elif diferenca < -LIMIAR_ESTADO:

                estado = "RESFRIANDO"

        # -------------------------
        # SALVAR CSV
        # -------------------------

        writer.writerow([
            round(tempo, 3),
            temperatura_bruta,
            temperatura,
            round(delta_t, 3),
            estado
        ])

        arquivo_csv.flush()

        # -------------------------
        # TERMINAL
        # -------------------------

        print(
            f"{tempo:6.1f} s | "
            f"T: {temperatura:6.2f} C | "
            f"dT: {delta_t:+6.2f} C | "
            f"{estado}"
        )

        # -------------------------
        # ATUALIZAR GRAFICO
        # -------------------------

        linha_grafico.set_data(
            tempos,
            temperaturas
        )

        ax.relim()
        ax.autoscale_view()

        texto_painel = (
            f"Temperatura atual:   {temperatura:.2f} C\n"
            f"Temperatura inicial: {temperatura_inicial:.2f} C\n"
            f"Minima:              {temperatura_minima:.2f} C\n"
            f"Maxima:              {temperatura_maxima:.2f} C\n"
            f"Delta T:             {delta_t:+.2f} C\n"
            f"Tempo:               {tempo:.1f} s\n"
            f"\nEstado: {estado}"
        )

        painel.set_text(texto_painel)

        fig.canvas.draw()
        fig.canvas.flush_events()

except KeyboardInterrupt:

    print()
    print("====================================")
    print(" EXPERIMENTO ENCERRADO")
    print("====================================")

finally:

    ser.close()
    arquivo_csv.close()

    if temperatura_inicial is not None:

        print(
            f"Temperatura inicial: "
            f"{temperatura_inicial:.2f} C"
        )

        print(
            f"Temperatura minima: "
            f"{temperatura_minima:.2f} C"
        )

        print(
            f"Temperatura maxima: "
            f"{temperatura_maxima:.2f} C"
        )

        print(
            f"Variacao maxima: "
            f"{temperatura_maxima - temperatura_inicial:+.2f} C"
        )

    print()
    print(f"Dados salvos em: {nome_csv}")

    plt.ioff()
    plt.show()