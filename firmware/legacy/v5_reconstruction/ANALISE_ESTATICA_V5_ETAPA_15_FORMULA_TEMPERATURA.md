# Etapa 15 — Reconstrução da conversão de temperatura (V5 histórico)

**Progresso estimado: 55%** após este bloco de investigação (estimativa qualitativa).

## Evidência do disassembly original

Em `0x0A36–0x0A46` são lidos ADCL e ADCH, e o resultado passa pela rotina `0x0F1A` (conversão inteira para float, por comportamento). Em seguida:

- `0x0A4A–0x0A52`: carrega `0x3BA0280A` (float ~0,0048875855 = 5/1023) e chama `0x1084`.
- `0x0A56–0x0A5E`: carrega `0x41200000` (float 10) e chama novamente `0x1084`.
- `0x0A62–0x0A6A`: carrega `0x41000000` (float 8) e chama `0x0CF0`.

O corpo `0x1084` salta à rotina de multiplicação de floats (`0x10AA`), e `0x0CF0` faz ajuste de expoente e usa o núcleo de adição `0x0D20`. Portanto a sequência é consistente com:

```cpp
float temperatura = (float(adc) * (5.0f/1023.0f)) * 10.0f + 8.0f;
```

**Nível de confiança:** alto para as constantes e operações, condicionado à semântica da biblioteca de ponto flutuante AVR. O algoritmo histórico **não deve ser tomado como calibração validada de um LM35** ou de qualquer sensor atualmente conectado.

## Coleta e filtro

- `0x0A12–0x0A86`: 61 amostras armazenadas como floats de 4 bytes, buffer `0x0194` a `0x0287`.
- `0x0A76–0x0A7E`: chama `0x0254` com argumento 2 (compatível com `delay(2)`).
- `0x0A88–0x0ADA`: ordenação dos valores.
- `0x0ADC–0x0AE8`: lê o elemento central em `0x020C` (índice 30), ou seja, mediana de 61.
- `0x0AEC–0x0B04`: imprime `Meteo -> T(C): `, valor com duas casas decimais e CR/LF.

## Limitações

O tempo total depende do ADC, ordenação e comunicação; 61 × 2 ms são somente 122 ms de atrasos solicitados. Não gravar na placa.