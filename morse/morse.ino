#define BUZ 12
#define MORSE 2
#define LED 4

int lastButtonState = 0;
int buttonState = 0;
int lastBounce = 0;

void setup() {
  pinMode(LED, OUTPUT);
  pinMode(MORSE, INPUT);
  noTone(BUZ);
  Serial.begin(9600);
}

void loop() {
  buttonState = digitalRead(MORSE);
  if (buttonState != lastButtonState && millis() - lastBounce > 50) {
    if (buttonState == HIGH) {
      digitalWrite(LED, HIGH);
      tone(BUZ, 440);
      Serial.print(1);
    } else {
      digitalWrite(LED, LOW);
      noTone(BUZ);
      Serial.print(0);
    }
    lastButtonState = buttonState;
    lastBounce = millis();
  }
}
