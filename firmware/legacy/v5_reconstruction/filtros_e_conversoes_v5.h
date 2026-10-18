#pragma once
#include <stddef.h>
#include <stdint.h>

// Historical V5 reconstruction; NOT original firmware or current pin mapping.
namespace pasco_v5 {
constexpr size_t N_TEMPERATURA = 61;
constexpr size_t MAX_ECOS = 5;
inline float converter_temperatura_c(uint16_t adc) {
  return (float(adc) * (5.0f / 1023.0f)) * 10.0f + 8.0f;
}
inline float converter_distancia_cm(uint32_t duracao_us) {
  return float(duracao_us) * 0.034f * 0.5f;
}
inline void ordenar(float* v, size_t n) {
  for (size_t i=1; i<n; ++i) {
    float x=v[i]; size_t j=i;
    while (j>0 && v[j-1]>x) { v[j]=v[j-1]; --j; }
    v[j]=x;
  }
}
inline float mediana_temperatura(float (&v)[61]) {
  ordenar(v,61);
  return v[30];
}
inline bool mediana_ecos(float* v, size_t n, float& out) {
  if (!v || n==0 || n>5) return false;
  ordenar(v,n);
  out=v[n/2];
  return true;
}
}