# PASCO — Firmware V5: Etapa 05 — Configuração USART

**Fonte:** `PASCO/flexduino_v5_disassembly.txt` do ZIP original. **Método:** análise estática; nenhuma gravação na placa.

## Evidência de registradores

Em `0x7A7E–0x7A90`:

```asm
7a7e: ldi r24, 0x10
7a80: sts 0x00C4, r24
7a84: sts 0x00C5, r1
7a88: ldi r24, 0x18
7a8a: sts 0x00C1, r24
7a8e: ldi r24, 0x06
7a90: sts 0x00C2, r24
```

Assumindo ATmega328P: `0xC4` = UBRR0L, `0xC5` = UBRR0H, `0xC1` = UCSR0B e `0xC2` = UCSR0C. Assim, UBRR0 = 16, transmissão e recepção habilitadas (`0x18`), modo assíncrono 8 bits, sem paridade, 1 stop bit (`0x06`). Em modo normal U2X0=0 e F_CPU=16 MHz, a taxa é 16.000.000/[16*(16+1)] = 58.823,5 bps, aproximadamente 58,8 kbps. **Não é evidência de 9600 bps.** Se o clock, U2X0 ou o modelo forem diferentes, o cálculo muda.

A rotina de configuração começa em `0x7A5A`; existe uma chamada a ela em `0x789A`. Não está ainda provado que esse caminho seja alcançado desde o vetor de reset, nem que a configuração persista sem alterações. Há outras rotinas USART na imagem, inclusive `0x097C` e `0x1C02` que zeram UCSR0B, indicando que o binário contém múltiplos contextos de inicialização.

## Próximas verificações

1. Rastrear a alcançabilidade de `0x789A` e `0x7A5A` a partir de `0x00C4` (vetor de reset).
2. Identificar escritas em UCSR0A (`0xC0`) para confirmar U2X0.
3. Verificar clock e MCU físicos antes de interpretar o baud rate como taxa efetiva do FlexDuino.
4. Confrontar com os testes históricos de serial, sem pressupor que o firmware V5 represente o mapeamento atual.