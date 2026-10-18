# PASCO — Firmware V5: Etapa 04, verificação de strings e resíduos

**Método:** leitura estática do arquivo `PASCO/flexduino_v5_backup.bin` extraído de `PASCO.zip`, sem modificar o FlexDuino. Endereços são offsets em bytes do arquivo, apresentados em hexadecimal.

## Evidências extraídas do binário

| Offset | Texto encontrado |
|---|---|
| `0x11DA` | `--- FlexDuino Estabilizado V5 ---` |
| `0x11FF` | `Meteo -> T(C): ` |
| `0x120F` | `Ultrassom -> D(cm): ` |
| `0x1224` | `Ultrassom -> D(cm): 0.0` |
| `0x303F` | `FLEXDUINO: Inicializando Sensor Meteo...` |
| `0x3068` | `ERRO: Sensor BME280 nao encontrado!` |
| `0x308C` | `Verifique se esta conectado na porta ANALOG (A4/A5)` |
| `0x30C0` | `SUCESSO: Sensor Meteo Conectado!` |
| `0x30E1` | `METEO:T=` |
| `0x6DFE` | `-- Default Test --` |
| `0x6E11` | `Could not find a valid BME280 sensor, check wiring!` |
| `0x6E45` | `BMP180 init success` |
| `0x6E59` | `BMP180 init fail` |

## Interpretação cautelosa

A imagem binária tem 32.768 bytes, o tamanho de toda a memória flash de um ATmega328P. A presença de mensagens de múltiplas versões e bibliotecas **não demonstra** que todas façam parte do programa ativo. Podem existir dados não utilizados, textos embutidos em bibliotecas ou resíduos de gravações anteriores, dependendo de como o backup foi obtido.

**Não confirmado:** se o conjunto BME280 é alcançável pelo vetor de reset, qual a taxa serial original, qual sensor efetivamente era inicializado, e se a imagem representa uma cópia fiel de um único build.

## Próximo teste estático

Rastrear o fluxo de controle a partir do vetor de reset e identificar referências de instruções às regiões que contêm as mensagens; verificar quais textos são efetivamente usados e quais são possivelmente inertes. Depois, localizar a inicialização USART e derivar a taxa de transmissão com hipótese explícita de clock. **Não gravar firmware reconstruído na placa antes de validar essas hipóteses.**