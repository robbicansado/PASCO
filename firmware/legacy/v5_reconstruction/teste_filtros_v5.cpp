#include "filtros_e_conversoes_v5.h"
#include <cassert>
#include <cmath>
#include <iostream>
int main(){
  using namespace pasco_v5;
  assert(std::fabs(converter_temperatura_c(0)-8.0f)<0.001f);
  assert(std::fabs(converter_temperatura_c(1023)-58.0f)<0.001f);
  assert(std::fabs(converter_distancia_cm(1000)-17.0f)<0.001f);
  float a[61];for(int i=0;i<61;i++)a[i]=float(60-i);
  assert(mediana_temperatura(a)==30.0f);
  float b[]={8,3,9,4,5};float out=0;
  assert(mediana_ecos(b,5,out)&&out==5.0f);
  float c[]={4,1,3,2};assert(mediana_ecos(c,4,out)&&out==3.0f);
  assert(!mediana_ecos(c,0,out));
  std::cout<<"7 verificacoes aprovadas\n";
}
