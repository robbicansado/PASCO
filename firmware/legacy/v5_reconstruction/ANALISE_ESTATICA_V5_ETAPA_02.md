# PASCO / FlexDuino — Engenharia reversa V5, Etapa 02

Data: 17/10/2026. Método: leitura **estática** dos arquivos originais extraídos de `PASCO.zip`. Nenhuma gravação ou execução na placa.

## Evidências verificadas

- `flexduino_v5_backup.bin`: 32.768 bytes; SHA-256 `15523ff712b995281d28209bbc9294b55f963f45556d7f776c8d5d5740271eba`.
- `flexduino_v5_backup.hex`: 78.861 bytes; SHA-256 `a9341ff177c96f76a56c62840ce28e8fa6b7d3697ae4455ee16fd65209b3055e`.
- `flexduino_v5_disassembly.txt`: 1.182.726 bytes; UTF-16; SHA-256 `e30cba2e894ff4d8a622c026ed1664a59cd71263206f200d7186b3157cf12355`.
- O início do disassembly mostra tabela de vetores AVR. Reset em `0x0000` salta para `0x00c4`; muitos vetores saltam para `0x0114`; os vetores nas posições `0x0040`, `0x0048` e `0x004c` saltam, respectivamente, para `0x072c`, `0x080c` e `0x07c0`. **Ainda não se atribuiu função a essas interrupções.**

## Cadeias legíveis encontradas no binário

| Offset hexadecimal | Texto literal |
| --- | --- |
| `0x11f5` | `V5` dentro de `--- FlexDuino Estabilizado V5 ---` |
| `0x11ff` | `Meteo -> T(C): ` |
| `0x120f` | `Ultrassom -> D(cm): ` |
| `0x1224` | `Ultrassom -> D(cm): 0.0` |
| `0x1633` | `PARAR` |
| `0x1639` | `Meteo -> ` |
| `0x1657` | ` P(hPa): ` |
| `0x303f` | `FLEXDUINO: Inicializando Sensor Meteo...` |
| `0x3068` | `ERRO: Sensor BME280 nao encontrado!` |
| `0x308c` | `Verifique se esta conectado na porta ANALOG (A4/A5)` |
| `0x30c0` | `SUCESSO: Sensor Meteo Conectado!` |
| `0x30e1` | `METEO:T=` (seguido de `;P=` e `;H=`) |

Os offsets são posições dos bytes **na imagem binária**, não endereços de funções. A presença de mensagens não demonstra, por si só, que o respectivo caminho de execução seja utilizado.

## Hipóteses e limites

1. Há indícios de código relacionado a BME280 e à interface I²C nos pinos A4/A5; isso **não comprova** que o sensor tenha funcionado no hardware real.
2. Há mensagens para temperatura e ultrassom; ainda é necessário localizar as chamadas que imprimem esses textos e as rotinas de aquisição.
3. Não é seguro atribuir o modelo exato do AVR apenas à tabela de vetores. Verificar a placa, o mapeamento de memória e os acessos a registradores.
4. Ainda não há código-fonte V5 reconstruído nem firmware recompilado. O arquivo `.ino` vazio não representa recuperação.

## Próximos passos concretos

- Mapear referências aos endereços das strings em instruções de carregamento de ponteiros AVR.
- Traçar o fluxo a partir de `0x00c4`, inclusive a inicialização da UART e eventuais rotinas de I²C.
- Separar funções de aquisição, serialização e tratamento de erros; documentar cada função com grau de confiança.
- Escrever C++ somente após localizar evidência suficiente, sem substituir o backup original.