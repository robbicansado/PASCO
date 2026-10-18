# Etapa 18 — Aquisição do eco e limite de espera

**Progresso global estimado: 60%.** Evidência extraída diretamente do disassembly original em `PASCO.zip`.

Em `0x0B4E–0x0B58`, o chamador prepara o limite `0x3A98` = **15000** e chama `0x0870`. Essa rotina consulta repetidamente um registrador de entrada por ponteiro Z, usando uma máscara (`r22`) e nível esperado (`r20`), em três fases: aguardar fim de pulso anterior, início do pulso e fim do pulso medido (`0x088C–0x08CE`). Em timeout, retorna zero (`0x08E4–0x08EA`).

No trecho `0x08B2–0x08D4`, a duração é representada por um contador de iterações. **A unidade de tempo do retorno ainda precisa ser comprovada**; não é correto tratá-lo automaticamente como microssegundos só porque a expressão de distância usa 0,034/2. O comportamento é compatível com uma rotina AVR otimizada do tipo `pulseIn`, mas requer verificação de clock e conversão.

Nenhum teste físico foi feito; a pinagem histórica não deve ser usada como referência para o PASCO atual.