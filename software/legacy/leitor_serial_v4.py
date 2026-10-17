import serial
import matplotlib.pyplot as plt
from collections import deque
import time

PORTA = "COM5"
BAUD = 9600

# Correcao provisoria para retirar o offset do firmware
CORRECAO = 16.0

ser = serial.Serial(PORTA, BAUD, timeout=1)

tempos = deque(maxlen=100)
temperaturas = deque(maxlen=100)

inicio = time.time()

plt.ion()

fig, ax = plt.subplots()
linha_grafico, = ax.plot([], [])

ax.set_title("PASCO - Temperatura corrigida em tempo real")
ax.set_xlabel("Tempo (s)")
ax.set_ylabel("Temperatura (C)")
ax.grid(True)

print("PASCO conectado.")
print("Correcao provisoria aplicada: +16 C")
print("Ctrl+C para encerrar.\n")

try:
    while True:

        linha = ser.readline().decode(errors="ignore").strip()

        if "Meteo -> T(C):" in linha:

            try:
                temperatura_recebida = float(
                    linha.split(":")[-1].strip()
                )

                temperatura_corrigida = (
                    temperatura_recebida + CORRECAO
                )

                tempo = time.time() - inicio

                tempos.append(tempo)
                temperaturas.append(temperatura_corrigida)

                print(
                    f"{tempo:6.1f} s | "
                    f"bruto: {temperatura_recebida:6.2f} C | "
                    f"corrigido: {temperatura_corrigida:6.2f} C"
                )

                linha_grafico.set_data(
                    tempos,
                    temperaturas
                )

                ax.relim()
                ax.autoscale_view()

                fig.canvas.draw()
                fig.canvas.flush_events()

            except ValueError:
                pass

except KeyboardInterrupt:
    print("\nAquisicao encerrada.")

finally:
    ser.close()
    plt.ioff()
    plt.show()
