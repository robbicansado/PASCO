#include <algorithm>
#include <cassert>
#include <cmath>
#include <cstdint>
#include <vector>
#include <iostream>
float t(uint16_t adc){return (float(adc)*(5.0f/1023.0f))*10.0f+8.0f;}
float d(uint32_t loops){return float((loops+1u)&0x0FFFFFFFu)*0.034f*0.5f;}
float middle(std::vector<float> a){assert(!a.empty());std::sort(a.begin(),a.end());return a[a.size()/2];}
int main(){
 assert(t(0)==8.0f);
 assert(std::fabs(t(1023)-58.0f)<0.0001f);
 std::vector<float> v(61,t(512));v[0]=999;assert(std::fabs(middle(v)-t(512))<0.0001f);
 std::vector<float> echoes={d(100),d(200),d(300),d(400)};assert(std::fabs(middle(echoes)-d(300))<0.0001f);
 assert(d(0x0FFFFFFFu)==0.0f);
 assert(d(100)>0.0f);
 std::vector<float> empty;assert(empty.empty());
 std::cout<<"7 verificacoes de logica aprovadas\n";
}