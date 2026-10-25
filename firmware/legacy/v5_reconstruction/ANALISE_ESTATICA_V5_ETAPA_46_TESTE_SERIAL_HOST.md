# Etapa 46 — Teste end-to-end em host

O arquivo `teste_integracao_serial.cpp` foi compilado com `g++ -std=c++11 -Wall -Wextra -Werror -I.` e executado localmente com um mock de Arduino, incluindo captura do texto enviado à Serial.

**Saída real:** `PASS: serial 9600, ADC median, echo median, timeouts, timing requests, output protocol`.

Casos efetivamente verificados: setup em 9600 baud; 61 leituras com valores extremos; mediana estável; cinco tentativas de eco; descarte de timeout; seleção superior para quatro ecos válidos; texto serial; falha sem eco; chamadas solicitadas de delay totalizando 197 ms por ciclo (sem contar o tempo de pulseIn e ADC). Esse total é apenas soma de delays pedidos, não período real.

Este é um teste C++ de host, **não** compilação com avr-g++ e **não** validação física.