# Etapa 35 — Auditoria estática de 15 invariantes

**Progresso global estimado: 75%.** Script: `auditoria_disassembly_v5.py`.

Foi executado localmente sobre `PASCO/flexduino_v5_disassembly.txt`, codificado em UTF-16, extraído do ZIP original.

**Resultado:** `15 invariantes` aprovadas, incluindo prescaler ADC, ADEN, seleção ADC0, leitura ADCL/ADCH, 61 floats, mediana, registros seriais candidatos, limite de eco, máscara e laço de amostragem.

**Importante:** invariantes de instrução confirmam os bytes desmontados, não o significado de todos os ponteiros nem a calibração física. Não houve gravação de firmware ou ensaio com sensores.

Próximos bloqueios: resolver ponteiros de USART, frequência do clock, escala temporal do eco e validação em bancada.