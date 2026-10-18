# PASCO — V5, Etapa 09: rastreamento de mensagens

## Evidência verificada no backup original

O disassembly AVR do `PASCO.zip` contém, na região de aplicação, as instruções:

```asm
0x0A02: ldi r24, 0x1E
0x0A04: ldi r25, 0x01
0x0A06: call 0x04D2
0x0A0A: ldi r24, 0x40
0x0A0C: ldi r25, 0x01
0x0A0E: call 0x04D2
```

O par r25:r24 forma ponteiros SRAM `0x011E` e `0x0140`, **não intervalos de tempo**. A rotina `0x04D2` varre os bytes até o terminador NUL, calcula o comprimento e transfere os dados para `0x02B8`, padrão compatível com impressão serial.

A inicialização em `0x00DC` copia dados da flash a partir de `0x11BC` para a SRAM a partir de `0x0100`. Portanto, os ponteiros `0x011E` e `0x0140` correspondem às posições flash `0x11DA` e `0x11FC`, respectivamente. O binário contém nesses endereços:

- `0x11DA`: `--- FlexDuino Estabilizado V5 ---\0`
- `0x11FC`: `\r\n\0`

Logo, as chamadas em `0x0A06` e `0x0A0E` são compatíveis com imprimir o título do V5 e uma quebra de linha. Isso vincula mensagens históricas a código da aplicação; não é apenas uma busca de strings soltas.

## Limites

- A interpretação pressupõe o modelo AVR observado no disassembly.
- A rotina `0x02B8` ainda precisa ser rastreada até a USART; não se deve atribuir um baud rate.
- A execução efetiva de `0x09EA–0x0A0E` no boot normal requer fechar o grafo de chamadas.
- Nenhum pino histórico deve ser tratado como mapeamento atual.

## Próximas ações

Rastrear `0x02B8` e a inicialização da USART da aplicação; reconstruir em C++ apenas os trechos com evidência; validar em bancada sem sobrescrever firmware funcional.