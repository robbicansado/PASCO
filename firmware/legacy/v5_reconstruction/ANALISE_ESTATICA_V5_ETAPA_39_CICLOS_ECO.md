# Etapa 39 - Temporizacao do eco

O caminho estavel do laco 0x08B2 a 0x08CC executa 16 ciclos AVR por incremento: ld(2), and(1), cp(1), breq tomado(2), ldi(1), sub(1), tres sbc(3), cp(1), tres cpc(3), breq nao tomado(1). Soma 16.

Com clock hipotetico de 16 MHz, cada incremento corresponde aproximadamente a 1 microssegundo. O chamador soma 1 ao contador e aplica mascara de 28 bits. Essa operacao e compativel com a conversao otimizada de pulseIn em Arduino AVR, mas a frequencia da placa nao foi medida.

A formula numerica e contador corrigido multiplicado por 0,034 e por 0,5. Os centimetros dependem da hipotese temporal e de calibracao fisica. Progresso estimado: 85% de entendimento historico; sem firmware gravado.