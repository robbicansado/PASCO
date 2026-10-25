# Etapa 40 - Escala temporal do ultrassom

O laco de medicao percorre 16 ciclos AVR por incremento no caminho estavel. Para um processador a 16 MHz, isso representa aproximadamente um microssegundo. O programa incrementa o resultado e aplica mascara de 28 bits, depois multiplica por 0,034 e 0,5.

A interpretacao da distancia em centimetros e consistente, mas depende de clock e calibracao fisica. O timeout de 15000 iteracoes seria da ordem de 15 milissegundos. Nenhuma medicao fisica foi feita. Progresso estimado 85%.