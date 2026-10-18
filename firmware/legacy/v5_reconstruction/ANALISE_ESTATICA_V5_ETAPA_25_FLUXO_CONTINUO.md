# Etapa 25 — Fluxo do laço principal e caminho de falha

**Progresso estimado: 65%.** Fonte: disassembly original.

A rotina `0x08FA` inicializa periféricos e em seguida entra no bloco `0x0A1A`, repetido por salto incondicional `0x0C7A: rjmp 0x0A1A`.

Cada volta:
1. Adquire 61 leituras ADC0, aplica transformação float e atraso solicitado de 2 ms por leitura.
2. Ordena e imprime a mediana de temperatura com duas casas decimais.
3. Faz até cinco tentativas de ultrassom, incluindo espera de 5 ms por tentativa.
4. Seleciona o elemento central superior dos ecos válidos ou imprime `Ultrassom -> D(cm): 0.0`.
5. Executa espera solicitada de 50 ms e volta ao início.

**Nota:** o caminho alternativo `0x0C8C–0x0C94` imprime a string de falha e retorna ao atraso de 50 ms. O salto em `0x0C7A` demonstra loop contínuo, mas não garante o tempo de ciclo. A sequência de leituras de eco é uma reconstrução parcial; não está confirmado que as cinco tentativas tenham sempre igual duração.

**Não confundir** a mensagem 0.0 de falha com medida física zero.