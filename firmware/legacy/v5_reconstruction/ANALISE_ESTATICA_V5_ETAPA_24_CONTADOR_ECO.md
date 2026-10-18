# Etapa 24 — Retorno do contador de eco: revisão crítica

**Progresso estimado: 65% (parcial, sem validação física).**

Análise do disassembly AVR original:

- `0x0870–0x08F8`: rotina de leitura de pulso conta iterações em quatro registradores (`r12:r15`); devolve zero em timeout.
- `0x0B4E–0x0B58`: argumento limite `15000`.
- `0x0B5C–0x0B64`: testa retorno nulo.
- **`0x0B66–0x0B6E`: incrementa o retorno em 1 e aplica `andi r25, 0x0F`**. Isso corresponde a `(contador + 1) & 0x0FFFFFFF`, sob convenção AVR de 32 bits. Não é uma conversão demonstrada para microssegundos.
- `0x0B70–0x0B78`: testa novamente zero; se não nulo, converte em float e multiplica por 0,034 e 0,5.

**Conclusão:** a fórmula aritmética no V5 está bem identificada, mas chamar a entrada de `duracao_us` sem comprovação é uma simplificação inadequada. O V5 pode estar usando contagem de loops diretamente como duração. Não afirmar distância calibrada.

## Evidência sobre timeout

O limite 15000 é passado para a rotina que faz três esperas e incrementa um contador. Sem identificar o clock e a duração de cada iteração, **15000 não pode ser rotulado de 15000 µs**.

## Próximo passo

Verificar a semântica da rotina `0x0118` (trigger) e do mapeamento de pinos; criar simulador que receba o retorno *bruto* e reproduza exatamente a transformação `+1`, máscara e multiplicação, deixando clara a incerteza dimensional.