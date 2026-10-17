// PASCO / FlexDuino — diagnostic optical acquisition (17 Oct 2026)
// Red optical board: A1; blue optical board: A2
// Readings are raw ADC counts (0–1023), NOT lux.
const int OPTICO_1 = A1;
const int OPTICO_2 = A2;
void setup() {
  Serial.begin(9600);
  Serial.println("PASCO | AQUISICAO OPTICA");
}
void loop() {
  int canal1 = analogRead(OPTICO_1);
  int canal2 = analogRead(OPTICO_2);
  Serial.print("A1=");
  Serial.print(canal1);
  Serial.print(";A2=");
  Serial.println(canal2);
  delay(200);
}
