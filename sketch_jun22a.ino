// ==========================
// PIN TB6600
// ==========================
#define ENA 4
#define DIR 18
#define PUL 19

// ==========================
// LIMIT SWITCH
// ==========================
#define LS_MAJU    35
#define LS_MUNDUR  34

// ==========================
// SETTING MOTOR
// ==========================
int stepDelay = 500;

// Status motor
bool motorRunning = false;

// Debounce
bool lastLSMaju = HIGH;
bool lastLSMundur = HIGH;

unsigned long lastDebounce = 0;
const unsigned long debounceDelay = 100;

void setup() {

  Serial.begin(115200);

  pinMode(ENA, OUTPUT);
  pinMode(DIR, OUTPUT);
  pinMode(PUL, OUTPUT);

  pinMode(LS_MAJU, INPUT);
  pinMode(LS_MUNDUR, INPUT);

  digitalWrite(ENA, LOW);

  Serial.println("=== SISTEM READY ===");
  Serial.println("LS1 = Motor Maju");
  Serial.println("LS2 = Motor Mundur");
}

void loop() {

  bool stateLSMaju = digitalRead(LS_MAJU);
  bool stateLSMundur = digitalRead(LS_MUNDUR);

  // ==========================
  // LIMIT SWITCH MAJU
  // ==========================
  if (lastLSMaju == HIGH &&
      stateLSMaju == LOW &&
      millis() - lastDebounce > debounceDelay) {

    digitalWrite(DIR, HIGH);

    motorRunning = true;

    Serial.println("LS1 Ditekan -> MOTOR MAJU");

    lastDebounce = millis();
  }

  // ==========================
  // LIMIT SWITCH MUNDUR
  // ==========================
  if (lastLSMundur == HIGH &&
      stateLSMundur == LOW &&
      millis() - lastDebounce > debounceDelay) {

    digitalWrite(DIR, LOW);

    motorRunning = true;

    Serial.println("LS2 Ditekan -> MOTOR MUNDUR");

    lastDebounce = millis();
  }

  lastLSMaju = stateLSMaju;
  lastLSMundur = stateLSMundur;

  // ==========================
  // GERAKKAN MOTOR
  // ==========================
  if (motorRunning) {

    digitalWrite(PUL, HIGH);
    delayMicroseconds(stepDelay);

    digitalWrite(PUL, LOW);
    delayMicroseconds(stepDelay);
  }
}