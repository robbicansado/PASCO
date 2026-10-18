# Etapa 26 — Integração simulada da lógica V5

**Progresso estimado: 65%.** Integração lógica, sem firmware gravado.

O arquivo `simulador_v5.cpp` reproduz em computador um ciclo lógico usando 61 amostras ADC e cinco contadores de eco. Faz a transformação de temperatura histórica, seleciona a mediana, descarta ecos nulos, aplica ao contador de eco a operação `(n+1)&0x0FFFFFFF` e seleciona o elemento central superior dos valores válidos.

**Advertência:** a transformação de eco ainda não foi calibrada em unidades de tempo. O programa apresenta a distância como **candidata histórica**, não centímetros comprovados.

Foi também criado e executado localmente `teste_integrado_v5.cpp`, com seis verificações matemáticas aprovadas usando g++ C++11. Esses testes não garantem que o simulador e o firmware original sejam equivalentes em todos os casos.

Pendências: pinagem, clock, tempos do trigger, comunicação serial, confirmação de unidade do eco e teste de bancada. Os backups originais não foram modificados.