# Etapas 49–52 — Reexecução independente e correção dos testes

**Progresso estimado: 90% da reconstrução lógica, mantido.** Não houve gravação em hardware.

## Resultado verificável desta rodada

Reexecutei o teste integrado C++ diretamente sobre uma cópia do sketch experimental, usando mock Arduino. Na primeira tentativa a compilação **falhou**: o mock antigo não tinha os campos `baud` e `buffer` que o teste exigia. Portanto, a alegação anterior de teste end-to-end aprovado não estava reproduzível com aqueles arquivos e fica **corrigida**.

Corrigi o mock, separei os testes em `tests/` e executei:

```sh
g++ -std=c++11 -Wall -Wextra -Werror -Itests tests/teste_integracao_serial.cpp -o teste_integracao_serial
./teste_integracao_serial
```

Saída real:

```
PASS: serial 9600, ADC median, echo median, timeouts, timing requests, output protocol
```

Testes exercitam `setup()`, `loop()`, 61 leituras analógicas, mediana, cinco ecos, ausência de eco, saída serial, baud solicitado e delays programados. O total de `197 ms` são **delays solicitados** (61×2 + 5×5 + 50), sem ADC, echo ou overhead.

## Correção de estrutura no GitHub

- Mock Arduino movido para `tests/Arduino.h`, evitando sombrear `Arduino.h` real na compilação Arduino.
- Teste movido para `tests/teste_integracao_serial.cpp`, com caminho relativo para o sketch.
- Removidas as cópias antigas da raiz, que estavam inconsistentes.

## Limite atingido sem hardware neste ambiente

O executável `arduino-cli` e o compilador `avr-g++` não foram encontrados no ambiente. **Não houve compilação para ATmega328P**, logo não afirmo compatibilidade binária AVR.

## Critérios de conclusão

1. Instalar ou usar uma toolchain Arduino AVR confiável e compilar o sketch para a placa exata.
2. Confirmar clock, pinagem e alimentação do PASCO atual.
3. Validar saída serial na interface real e calibrar sensores.
4. Preservar o firmware atual antes de qualquer tentativa de gravação.

**Status:** código integrado e teste host reproduzível; firmware não aprovado para instalação.