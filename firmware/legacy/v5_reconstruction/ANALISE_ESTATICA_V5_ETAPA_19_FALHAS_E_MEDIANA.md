# Etapa 19 — Ultrassom: até 5 tentativas, falhas e seleção central

**Progresso estimado: 60%.** Fonte: disassembly original.

- `0x0B06`: contador de cinco tentativas.
- `0x0B5C–0x0B78`: resultado nulo não é incluído no conjunto de distâncias válidas.
- `0x0BCC–0x0C32`: ordenação dos floats válidos.
- `0x0C34–0x0C4A`: índice `n/2` no vetor ordenado em SRAM a partir de `0x0180`. Para contagem par, escolhe o elemento central **superior**; não calcula média.
- `0x0BC6–0x0BCA`: se zero medidas válidas, salta a `0x0C8C`, imprimindo `Ultrassom -> D(cm): 0.0`.

Essas decisões foram usadas na reconstrução independente de filtros em C++. O valor impresso em caso de falha não deve ser interpretado como distância zero fisicamente medida. A unidade do contador de eco ainda precisa ser verificada.

**Histórico:** não aplicar os pinos V5 ao FlexDuino atual.