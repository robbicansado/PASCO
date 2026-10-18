# Etapa 32 — Critérios para passar da simulação à bancada

**Progresso estimado: 70%.** O sistema ainda não está pronto para gravação.

## Já verificado

- ADC0, 61 amostras e mediana.
- Padrão de cinco tentativas de eco e timeout.
- Fluxo contínuo de execução.
- Mensagens de temperatura e distância.
- Constantes aritméticas e processamento em ponto flutuante.
- 12 invariantes diretamente no disassembly, por script reproduzível.

## Bloqueadores antes de um firmware experimental gravável

1. Resolver a frequência de clock e o tempo de iteração da rotina de pulso.
2. Verificar mapeamento físico real dos pinos no hardware atual, **separado** da pinagem histórica.
3. Confirmar endereços dos registradores USART e baud rate da aplicação.
4. Comparar uma execução simulada com logs históricos, quando disponíveis.
5. Construir sketch experimental **isolado** e revisão de segurança antes de qualquer upload.
6. Validar aquisição real e calibração dos sensores, sem sobrescrever o backup V5.

## Métrica

70% é uma estimativa de entendimento arquitetural e algorítmico, não de código fonte original recuperado. Não aumentar o percentual apenas por produzir documentos ou testes redundantes.