# Etapa 34 — Hipótese forte de 9600 baud, 8N1

**Progresso estimado: 75%.** Fonte: disassembly original da aplicação.

- `0x097C`: zera UCSR0B diretamente.
- `0x0988–0x098A`: escreve `0x02` em endereço indireto via SRAM `0x02A1–0x02A2`.
- `0x099E–0x09A0`: escreve `0xCF` (207) via ponteiro `0x029F–0x02A0`.
- `0x09AE–0x09B0`: escreve `0x06` via ponteiro `0x02A5–0x02A6`.

Se os ponteiros apontam para UCSR0A, UBRR0L e UCSR0C, respectivamente, a configuração corresponde a U2X0=1, divisor 207 e quadro 8N1. **Com clock de 16 MHz**, isso equivale a 9615,38 baud (erro de +0,16% frente a 9600).

Ainda falta demonstrar a inicialização dos ponteiros. O baud do bootloader não serve como evidência para a aplicação. Não chamar 9600 de definitivamente confirmado.