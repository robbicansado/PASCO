# Etapa 20 — Testes locais reproduzíveis

**Progresso global estimado: 60%.** O arquivo `teste_filtros_v5_verificado.cpp` contém sete testes matemáticos independentes, sem Arduino.

Compilação executada em ambiente Linux com:

```sh
g++ -std=c++11 -Wall -Wextra -Werror teste_filtros_v5_verificado.cpp -o teste
./teste
```

**Saída observada:** `7 testes matematicos aprovados`.

Os casos cobrem ADC 0 e 1023, conversão candidata de eco 1000 -> 17 cm, mediana de 61 temperaturas, seleção central de 5 e 4 ecos e caso de 1 eco.

**Limites:** testes de lógica isolada; não validam pinagem, aquisição elétrica, velocidade serial, frequência do clock, conversão de tempo de pulso, nem equivalência com o binário original. O teste foi executado localmente, não no microcontrolador.

**Próximas ações:** fechar a unidade da rotina `0x0870`, confirmar `0x0118` e `0x0254`, depois preparar firmware experimental isolado para validação sem alterar o V5 preservado.