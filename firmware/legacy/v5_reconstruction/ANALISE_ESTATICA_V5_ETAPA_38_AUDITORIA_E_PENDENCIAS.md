# Etapa 38 — Auditoria independente e pendências

**Progresso global estimado: 80% de compreensão do V5.** Não equivale a 80% de firmware pronto.

Uma auditoria Python foi executada localmente contra o arquivo UTF-16 original do disassembly, confirmando **25 instruções** relacionadas à construção do objeto serial e à configuração da UART, além de verificações de endereçamento e cálculo do baud.

**Saída real:** `AUDITORIA UART: 25 verificacoes de instrucao + enderecamento + baud OK`, `Baud nominal 9600, calculado para 16MHz: 9615.38`.

## Corrigindo um problema dos relatórios anteriores

A configuração serial não é mais apenas uma hipótese de ponteiros: o construtor em `0x0C96` prova os endereços. Entretanto, 9600 baud continua condicionado a 16 MHz, porque não medimos o clock físico.

## Próximas pendências prioritárias

1. Relacionar o contador do eco à duração física de cada iteração, ou marcar a distância como não calibrada.
2. Reconstituir fielmente o fluxo completo e os casos de falha em um sketch experimental isolado.
3. Verificar clock e pinagem da placa real antes de qualquer upload.
4. Comparar saída serial do simulador com registros históricos, se disponíveis.

**Segurança:** não alterar os arquivos `.bin`/`.hex` originais e não carregar firmware na placa funcional sem validação explícita.