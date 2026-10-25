# Etapa 47 — Revisão de riscos da reconstrução

**Progresso estimado: 90% da reconstrução lógica, mantido.**

A análise de integração mostra que ainda não há evidência para aumentar o percentual de prontidão do firmware. Há riscos conhecidos:

1. D11, D10 e A0 são pinagem histórica, não a pinagem verificada da montagem atual.
2. O offset de +8 graus é histórico e não deve ser tratado como calibração do LM35 atual.
3. `pulseIn(...,15000)` e o trigger com 2/10 microssegundos são uma aproximação de alto nível, não reprodução binária idêntica.
4. As mensagens são compatíveis com leitores históricos, mas não se conhece a totalidade das interfaces atuais.
5. A ausência de eco imprime 0.0 no legado; uma interface moderna deve diferenciá-la de medida física zero.
6. Nenhum compilador AVR está disponível no ambiente de teste desta rodada.

**Recomendação:** preservar o firmware funcional e usar a reconstrução apenas como referência, até validar pinagem e hardware.