# PASCO V5 — Etapa 11: especificação para reconstrução da leitura ADC

**Progresso global estimado: 25%.** Este percentual é gerencial, não é a fração de instruções decodificadas.

## O que já é evidência

- O relatório da Etapa 07 localiza em `0x0A1E–0x0A36` escritas nos endereços `0x007C` e `0x007A`, seguidas de espera pelo fim de uma conversão.
- Sob o mapa de registradores do **ATmega328P**, `0x007C` é `ADMUX` e `0x007A` é `ADCSRA`.
- Isso é compatível com o padrão de leitura do ADC interno do Arduino. **Ainda não demonstra** o canal escolhido, a referência de tensão, o valor bruto nem a fórmula de conversão do sensor.
- A Etapa 08 encontrou candidatos a `pinMode(11, OUTPUT)`, `pinMode(10, INPUT)`, `pinMode(14, INPUT)`. Isso não associa automaticamente o ADC a A0: `pinMode(A0, INPUT)` não equivale a `analogRead(A0)` sem rastrear `ADMUX`.

## Modelo didático de aquisição analógica

1. Selecionar a entrada e a referência de tensão em ADMUX.
2. Habilitar e iniciar a conversão em ADCSRA.
3. Aguardar o término.
4. Ler o resultado de 10 bits, usualmente por ADCL/ADCH.
5. Aplicar uma conversão de unidades adequada ao sensor e à calibração.

**Isto é o funcionamento geral do ADC AVR, não código V5 já recuperado.**

## Exemplo de pseudocódigo — não validado

```cpp
// Exemplo conceitual. NÃO representa reconstrução confirmada do V5.
uint16_t lerADC(uint8_t canal) {
  // configurar ADMUX, iniciar conversão, aguardar, ler ADC
  return 0; // placeholder: não usar como firmware
}
```

## Verificações ainda necessárias no disassembly original

1. Copiar literalmente as instruções de `0x0A1E–0x0A60` e identificar a escrita em ADMUX.
2. Verificar o mascaramento dos bits MUX3..0 para deduzir o canal.
3. Verificar bits REFS1:0 para deduzir a referência.
4. Identificar as leituras de `0x0078`/`0x0079` (ADCL/ADCH) ou `0x0078` de 16 bits e as operações posteriores.
5. Rastrear se o valor vai para uma função de formatação, cálculo de temperatura, distância ou outro uso.

## Cautelas

- A pinagem do firmware V5 é **histórica**, anterior ao mapeamento experimental atual.
- O modelo exato do MCU e o caminho de execução completo ainda carecem de confirmação.
- Não inferir `LM35` a partir da mera existência de `analogRead`; o LM35 foi validado em trabalho posterior.
- Não regravar o FlexDuino a partir desta hipótese.

**Resultado desta etapa:** definição de um procedimento auditável para recuperar o ADC; a fórmula científica do V5 permanece desconhecida.