# PASCO V5 — Etapa 12: ADC, 60 amostras e fórmula candidata

**Progresso global estimado: 35%** (estimativa qualitativa, não cobertura de código). Fonte: `PASCO.zip`, disassembly AVR e imagem binária V5. Análise estática, sem hardware.

## Instruções observadas

- `0x0A1E: ldi r24,0x40` e `0x0A20: sts 0x007C,r24`. No ATmega328P, `ADMUX=0x40` significa referência AVcc (`REFS0=1`) e canal ADC0 (`MUX=0`), isto é, **A0**.
- `0x0A24–0x0A34`: define `ADSC` em `ADCSRA` (bit 6) e aguarda que seja limpo: conversão ADC.
- `0x0A36–0x0A3A`: lê `ADCL` e `ADCH`, que compõem a amostra de 10 bits.
- `0x0A46: call 0x0F1A` converte a amostra inteira para representação de ponto flutuante (hipótese apoiada pelas chamadas seguintes).
- `0x0A4A–0x0A52`: constante IEEE-754 `0x3BA0280A` = aproximadamente **0,0048875855**, compatível com `5.0/1023.0`.
- `0x0A56–0x0A5E`: constante `0x41200000` = **10.0**.
- `0x0A62–0x0A6A`: constante `0x41000000` = **8.0**, seguida da chamada `0x0CF0` (operação a confirmar).
- `0x0A6E–0x0A74`: grava um valor de quatro bytes em buffer.
- `0x0A82–0x0A86`: compara índice/ponteiro com `0x0194` e retorna a `0x0A1E`. A combinação com o armazenamento de 4 bytes e a origem `0x0104` é **compatível com 60 amostras** (0x0194-0x0104 = 144 bytes = 36 floats) **mas precisa ser revista**: o endereço 0x0194 é o limite de buffer e a origem do buffer deve ser rastreada antes de fixar a contagem.

### Correção sobre a contagem

A leitura `0x0A12–0x0A1C` define `r3:r2=0x0288` e `Y=0x0194`; `0x0A6E` grava 4 bytes e incrementa Y. O laço termina quando `r3:r2 == Y`, isto é, `(0x0288-0x0194)/4 = 61` valores **se** esses limites forem o início e fim corretos. Contudo, o limite 0x0288 pode ser área reservada para outros objetos e o tamanho do buffer pode ser 61. **Não afirmar 60 amostras sem confirmar os endereços exatos e limites de memória**.

## Interpretação da conversão

A sequência de constantes sugere `valorADC * (5/1023) * 10 + 8` ou expressão próxima. **A operação da chamada `0x0CF0` ainda precisa ser identificada**; portanto a fórmula é candidata, não confirmada. O fator 10 pode ter relação com escala de sensor; não atribuir automaticamente ao LM35, que é uma validação posterior.

## Próximas verificações

Desmontar `0x0CF0`, `0x1084` e o corpo da rotina de ordenação `0x0A88–0x0ADA`; confirmar os limites do buffer e a relação entre a amostra calculada e o texto `Meteo -> T(C)`.

**Histórico:** não utilizar esta pinagem como instrução para conectar o PASCO atual.