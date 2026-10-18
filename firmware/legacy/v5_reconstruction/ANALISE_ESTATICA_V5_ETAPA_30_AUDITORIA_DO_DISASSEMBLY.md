# Etapa 30 — Auditoria do disassembly original

**Progresso estimado: 70%, mantido.** Fonte primária: `PASCO/flexduino_v5_disassembly.txt` extraído de `PASCO.zip`. Em vez de aumentar o percentual sem comprovação, foram verificadas 12 invariantes por script local executado com Python.

## Verificações efetivamente executadas

1. `0x0A1E–0x0A20`: ADMUX recebe 0x40, compatível com AVcc/ADC0 no ATmega328P.
2. `0x0A28`: ADSC é acionado.
3. `0x0A36–0x0A3A`: leitura de ADCL e ADCH.
4. Buffer 0x0194–0x0287 comporta 61 floats de 4 bytes; o laço compara o ponteiro em `0x0A86`.
5. `0x020C` corresponde ao elemento 30 do buffer.
6. `0x0B4E–0x0B50`: limite de 15000.
7. `0x0B06`: cinco tentativas.
8. `0x08B4` e `0x08C6`: contador por iterações de leitura do pino.
9. `0x0B6E`: máscara de 28 bits no resultado de pulso.
10. `0x0C66–0x0C6E`: argumento 50 para rotina de espera.
11. `0x0C7A`: salto de volta para `0x0A1A`.
12. `0x0C90–0x0C94`: impressão de falha e retorno ao caminho comum.

**Saída local real:** `12 invariantes do disassembly confirmadas`.

A verificação confirma instruções e endereços, não mede o hardware nem prova a semântica física de todas as rotinas. O script de auditoria acompanha esta etapa.