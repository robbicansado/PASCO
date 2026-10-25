/* PASCO V5 experimental reconstruction; NOT original source.
 * Historical candidate wiring: A0 analog, D11 trigger, D10 echo.
 * DO NOT flash before verifying the current hardware wiring and voltage.
 */
#include <Arduino.h>
namespace LegacyV5 {
const uint8_t TEMP_PIN=A0, TRIG_PIN=11, ECHO_PIN=10;
const uint8_t N_TEMP=61, N_ECHO=5;
float temperatures[N_TEMP], distances[N_ECHO];
float legacyTemperature(int adc) {
  return (float(adc)*(5.0f/1023.0f))*10.0f+8.0f;
}
void sortFloats(float *v,uint8_t n) {
  for(uint8_t i=1;i<n;++i) {
    float x=v[i];uint8_t j=i;
    while(j>0&&v[j-1]>x){v[j]=v[j-1];--j;}
    v[j]=x;
  }
}
float temperatureMedian() {
  for(uint8_t i=0;i<N_TEMP;++i){
    temperatures[i]=legacyTemperature(analogRead(TEMP_PIN));
    delay(2);
  }
  sortFloats(temperatures,N_TEMP);
  return temperatures[N_TEMP/2];
}
void trigger() {
  digitalWrite(TRIG_PIN,LOW);delayMicroseconds(2);
  digitalWrite(TRIG_PIN,HIGH);delayMicroseconds(10);
  digitalWrite(TRIG_PIN,LOW);
}
bool distanceMedian(float &cm) {
  uint8_t valid=0;
  for(uint8_t i=0;i<N_ECHO;++i){
    trigger();
    unsigned long us=pulseIn(ECHO_PIN,HIGH,15000UL);
    if(us!=0) distances[valid++]=float(us)*0.034f*0.5f;
    delay(5);
  }
  if(valid==0) return false;
  sortFloats(distances,valid);
  cm=distances[valid/2];
  return true;
}
}
void setup(){
  Serial.begin(9600);
  pinMode(LegacyV5::TRIG_PIN,OUTPUT);
  pinMode(LegacyV5::ECHO_PIN,INPUT);
  pinMode(LegacyV5::TEMP_PIN,INPUT);
  digitalWrite(LegacyV5::TRIG_PIN,LOW);
  Serial.println(F("--- FlexDuino Estabilizado V5 [RECONSTRUCAO EXPERIMENTAL] ---"));
}
void loop(){
  Serial.print(F("Meteo -> T(C): "));
  Serial.println(LegacyV5::temperatureMedian(),2);
  float cm=0;
  if(LegacyV5::distanceMedian(cm)){
    Serial.print(F("Ultrassom -> D(cm): "));
    Serial.println(cm,2);
  } else Serial.println(F("Ultrassom -> D(cm): 0.0"));
  delay(50);
}