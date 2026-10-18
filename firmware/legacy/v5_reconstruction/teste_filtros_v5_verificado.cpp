#include <cassert>
#include <cmath>
#include <cstddef>
#include <cstdint>
#include <iostream>
#include <algorithm>
float temperatura(uint16_t adc) {return (float(adc)*(5.0f/1023.0f))*10.0f+8.0f;}
float distancia(uint32_t duracao){return float(duracao)*0.034f*0.5f;}
float mediana(float *v,size_t n){std::sort(v,v+n);return v[n/2];}
int main(){
assert(fabs(temperatura(0)-8)<.001);assert(fabs(temperatura(1023)-58)<.001);
assert(fabs(distancia(1000)-17)<.001);
float a[61];for(int i=0;i<61;i++)a[i]=float(60-i);assert(mediana(a,61)==30);
float b[]={8,3,9,4,5};assert(mediana(b,5)==5);
float c[]={4,1,3,2};assert(mediana(c,4)==3);
float d[]={4};assert(mediana(d,1)==4);
std::cout<<"7 testes matematicos aprovados\n";
}
