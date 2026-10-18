# Etapa 31 — Unidade da medição ultrassônica

Progresso estimado: 70%.

O disassembly mostra que a função 0x0870 incrementa um contador a cada iteração do laço de leitura do pino, em 0x08B2–0x08BC. Ela retorna o contador em 0x08CE–0x08D4 ou zero quando excede o limite. O chamador passa o limite numérico 15000, incrementa o retorno não nulo e aplica uma máscara de 28 bits em 0x0B66–0x0B6E.

Depois o programa converte o número para float e multiplica por 0,034 e 0,5. Essa é a fórmula numérica observada, mas não foi demonstrado que cada contagem equivale a um microssegundo. O texto D(cm) expressa a intenção do firmware, não uma calibração comprovada.

Em uma implementação reconstruída, manter separados contador bruto e distância histórica reportada. Não alterar o firmware funcional nem assumir pinagem histórica.