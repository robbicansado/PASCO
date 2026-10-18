# Etapa 22 — Laço de repetição e atrasos

Fonte: disassembly original. **Progresso global estimado: 60%.**

- `0x00C4–0x0110`: runtime AVR, inicialização e chamada `0x08FA`.
- `0x0C7A`: salto relativo de volta a `0x0A1A` (conferir endereço de destino no disassembly completo). Isso demonstra repetição do bloco de aquisição, não apenas execução única.
- `0x0254–0x02B0`: rotina compatível com `delay` baseada em relógio de milissegundos: chama `0x020A` duas vezes, subtrai timestamps, compara com 1000 (`0x03E8`), decrementa o tempo solicitado. Isso sustenta a interpretação dos argumentos 2, 5 e 50 como **milissegundos**, sob a hipótese de runtime Arduino AVR.
- `0x0B16–0x0B2A`: dois loops curtos delimitam o pulso de disparo do ultrassom; duração exata depende do clock e de custos de instrução.
- `0x0C66–0x0C70`: chamada com argumento 50 antes da próxima iteração no caminho de medição válida.

**Limitação:** a duração real do ciclo inclui conversões ADC, ordenação, UART e possíveis timeouts do eco. Não é possível deduzi-la apenas somando delays.