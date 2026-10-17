import serial

ser = serial.Serial('COM5', 9600, timeout=1)

print("Conectado ao FlexDuino na COM5.")
print("Pressione Ctrl+C para parar.\n")

try:
    while True:
        linha = ser.readline().decode(errors='ignore').strip()

        if linha:
            print(linha)

except KeyboardInterrupt:
    print("\nLeitura encerrada.")

finally:
    ser.close()
