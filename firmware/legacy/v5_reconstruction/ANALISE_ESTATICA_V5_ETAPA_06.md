# PASCO — Reconstrução histórica do firmware V5
## Etapa 06 — Separação entre aplicação e possível bootloader

**Fonte analisada:** `PASCO.zip`, arquivos `flexduino_v5_disassembly.txt`, `flexduino_v5_backup.hex` e `flexduino_v5_backup.bin`.

## Evidências diretas

1. No vetor de reset no endereço **0x0000** há `jmp 0x00c4`. Este é o ponto de entrada da aplicação representada na imagem, sob a hipótese de reset pelo vetor padrão.
2. Existe uma segunda tabela de saltos no endereço **0x7800**, iniciada por `jmp 0x7868` e com diversos vetores apontando para `0x78a2`. Isso é típico de uma região de bootloader AVR, mas a função exata depende dos fusíveis e do modelo do microcontrolador.
3. O trecho `0x789a: call 0x7a5a` chama a rotina que escreve nos registradores USART a partir de `0x7a7e` (`UBRR0L=0x10`, `UBRR0H=0`, `UCSR0B=0x18`, `UCSR0C=0x06` se ATmega328P).
4. Logo após, `0x789e: jmp 0x7f98`; em `0x7f98` há `cli` e um loop infinito (`rjmp 0x7f9a`). A chamada `0x789a` é parte de um fluxo de inicialização na região alta, não uma chamada demonstrada a partir do vetor de reset da aplicação.
5. O intervalo de endereço **0x7800–0x7fff** equivale aos 2 KiB superiores de uma flash de 32 KiB. É uma **região compatível** com bootloader em um ATmega328P; isso não prova, isoladamente, que o hardware tenha fusíveis de boot configurados dessa forma.

## Correção interpretativa da etapa 05

O divisor serial **16** encontrado no endereço `0x7a7e` **não pode ser atribuído ao programa de aquisição do PASCO** sem demonstrar que a aplicação o chama. A hipótese mais forte, dada a tabela de vetores em `0x7800`, é que pertença ao bootloader. O valor nominal de baud rate depende do clock e do bit U2X0, ainda não rastreados nesse caminho.

## O que não foi demonstrado

- O microcontrolador exato e os fusíveis de boot.
- O baud rate da aplicação científica.
- Quais pinos e sensores eram realmente usados pelo V5.
- Se todas as strings presentes na imagem são alcançáveis em execução.

## Próximo procedimento técnico

Seguir o vetor de reset da **aplicação** (`0x0000 -> 0x00c4`), localizar a inicialização C/C++ e identificar as escritas de configuração serial **abaixo de `0x7800`**. Separar resultados da engenharia reversa histórica do mapeamento experimental atual do PASCO.

**Segurança:** não gravar firmware nem modificar a placa nesta etapa.