# Etapa 23 — Revisão de fidelidade e testes independentes

**Progresso global estimado: 60%.** Nenhuma gravação em Arduino.

## O que já está fundamentado

- ADC0/A0 sob hipótese ATmega328P; 61 amostras, mediana de índice 30.
- Fórmula histórica candidata: `((adc * (5/1023)) * 10) + 8`; exige confirmação física antes de usá-la em sensores atuais.
- Cinco tentativas de eco, descarte de retornos nulos, seleção do central superior para número par.
- Três fases da detecção de pulso e timeout com retorno zero.
- Impressão de temperatura e distância com duas casas decimais.

## Testes locais

O arquivo `teste_politica_ecos.cpp` compila com `g++ -std=c++11 -Wall -Wextra -Werror`. Cinco verificações foram executadas localmente com sucesso: mediana ímpar, central superior par, eco único, fórmula numérica candidata e tratamento separado de lista vazia.

## Questões em aberto

1. Unidade do contador retornado por `0x0870` e interpretação do limite 15000.
2. Exatidão dos pinos históricos e relação com os sensores.
3. Rastrear o construtor USART e confirmar taxa serial da aplicação.
4. Confirmar todos os caminhos do loop e de erros.
5. Montar um firmware experimental **separado** dos backups originais e validar com instrumentação.

Não confundir testes matemáticos em computador com validação do dispositivo físico.