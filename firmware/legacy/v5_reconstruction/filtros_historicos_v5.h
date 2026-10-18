#pragma once
// PASCO V5: reconstrução funcional PARCIAL de filtros estatísticos.
// Código novo baseado em evidências do disassembly; NÃO é o fonte original.
// Sem pinagem, sem leitura de sensores, sem comandos para gravar no Arduino.
#include <stdint.h>
#include <stddef.h>

namespace pasco_v5_historico {

// Ordenação em ordem crescente de floats válidos.
// Na imagem original existe ordenação por comparação/troca;
// esta implementação é independente e não afirma reproduzir cada instrução.
inline void ordenar(float* dados, size_t n) {
  for (size_t i = 1; i < n; ++i) {
    const float valor = dados[i];
    size_t j = i;
    while (j > 0 && dados[j - 1] > valor) {
      dados[j] = dados[j - 1];
      --j;
    }
    dados[j] = valor;
  }
}

// O V5 armazena 61 floats e usa o elemento de índice 30 após ordenar.
inline float mediana_temperatura_61(float (&amostras)[61]) {
  ordenar(amostras, 61);
  return amostras[30];
}

// O V5 tenta até cinco ecos e seleciona o elemento central dos válidos.
// Para contagem par, usa índice n/2; esta é uma reconstrução candidata.
inline bool selecionar_distancia(float* validas, size_t n, float& resultado) {
  if (n == 0 || n > 5) return false;
  ordenar(validas, n);
  resultado = validas[n / 2];
  return true;
}

// Fórmula candidata; duração em microssegundos NÃO verificada no V5.
inline float distancia_candidata_cm(float duracao_us) {
  return duracao_us * 0.034f * 0.5f;
}

} // namespace pasco_v5_historico
