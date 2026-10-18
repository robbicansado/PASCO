# Etapa 17 — Código C++ parcial e validação local

**Progresso global estimado: 55%.** Os testes abaixo validam o **novo código matemático**, não a equivalência binária ao firmware original.

## Arquivos

- `filtros_e_conversoes_v5.h`: implementação independente de conversão ADC, conversão candidata de distância, ordenação e seleção de mediana.
- `teste_filtros_v5.cpp`: sete verificações, compiláveis com g++ C++11.

## Testes realizados localmente

Compilação: `g++ -std=c++11 -Wall -Wextra -Werror teste_filtros_v5.cpp -o teste_filtros_v5`.

Saída: `7 verificacoes aprovadas`.

Casos: ADC 0 -> 8 °C; ADC 1023 -> 58 °C; eco 1000 µs -> 17 cm (hipótese de unidade); mediana de 61 valores; mediana de 5 ecos; seleção central para 4 ecos; rejeição de zero ecos.

## Limitações críticas

- Nenhuma leitura de hardware ou gravação no Nano.
- A fórmula é reconstruída como **comportamento histórico**, não validada fisicamente.
- `0x0870` e `0x0254` ainda precisam de confirmação funcional completa.
- Código-fonte original não foi recuperado; a implementação usa algoritmos independentes.
- Para equivalência do V5, falta reconstituir inicialização, fluxo do loop, temporização e casos de erro.

**Não usar o arquivo como firmware completo nem assumir pinagem histórica como atual.**