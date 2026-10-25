# Etapa 48 — Ponto de parada sem hardware

**Estado:** concluídas as verificações de software disponíveis nesta rodada; reconstrução lógica estimada em 90%. Ainda não foi possível compilar com a toolchain Arduino AVR.

**Verificado:** formato serial contra leitores históricos, lógica de temperatura e eco, caminhos de timeout, teste integrado de setup e loop com mocks, documentação dos pressupostos de hardware.

**Para prosseguir com segurança:** (1) identificar placa e clock; (2) confirmar fisicamente conexões dos três sensores e tensões; (3) instalar/usar Arduino CLI com core avr e compilar para placa exata; (4) ensaiar em placa de teste ou com plano de recuperação; (5) calibrar e comparar logs com a interface atual.

Nenhuma gravação foi feita. Não declarar o firmware pronto para substituição.