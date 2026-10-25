# Etapa 42 — Sketch experimental integrado

Progresso estimado: 90% de reconstrução lógica, não validação física.

Arquivo `PASCO_V5_experimental.ino`: integra 61 leituras de A0, fórmula de temperatura candidata, mediana, cinco tentativas de eco, mediana superior e saída serial nominal 9600. Os pinos D11, D10 e A0 são históricos. **Não carregar no PASCO atual sem checar os circuitos.**

O pulso de trigger usa `delayMicroseconds(2)` e `delayMicroseconds(10)` como aproximação Arduino. A rotina de medição usa `pulseIn`, não é transcrição byte a byte do V5. Não se deve declarar equivalência temporal comprovada. O offset +8 °C e o fator 0,034 são históricos e não calibração atual.