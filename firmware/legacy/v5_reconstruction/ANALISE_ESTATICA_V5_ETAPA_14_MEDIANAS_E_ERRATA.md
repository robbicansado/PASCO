# PASCO V5 — Etapa 14: mediana identificada e correção da contagem

**Progresso global estimado: 45%.** Estimativa de engenharia reversa, não percentagem de código-fonte recuperado.

## Confirmação das 61 leituras ADC

Em `0x0A12–0x0A1C`, o firmware inicializa `r3:r2=0x0288` e o ponteiro Y em `0x0194`. Cada ciclo grava um `float` de 4 bytes e avança Y em quatro (`0x0A6E–0x0A74`). Em `0x0A82–0x0A86`, compara Y com `0x0288` e repete enquanto forem diferentes. A diferença `0x0288-0x0194=0xF4=244` bytes equivale a **61 amostras**.

**Errata:** a afirmação preliminar de “60 leituras” e o cálculo de 36 valores mencionados na Etapa 12 estavam incorretos. O valor sustentado pelo trecho é **61**.

## Mediana de temperatura

Após a ordenação em `0x0A88–0x0ADA`, o código carrega um `float` de SRAM `0x020C–0x020F` (`0x0ADC–0x0AE8`). O deslocamento relativo ao início do buffer é `0x020C - 0x0194 = 0x78 = 120` bytes, ou seja, **índice 30** para floats de 4 bytes (31º elemento em 61). Isso é o **elemento central** de uma lista ordenada: a **mediana**.

A seguir imprime `Meteo -> T(C): ` e chama uma rotina de impressão de ponto flutuante com 2 casas decimais.

## Ultrassom: mediana de até cinco valores

Em `0x0B06–0x0BC4`, há um contador inicializado com 5, leituras de pulso e cálculos de distância. Quando o pulso retorna valor não nulo, o resultado é guardado e o contador de válidos é incrementado. Em `0x0BCC–0x0C32`, o código ordena os valores válidos. Em `0x0C34–0x0C4A`, calcula o índice central via divisão inteira por dois, multiplica por 4 e busca o float em buffer a partir de `0x0180`. Isso é compatível com **seleção do elemento central ordenado**; para quantidade par, a rotina parece selecionar um dos dois centrais, não calcular média.

A constante `0.034` multiplicada por `0.5` aparece no cálculo da distância, compatível com `distancia_cm = duracao_us * 0.034 / 2`, condicionada à confirmação de que a duração está em microssegundos.

## Esboço de algoritmo reconstruído (não é o fonte original)

```text
configurar serial e pinos históricos
repetir:
  coletar 61 leituras de ADC0
  converter cada leitura por fórmula float ainda sob investigação
  ordenar leituras
  imprimir o elemento de índice 30 como Meteo -> T(C), 2 casas
  tentar até 5 medidas ultrassônicas
  guardar apenas distâncias de pulsos válidos
  ordenar distâncias válidas
  imprimir elemento central (ou 0.0 quando não há valores válidos)
  aguardar e repetir
```

## Limitações

- A ordem de comparação e a semântica precisa das funções float precisam ser validadas.
- O valor 8.0 na conversão de temperatura ainda não foi provado como soma ou subtração.
- A frequência da repetição, os tempos dos pulsos e os pinos devem ser verificados antes de um firmware compilável.
- O mapeamento histórico **não deve substituir** o mapeamento físico experimental atual.

**Sem regravação de placa e sem alegar que o código-fonte original foi recuperado.**