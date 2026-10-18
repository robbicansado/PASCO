# PASCO — Firmware V5, Etapa 03: interrupções e comunicação

Data: 17/10/2026. Fonte: `PASCO.zip`, arquivos `flexduino_v5_backup.bin` e `flexduino_v5_disassembly.txt`. Inspeção estática, sem gravação na placa.

## Descobertas verificadas

- O vetor de reset em `0x0000` salta para `0x00c4`.
- Os vetores em `0x0040`, `0x0048` e `0x004c` saltam, respectivamente, para `0x072c`, `0x080c` e `0x07c0`.
- A rotina `0x072c` salva registradores e manipula contadores de múltiplos bytes em SRAM (`0x0289`–`0x028c`). Isso é **compatível** com uma rotina de contagem de tempo, mas a finalidade exata requer rastreamento adicional.
- A rotina `0x080c` usa ponteiros em SRAM (`0x02a1`–`0x02a2`, `0x02a7`–`0x02a8`) e manipula um índice circular limitado por `0x3f` (63). Isso é **compatível** com um buffer circular de 64 posições e, no contexto do vetor, com transmissão serial; ainda não está demonstrado qual é a taxa serial.
- A rotina `0x07c0` salva registradores e chama `0x03b4` com o par de registradores `r25:r24` contendo `0x0291`. Isso sugere tratamento de dados em memória, mas não basta para atribuir função ao sensor.

## Interpretação condicionada ao microcontrolador

**Se** o microcontrolador for ATmega328P, os vetores `0x0040`, `0x0048` e `0x004c` correspondem, respectivamente, a `TIMER0_OVF`, `USART_RX` e `USART_UDRE`. Essa correspondência é consistente com o padrão de interrupções do Arduino Nano/Uno. **Não é identificação definitiva do chip.**

## Consequência para reconstrução

O V5 parece conter uma infraestrutura de temporização e comunicação serial baseada em interrupções. Ainda não é justificável fixar `Serial.begin(9600)` como parâmetro original do V5 apenas com estes trechos. Os scripts históricos que usam 9600 baud fornecem uma hipótese de trabalho, não prova independente.

## Próxima análise executável

1. Rastrear o corpo completo de `0x080c` e `0x07c0` até o retorno `reti` e localizar acessos aos registradores USART.
2. Procurar a rotina que configura `UBRR0H/UBRR0L` e `UCSR0A/B/C`; derivar baud rate com frequência de clock explicitamente assumida.
3. Identificar referências cruzadas às mensagens `Meteo` e `Ultrassom` antes de reescrever qualquer módulo de sensor.
4. Comparar pinos e conexões com os relatórios posteriores; não inferir cabeamento atual a partir do V5.

**Status:** evidência nova extraída; nenhum código-fonte original recuperado, nenhum firmware reconstruído/gravado.