# Etapa 33 — Clock do ADC V5

**Progresso estimado: 75%.** Análise do disassembly original.

Em `0x0954–0x096E`, o programa ativa os bits ADPS2, ADPS1 e ADPS0 de ADCSRA (0x007A). Em `0x0972–0x0978`, ativa ADEN. No ATmega328P, isso seleciona **prescaler 128**.

Sob a hipótese de F_CPU=16 MHz, o clock do ADC é 125 kHz. Uma conversão convencional de 13 ciclos dura aproximadamente **104 microssegundos**; a primeira conversão pode demorar mais. O programa solicita também uma espera de 2 ms por amostra.

Não é medição do clock da placa e não confirma a precisão do sensor.