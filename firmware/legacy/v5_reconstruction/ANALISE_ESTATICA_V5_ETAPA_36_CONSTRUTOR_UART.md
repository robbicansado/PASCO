# Etapa 36 — Ponteiros da UART identificados

Progresso estimado: 80% de compreensão histórica.

A tabela de construtores em 0x00C2 contém a palavra 0x064B, que aponta para a função no endereço de byte 0x0C96. Essa função inicializa um objeto em SRAM 0x0291 e configura seus ponteiros de registradores.

Mapa comprovado no disassembly entre 0x0CB6 e 0x0CE4:

- SRAM 0x029D aponta para 0x00C5 (UBRR0H).
- SRAM 0x029F aponta para 0x00C4 (UBRR0L).
- SRAM 0x02A1 aponta para 0x00C0 (UCSR0A).
- SRAM 0x02A3 aponta para 0x00C1 (UCSR0B).
- SRAM 0x02A5 aponta para 0x00C2 (UCSR0C).
- SRAM 0x02A7 aponta para 0x00C6 (UDR0).

Assim, os acessos indiretos da aplicação em 0x0980–0x09E8 passam a ter destinos comprovados. A identificação dos nomes de registradores pressupõe o mapa ATmega328P. Não foi feita gravação nem alteração de hardware.