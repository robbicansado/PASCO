# Etapa 16 — Temporização e ultrassom no V5 histórico

**Fonte:** disassembly original `PASCO.zip`. Não houve ensaio de hardware.

## Trechos relevantes

- `0x0B06`: inicia contador em 5, compatível com cinco tentativas ultrassônicas.
- `0x0B10–0x0B30`: alterna nível do pino com chamadas a `0x0118` e loops curtos, compatíveis com trigger de sensor ultrassônico. **Não** atribuir tempos exatos aos loops sem conhecer F_CPU e desvio de compilação.
- `0x0B4E–0x0B58`: carrega limite de espera `0x00003A98` = 15000 e chama `0x0870`. O padrão de `0x0870` é compatível com medição de pulso, mas a unidade e semântica do limite precisam ser confirmadas.
- `0x0B5C–0x0B78`: verifica retorno diferente de zero e, quando válido, incrementa a contagem.
- `0x0B8C–0x0BA4`: usa constantes float 0,034 e 0,5 em multiplicações. Cálculo candidato: `distancia_cm = duracao_us * 0.034 * 0.5`, **condicionado à confirmação de microssegundos**.
- `0x0BB0–0x0BBC`: chama `0x0254` com argumento 5 (compatível com `delay(5)`).
- `0x0BC6–0x0C4A`: ordena amostras válidas e escolhe elemento de índice `n/2` (para n par, elemento superior central, não média dos dois).
- `0x0C66–0x0C70`: chama `0x0254` com argumento 50 (compatível com `delay(50)`) após imprimir distância.
- `0x0C8C`: imprime mensagem alternativa `Ultrassom -> D(cm): 0.0` quando não há amostra válida.

## Notas

O tempo total por ciclo não é simplesmente 122+25+50 ms: inclui leitura ADC, ordenações, transmissão serial, cinco medições com espera e possíveis timeouts. O V5 não estabelece pinagem confiável para o PASCO atual.