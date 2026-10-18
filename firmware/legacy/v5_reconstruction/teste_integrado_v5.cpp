#include <algorithm>
#include <cassert>
#include <cmath>
#include <cstdint>
#include <iostream>
#include <vector>
float temp(uint16_t adc){return (float(adc)*(5.f/1023.f))*10.f+8.f;}
float eco(uint32_t raw){return float((raw+1u)&0x0FFFFFFFu)*0.034f*0.5f;}
float med(std::vector<float> x){std::sort(x.begin(),x.end());return x[x.size()/2];}
int main(){
  std::vector<float> t(61,temp(512));
  assert(std::fabs(med(t)-temp(512))<.001f);
  assert(temp(0)==8.f);
  assert(std::fabs(temp(1023)-58.f)<.001f);
  std::vector<float> e={eco(100),eco(200),eco(300),eco(400)};
  assert(std::fabs(med(e)-eco(300))<.001f);
  assert(eco(0x0FFFFFFFu)==0.f);
  assert(e.size()==4);
  std::cout<<"6 verificacoes integradas aprovadas\n";
}
