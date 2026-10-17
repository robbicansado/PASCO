import serial
import matplotlib.pyplot as plt
from collections import deque
import time

PORTA = 'COM5'
BAUD = 9600

ser = serial.Serial(PORTA, BAUD, timeout=1)

tempos = deque(maxlen=100)
temperaturas = deque(maxlen=100)

inicio = time.time()

plt.ion()

fig, ax = plt.subplots()
linha_grafico, = ax.plot([], [])

ax.set_title("PASCO - Temperatura em tempo real")
ax.set_xlabel("Tempo (s)")
ax.set_ylabel("Temperatura (°C)")
ax.grid(True)

print("PASCO conectado.")
print("Lendo temperatura em tempo real...")
print("Ctrl+C para encerrar.\n")

try:
    while True:

        linha = ser.readline().decode(errors='ignore').strip()

        if "Meteo -> T(C):" in linha:

            try:
                temperatura = float(linha.split(":")[-1].strip())
                tempo = time.time() - inicio

                tempos.append(tempo)
                temperaturas.append(temperatura)

                print(f"{tempo:6.1f} s | {temperatura:.2f} °C")

                linha_grafico.set_data(tempos, temperaturas)

                ax.relim()
                ax.autoscale_view()

                fig.canvas.draw()
                fig.canvas.flush_events()

            except ValueError:
                pass

except KeyboardInterrupt:
    print("\nAquisição encerrada.")

finally:
    ser.close()
    plt.ioff()
    plt.show()
