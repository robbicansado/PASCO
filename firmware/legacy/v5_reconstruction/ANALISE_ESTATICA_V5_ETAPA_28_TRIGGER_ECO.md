# Etapa 28 — Pulso de disparo e captura de eco

**Progresso estimado: 70%.** Fonte: disassembly V5.

Em `0x0B10–0x0B30`, a aplicação chama `0x0118` três vezes com argumentos 0, 1 e 0, separados por laços curtos. A função `0x0118` usa mapeamento de portas em flash e manipulação de bits de I/O com proteção de interrupções, compatível com escrita digital. A sequência é **LOW → HIGH → LOW**, compatível com trigger ultrassônico.

Em seguida, `0x0B58` chama `0x0870`, rotina de três fases para captura de pulso; retorna zero no timeout. O limite passado é 15000, **sem unidade temporal ainda confirmada**.

Pendente: verificar pinos físicos e a escala temporal a partir do clock. Sem alteração do PASCO atual.