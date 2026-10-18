#include <algorithm>
#include <cassert>
#include <cmath>
#include <cstdint>
#include <iomanip>
#include <iostream>
#include <vector>

float temperatura(uint16_t adc) {
  return (float(adc) * (5.0f / 1023.0f)) * 10.0f + 8.0f;
}
float valor_eco(uint32_t contador_bruto) {
  const uint32_t corrigido = (contador_bruto + 1u) & 0x0FFFFFFFu;
  return float(corrigido) * 0.034f * 0.5f;
}
float elemento_central_superior(std::vector<float> dados) {
  assert(!dados.empty());
  std::sort(dados.begin(), dados.end());
  return dados[dados.size() / 2];
}
struct Ciclo {
  float temperatura_c;
  bool eco_valido;
  float distancia_historica;
};
Ciclo simular(const std::vector<uint16_t>& adc, const std::vector<uint32_t>& ecos) {
  assert(adc.size() == 61 && ecos.size() == 5);
  std::vector<float> t;
  for (uint16_t x : adc) t.push_back(temperatura(x));
  std::vector<float> d;
  for (uint32_t x : ecos) {
    if (x != 0u && ((x + 1u) & 0x0FFFFFFFu) != 0u) d.push_back(valor_eco(x));
  }
  Ciclo out{elemento_central_superior(t), !d.empty(), 0.0f};
  if (!d.empty()) out.distancia_historica = elemento_central_superior(d);
  return out;
}
int main() {
  const std::vector<uint16_t> adc(61, 512);
  const std::vector<uint32_t> ecos{100, 0, 300, 200, 400};
  Ciclo x = simular(adc, ecos);
  assert(std::fabs(x.temperatura_c - temperatura(512)) < 0.001f);
  assert(x.eco_valido);
  assert(std::fabs(x.distancia_historica - valor_eco(300)) < 0.001f);
  Ciclo z = simular(std::vector<uint16_t>(61, 0), std::vector<uint32_t>(5, 0));
  assert(z.temperatura_c == 8.0f && !z.eco_valido);
  assert(std::fabs(temperatura(1023) - 58.0f) < 0.001f);
  assert(std::fabs(valor_eco(0x0FFFFFFFu)) < 0.001f);
  assert(adc.size() == 61 && ecos.size() == 5);
  std::cout << "Simulacao V5: verificacoes integradas aprovadas\n";
  std::cout << std::fixed << std::setprecision(2);
  std::cout << "Meteo -> T(C): " << x.temperatura_c << "\n";
  std::cout << "Ultrassom -> D(candidata): " << x.distancia_historica << "\n";
}
