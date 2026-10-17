import serial
import time
import csv
from datetime import datetime
from collections import deque
from statistics import median
import matplotlib.pyplot as plt

# ============================================================
# PASCO - LM35 CALIBRADO V1
# Calibracao cruzada preliminar LM35 x METEO
# ============================================================

PORTA = "COM5"
BAUDRATE = 9600

# Calibracao preliminar obtida em 16/08/2026
A = 3.69
B = 40.36

JANELA_FILTRO = 5
MAX_PONTOS = 250

# ============================================================
# SERIAL
# ============================================================

ser = serial.Serial(
    PORTA,
    BAUDRATE,
    timeout=0.2
)

time.sleep(2)

print("==========================================")
print(" PASCO - LM35 CALIBRADO V1")
print(" Calibracao cruzada preliminar")
print("==========================================")
print(f"Porta: {PORTA}")
print(f"Baud rate: {BAUDRATE}")
print()
print("Equacao aplicada:")
print("T_corrigida = 3.69*T_firmware + 40.36")
print()
print("Ctrl+C para encerrar.\n")


# ============================================================
# CSV
# ============================================================

agora = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

nome_arquivo = (
    f"pasco_lm35_calibrado_{agora}.csv"
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
    "leitura_firmware",
    "temperatura_corrigida_C",
    "temperatura_filtrada_C"
])


# ============================================================
# DADOS
# ============================================================

inicio = time.time()

tempos = deque(maxlen=MAX_PONTOS)
temperaturas = deque(maxlen=MAX_PONTOS)

janela_filtro = deque(maxlen=JANELA_FILTRO)


# ============================================================
# GRAFICO
# ============================================================

plt.ion()

fig, ax = plt.subplots(figsize=(11, 6))

linha, = ax.plot(
    [],
    [],
    linewidth=2
)

ax.set_title(
    "PASCO - LM35 | Temperatura calibrada"
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

            leitura_firmware = float(
                linha_serial
                .split(":")[-1]
                .strip()
            )

        except ValueError:
            continue


        # ----------------------------------------------------
        # CALIBRACAO
        # ----------------------------------------------------

        temperatura_corrigida = (
            A * leitura_firmware
            + B
        )


        # ----------------------------------------------------
        # FILTRO
        # ----------------------------------------------------

        janela_filtro.append(
            temperatura_corrigida
        )

        temperatura_filtrada = median(
            janela_filtro
        )


        # ----------------------------------------------------
        # TEMPO
        # ----------------------------------------------------

        tempo_atual = time.time() - inicio


        # ----------------------------------------------------
        # DADOS
        # ----------------------------------------------------

        tempos.append(
            tempo_atual
        )

        temperaturas.append(
            temperatura_filtrada
        )


        # ----------------------------------------------------
        # TERMINAL
        # ----------------------------------------------------

        print(
            f"{tempo_atual:7.1f} s | "
            f"firmware: {leitura_firmware:6.2f} | "
            f"T corrigida: {temperatura_corrigida:6.2f} C | "
            f"T filtrada: {temperatura_filtrada:6.2f} C"
        )


        # ----------------------------------------------------
        # CSV
        # ----------------------------------------------------

        writer.writerow([
            round(tempo_atual, 3),
            leitura_firmware,
            round(
                temperatura_corrigida,
                3
            ),
            round(
                temperatura_filtrada,
                3
            )
        ])

        arquivo.flush()


        # ----------------------------------------------------
        # GRAFICO
        # ----------------------------------------------------

        linha.set_data(
            list(tempos),
            list(temperaturas)
        )

        if len(tempos) >= 2:

            ax.set_xlim(
                min(tempos),
                max(tempos) + 1
            )

            minimo = min(
                temperaturas
            )

            maximo = max(
                temperaturas
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

        painel.set_text(
            f"Leitura firmware: {leitura_firmware:.2f}\n"
            f"Temperatura:      {temperatura_filtrada:.2f} C\n\n"
            f"T = 3.69*f + 40.36\n"
            f"Calibracao preliminar LM35 x METEO"
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

    print(
        f"Dados salvos em: {nome_arquivo}"
    )

    plt.ioff()
    plt.show()
