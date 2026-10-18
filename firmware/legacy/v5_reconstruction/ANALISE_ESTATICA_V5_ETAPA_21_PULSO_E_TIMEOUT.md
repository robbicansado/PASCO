# Etapa 21 — Leitura do pulso e timeout

Progresso estimado: 60%. Fonte: disassembly do backup V5 original.

A rotina no endereço `0x0870` examina um registrador de entrada em três fases: espera o término do estado anterior (`0x088C`), espera o começo do estado desejado (`0x08A0`) e conta iterações até o término do pulso (`0x08B2–0x08CC`). Quando o limite é atingido, retorna zero (`0x08E4`). Caso contrário, devolve o contador (`0x08CE`).

O chamador em `0x0B4E–0x0B58` passa um limite numérico de 15000. A unidade temporal exata ainda não foi confirmada; não se deve tratar o contador automaticamente como microssegundos.

Nenhuma alteração de hardware foi realizada. Os pinos V5 são históricos e não substituem a pinagem validada posteriormente.