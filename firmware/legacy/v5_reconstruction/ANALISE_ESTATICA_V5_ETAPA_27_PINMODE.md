# Etapa 27 — Configuração de pinos

Progresso estimado: 70%. Fonte: disassembly V5.

Em 0x09EA–0x09FE, a aplicação chama 0x01A8 com os pares (11,1), (10,0) e (14,0). A função acessa tabelas de pinos na memória flash, localiza registradores de direção e modifica seus bits preservando o estado das interrupções. Isso sustenta a identificação como função equivalente a pinMode.

Interpretação histórica sob Arduino AVR: D11 OUTPUT, D10 INPUT, A0 INPUT. Não reutilizar como pinagem validada do PASCO atual.

Sem testes físicos ou gravação no Arduino.