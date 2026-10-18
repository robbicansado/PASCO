# PASCO — Firmware V5: análise estática inicial

**Origem:** PASCO.zip enviado pelo usuário. **Método:** análise offline, sem gravar firmware na placa.

## Evidências verificadas

- `flexduino_v5_backup.bin`: 32.768 bytes, SHA-256 `15523ff712b995281d28209bbc9294b55f963f45556d7f776c8d5d5740271eba`.
- `flexduino_v5_backup.hex`: Intel HEX; ao reconstruir a imagem de 32 KiB, todos os bytes coincidem com o `.bin`.
- `flexduino_v5_disassembly.txt`: UTF-16, 14.165 linhas.
- Início da imagem: instruções AVR `JMP`; vetor de reset salta para endereço de byte `0x00C4`.
- As instruções e o tamanho são compatíveis com AVR, mas não identificam isoladamente o modelo exato do microcontrolador.

## Strings presentes na imagem

| Offset em flash | Texto encontrado |
|---|---|
| `0x11da` | `--- FlexDuino Estabilizado V5 ---` |
| `0x11ff` | `Meteo -> T(C): ` |
| `0x120f` | `Ultrassom -> D(cm): ` |
| `0x1224` | `Ultrassom -> D(cm): 0.0` |
| `0x1633` | `PARAR` |
| `0x1639` | `Meteo -> ` |
| `0x1643` | `T(C): ` |
| `0x1656` | ` P(hPa): ` |
| `0x303f` | `FLEXDUINO: Inicializando Sensor Meteo...` |
| `0x30c0` | `SUCESSO: Sensor Meteo Conectado!` |
| `0x711b` | ` T(C)  ` |
| `0x7185` | ` T(C) ` |

## Interpretação

A presença de textos para `Meteo`, `Ultrassom`, `T(C)` e `P(hPa)` indica que o firmware contém rotinas ou mensagens relacionadas a temperatura, pressão e ultrassom. **Não comprova**, por si só, que sensores estavam conectados ou calibrados, nem que cada rotina funcionava.

## Próximas etapas

1. Mapear vetores de interrupção e inicialização de UART, ADC, timers e I²C/TWI no disassembly.
2. Identificar referências a essas strings e os caminhos de execução.
3. Confrontar os resultados com relatórios experimentais e mapeamento físico do FlexDuino.
4. Reimplementar rotinas por módulos em C++ sem afirmar que se trata do fonte original.
5. Validar em bancada, preferencialmente em hardware separado, sem sobrescrever backups.

**Limitações:** não foi executado nem gravado firmware; nenhuma equivalência funcional foi demonstrada.