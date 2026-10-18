# Etapa 37 — Serial da aplicação: configuração determinada

**Progresso estimado: 80%.** Esta análise distingue a aplicação do bootloader.

O construtor `0x0C96` confirma que:
- `0x0988–0x098A`: `UCSR0A = 0x02` ativa U2X0 (velocidade dupla).
- `0x098C–0x09A0`: `UBRR0H = 0` e `UBRR0L = 207`.
- `0x09AE–0x09B0`: `UCSR0C = 0x06` seleciona formato assíncrono de 8 bits, sem paridade, um stop bit (8N1).
- `0x09BA–0x09E8`: bits de controle da USART são modificados via UCSR0B.

Com clock hipotético de 16 MHz e U2X0=1, a taxa física é `16000000/(8*(207+1)) = 9615,38 bps`, correspondente à configuração nominal **Serial.begin(9600)**, erro +0,16%.

**Resultado:** a configuração dos registradores foi confirmada no binário; a frequência real do oscilador não foi medida. A rotina do bootloader `0x7A7E` não é a origem dessa conclusão.