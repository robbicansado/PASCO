import serial

ser = serial.Serial('COM5', 9600, timeout=1)

print("Conectado ao FlexDuino na COM5.")
print("Pressione Ctrl+C para parar.\n")

temperatura = None
distancia = None

try:
    while True:
        linha = ser.readline().decode(errors='ignore').strip()

        if not linha:
            continue

        if "Meteo -> T(C):" in linha:
            valor = linha.split(":")[-1].strip()

            try:
                temperatura = float(valor)
                print(f"Temperatura: {temperatura:.2f} °C")
            except ValueError:
                print(f"Erro ao interpretar Meteo: {linha}")

        elif "Ultrassom -> D(cm):" in linha:
            valor = linha.split(":")[-1].strip()

            try:
                distancia = float(valor)
                print(f"Distância: {distancia:.1f} cm")
            except ValueError:
                print(f"Erro ao interpretar Ultrassom: {linha}")

        else:
            print(f"[INFO] {linha}")

except KeyboardInterrupt:
    print("\nLeitura encerrada.")

finally:
    ser.close()
