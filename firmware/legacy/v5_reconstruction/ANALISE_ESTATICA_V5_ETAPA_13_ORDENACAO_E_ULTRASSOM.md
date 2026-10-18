# PASCO V5 — Etapa 13: ordenação e caminho ultrassônico

**Progresso global estimado: 35%**. Fonte: disassembly original `PASCO/flexduino_v5_disassembly.txt`. Sem teste físico.

## Ordenação dos valores ADC

- `0x0A88–0x0ADA`: percorre uma região de memória em passos de 4 bytes, compara pares por `call 0x107A` e troca valores quando a condição de comparação é atendida.
- Isso é **compatível com ordenação de amostras de ponto flutuante**. O método específico (por exemplo, bubble sort) e a direção da ordenação exigem confirmar a semântica de `0x107A`.
- `0x0ADC–0x0B04`: carrega um valor de 4 bytes em SRAM, imprime o texto que começa em SRAM `0x0143` (flash `0x11FF`, `Meteo -> T(C): `) e chama `0x0574` com precisão 2; depois imprime CR/LF. **Evidência direta de apresentação de uma medida de temperatura com duas casas decimais**.

## Medição de ultrassom

- `0x0B10–0x0B30`: alterna nível lógico de um pino usando `call 0x0118` e pequenos atrasos, padrão compatível com um pulso de trigger.
- `0x0B32–0x0B5C`: consulta tabelas de mapeamento de pinos AVR em flash e acessa registradores de I/O; indica caminho de leitura de um pino.
- `0x0B8C–0x0BA4`: aplica à duração uma constante float `0x3D0B4396` = **0,03400000185**, seguida de `0x3F000000` = **0,5**. O produto corresponde a `duracao * 0.034 * 0.5`, fórmula típica de distância de eco ultrassônico em centímetros **se** duração estiver em microssegundos.
- `0x0BC6–0x0C5E`: processamento de amostras, ordenação/seleção, impressão de string em SRAM `0x0153` (flash `0x120F`, `Ultrassom -> D(cm): `) e chamada de formatação com 2 casas decimais.
- `0x0C8C`: caminho alternativo imprime string em SRAM `0x0168` (flash `0x1224`, `Ultrassom -> D(cm): 0.0`).

## Cuidados de interpretação

- O código indica **estrutura de aquisição ultrassônica** e cálculo compatível com tempo de eco. Não demonstra qual sensor físico estava conectado nem valida precisão.
- As instruções de espera e acesso aos pinos ainda precisam ser rastreadas até as rotinas de tempo para confirmar unidade.
- O algoritmo exato de seleção das amostras ainda está em análise.
- Não usar os pinos históricos como pinagem atual do FlexDuino.

## Próximo marco

Confirmar unidades do tempo de eco, número de amostras e seleção estatística, e criar reconstrução modular do algoritmo com parâmetros explicitamente históricos.