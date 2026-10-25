#pragma once
#include <cstdint>
#include <string>
#include <sstream>
#include <iomanip>
#define A0 14
#define OUTPUT 1
#define INPUT 0
#define HIGH 1
#define LOW 0
#define F(x) x
using uint8_t=std::uint8_t;
struct SerialMock {
 std::string buffer; unsigned long baud=0;
 void begin(unsigned long b){baud=b;}
 void print(const char*s){buffer+=s;}
 void println(const char*s){buffer+=s;buffer+='\n';}
 void println(float v,int n){std::ostringstream o;o<<std::fixed<<std::setprecision(n)<<v<<'\n';buffer+=o.str();}
};
extern SerialMock Serial;
int analogRead(uint8_t);
void pinMode(uint8_t,uint8_t);
void digitalWrite(uint8_t,uint8_t);
void delay(unsigned long);
void delayMicroseconds(unsigned int);
unsigned long pulseIn(uint8_t,uint8_t,unsigned long);
