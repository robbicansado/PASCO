# PASCO — Reconstrução histórica do firmware V5 — Etapa 07

Data: 17–18/10/2026. Fonte: `PASCO.zip`, arquivos `flexduino_v5_backup.bin` e `flexduino_v5_disassembly.txt` (UTF-16).

## Evidências verificadas

- Vetor de reset no endereço de byte `0x0000`: `jmp 0x00C4`.
- Inicialização em `0x00C4`: zera R1, inicializa a pilha com `SP=0x08FF`, copia dados inicializados da Flash para RAM e zera a região BSS. Essas operações são típicas do runtime AVR, não são lógica de sensores.
- Após a inicialização, a rotina em `0x08FA` começa com `sei` e configura registradores associados aos temporizadores e ao ADC, sob a hipótese de mapeamento ATmega328P.
- Entre `0x09EA` e `0x09FE` existem chamadas a `0x01A8` com argumentos 11/1, 10/0 e 14/0. A função pode ser uma rotina de configuração de pinos, mas a identificação exata ainda precisa ser confirmada examinando `0x01A8`.
- Entre `0x0A1E` e `0x0A36` aparecem escritas em `0x007C` (ADMUX) e `0x007A` (ADCSRA), seguida de espera pelo fim da conversão. **Evidência forte de uso do ADC** na aplicação, sob o mapeamento ATmega328P.
- As mensagens `--- FlexDuino Estabilizado V5 ---`, `Meteo -> T(C):` e `Ultrassom -> D(cm):` começam, respectivamente, nos offsets `0x11DA`, `0x11FF` e `0x120F` do binário.
- Há bytes diferentes de `0xFF` depois de `0x123C` e antes de `0x7800`, incluindo a string `BME280` em `0x3075`. **Ainda não demonstramos se esses dados são código alcançável, bibliotecas, dados ou resíduos históricos.**
- A região de bootloader começa com tabela de saltos em `0x7800`. A rotina serial em `0x7A7E` pertence a essa região e não determina por si só a velocidade serial da aplicação.

## Interpretação e limites

Este passo identificou inicialização e evidência de aquisição analógica; **não** recuperou o código-fonte V5, nem confirmou a atribuição de pinos aos sensores. O mapeamento posterior do PASCO é a referência para os testes atuais; este firmware é um artefato histórico. O microcontrolador exato e o caminho de execução completo permanecem em verificação.

## Próxima análise concreta

1. Examinar a função `0x01A8` para confirmar se configura direção de pinos.
2. Seguir a função de aquisição que lê ADCL/ADCH e identificar o canal analógico escolhido.
3. Identificar onde a aplicação configura USART, distinguindo-a do bootloader.
4. Produzir pseudocódigo com graus de confiança antes de escrever um firmware novo.

Nenhum código foi gravado na placa e nenhum backup original foi modificado.