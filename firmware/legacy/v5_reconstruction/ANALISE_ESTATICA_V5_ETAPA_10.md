# PASCO V5 — Etapa 10: transmissão serial da aplicação

**Fonte:** `PASCO.zip`, `PASCO/flexduino_v5_disassembly.txt`. Análise estática, sem gravação na placa.

## Fluxo de transmissão

- `0x04D2`: percorre string terminada em NUL e encaminha comprimento e ponteiro a `0x02B8`.
- `0x02B8`: percorre bytes (`0x02E4: ld r22, Y+`) e executa `icall` em `0x02F4` via ponteiro de função de uma estrutura. Compatível com abstração `Print` da biblioteca Arduino AVR, mas identificação exata da classe é inferida.
- `0x03F8`: rotina compatível com escrita de byte em buffer circular de 64 posições: índice mascarado com `0x3F` em `0x0450`, gravação em `0x0480`, habilitação de interrupção em `0x048E`.
- `0x03B4`: retira byte do buffer e escreve no registrador de dados apontado pela estrutura (`0x03D4: st X,r18`). Evidência forte de transmissão UART por interrupção.

## Inicialização serial observada em `0x08FA`

| Endereço | Operação |
|---|---|
| `0x097C` | zera `0x00C1` (UCSR0B se ATmega328P) |
| `0x0988` | grava `0x02` no endereço apontado por SRAM `0x02A1–0x02A2` |
| `0x099E` | grava `0xCF` (207) no endereço apontado por SRAM `0x029F–0x02A0` |
| `0x09AE` | grava `0x06` no endereço apontado por SRAM `0x02A5–0x02A6` |
| `0x09BA–0x09E8` | altera bits 0x10, 0x08, 0x80 e 0x20 no endereço apontado por SRAM `0x02A3–0x02A4` |

O padrão é compatível com `Serial.begin(9600)` em ATmega328P, assumindo ponteiros para UCSR0A/UBRR0L/UCSR0C/UCSR0B respectivamente e clock de 16 MHz. Com U2X0=1 e UBRR0=207:

`16.000.000 / (8 × (207 + 1)) = 9.615,38 bps` (erro de +0,16% em relação a 9600).

**Pendente:** confirmar os endereços efetivos desses ponteiros na construção dos objetos e a frequência de clock da placa. Não é medição de baud rate. O divisor 16 identificado na região `0x7A7E` é compatível com o bootloader e não deve ser atribuído à aplicação.

## Próximos passos

1. Rastrear construtores para resolver os ponteiros em SRAM `0x029D–0x02A6`.
2. Fechar a cadeia da UART e identificar o objeto serial.
3. Rastrear leitura ADC em `0x0A1E–0x0A46` e conversões.
4. Reconstituir C++ apenas com graus de confiança explícitos; não gravar na placa funcional.

**Status:** análise de arquitetura, não recuperação do fonte original nem firmware testado.
