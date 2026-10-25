# Etapa 45 — Compatibilidade com os leitores históricos

Inspecionado o backup original `PASCO.zip`. Os arquivos `PASCO/leitor_meteo_v10.py` e `PASCO/leitor_lm35_calibrado_v1.py` abrem serial em **9600 baud** e identificam linhas contendo `Meteo -> T(C):`, extraindo o número depois do último caractere `:`.

O sketch experimental reproduz a etiqueta `Meteo -> T(C): `, duas casas decimais e baud 9600. Também reproduz `Ultrassom -> D(cm): ` e, em caso de ausência de eco, a linha `Ultrassom -> D(cm): 0.0`.

**Compatibilidade demonstrada apenas no nível de formato de linha.** Não há garantia de integração com todos os aplicativos, de estabilidade temporal ou de calibração. O backup `flexduino_v5_recuperado.ino` contém somente `setup` e `loop` vazios: não é a fonte recuperada do V5.