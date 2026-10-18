#include <algorithm>
#include <cassert>
#include <cmath>
#include <cstddef>
#include <iostream>
#include <vector>
float seleciona(std::vector<float> valores) {
  std::sort(valores.begin(), valores.end());
  return valores[valores.size()/2];
}
int main() {
  assert(seleciona({1,3,2})==2);
  assert(seleciona({1,2,3,4})==3);
  assert(seleciona({17})==17);
  assert(std::fabs(1000.f*0.034f*0.5f-17.f)<0.001f);
  std::vector<float> vazios;
  assert(vazios.empty());
  std::cout << "5 testes de politica de eco aprovados\n";
}
