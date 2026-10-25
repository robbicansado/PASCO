#include "Arduino.h"
#include <cassert>
#include <cmath>
#include <iostream>
#include <vector>
SerialMock Serial;
static std::vector<int> samples;
static std::vector<unsigned long> pulses;
static size_t adcPos=0,pulsePos=0;
static unsigned long delaysMs=0;
static int trigHigh=0;
int analogRead(uint8_t pin){assert(pin==A0&&adcPos<samples.size());return samples[adcPos++];}
void pinMode(uint8_t,uint8_t){}
void digitalWrite(uint8_t pin,uint8_t value){if(pin==11&&value==HIGH)++trigHigh;}
void delay(unsigned long n){delaysMs+=n;}
void delayMicroseconds(unsigned int){}
unsigned long pulseIn(uint8_t pin,uint8_t state,unsigned long timeout){
 assert(pin==10&&state==HIGH&&timeout==15000&&pulsePos<pulses.size());
 return pulses[pulsePos++];
}
#include "PASCO_V5_experimental.ino"
int main(){
 setup();assert(Serial.baud==9600);Serial.buffer.clear();
 samples.assign(61,512);samples[0]=0;samples[60]=1023;adcPos=0;
 pulses={1000,0,2000,3000,4000};pulsePos=0;loop();
 assert(adcPos==61&&pulsePos==5&&trigHigh==5);
 assert(delaysMs==197);
 assert(Serial.buffer.find("Meteo -> T(C): ")==0);
 assert(Serial.buffer.find("Ultrassom -> D(cm): 51.00\n")!=std::string::npos);
 Serial.buffer.clear();samples.assign(61,0);adcPos=0;pulses.assign(5,0);pulsePos=0;
 loop();
 assert(Serial.buffer=="Meteo -> T(C): 8.00\nUltrassom -> D(cm): 0.0\n");
 assert(trigHigh==10);
 std::cout<<"PASS: serial 9600, ADC median, echo median, timeouts, timing requests, output protocol\n";
}