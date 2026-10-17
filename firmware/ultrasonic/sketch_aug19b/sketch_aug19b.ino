const int TRIG = 7;
const int ECHO = 6;

void setup() {
  Serial.begin(9600);
  pinMode(TRIG, OUTPUT);
  pinMode(ECHO, INPUT);
  digitalWrite(TRIG, LOW);
  Serial.println("HC-SR04 DIRETO NO NANO NOVO");
}

void loop() {
  digitalWrite(TRIG, LOW);
  delayMicroseconds(5);
  digitalWrite(TRIG, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG, LOW);

  unsigned long duracao = pulseIn(ECHO, HIGH, 50000);

  if (duracao == 0) {
    Serial.println("SEM ECHO");
  } else {
    float distancia = duracao * 0.0343 / 2.0;
    Serial.print("ECHO: ");
    Serial.print(duracao);
    Serial.print(" us | DISTANCIA: ");
    Serial.print(distancia, 1);
    Serial.println(" cm");
  }
  delay(500);
}
