const int rows[] = {25, 24, 23, 22}; // GPIO pour les lignes
const int cols[] = {0, 1};   // GPIO pour les colonnes
const char keys[4][2] = {
  {'1', '2'},
  {'3', '4'},
  {'5', '6'},
  {'7', '8'}
};
const int ledPin = 25;       // LED intégrée au Raspberry Pi Pico

void setup() {
  Serial.begin(9600);

  // Configurer la LED intégrée comme sortie
  pinMode(ledPin, OUTPUT);
  digitalWrite(ledPin, LOW); // Éteindre la LED au départ
  
  // Configurer les pins des lignes comme OUTPUT
  for (int i = 0; i < 2; i++) {
    pinMode(rows[i], OUTPUT);
    digitalWrite(rows[i], HIGH); // Les lignes commencent à HIGH
  }
  
  // Configurer les pins des colonnes comme INPUT_PULLUP
  for (int i = 0; i < 2; i++) {
    pinMode(cols[i], INPUT_PULLUP);
  }
}

void loop() {
  for (int r = 0; r < 2; r++) {
    // Activer une ligne à la fois (mettre à LOW)
    digitalWrite(rows[r], LOW);
    
    // Vérifier les colonnes
    for (int c = 0; c < 2; c++) {
      if (digitalRead(cols[c]) == LOW) { // Bouton pressé
        // Allumer la LED intégrée
        digitalWrite(ledPin, HIGH);
        delay(100); // Garder la LED allumée 100 ms
        digitalWrite(ledPin, LOW);
        
        // Afficher le debug dans le port série avec le timer
        Serial.print("Touche pressée : ");
        Serial.print(keys[r][c]);
        Serial.print(" | Timer : ");
        Serial.print(millis());
        Serial.println(" ms");
        
        // Anti-rebond simple
        delay(200);
        while (digitalRead(cols[c]) == LOW); // Attendre que le bouton soit relâché
      }
    }
    
    // Désactiver la ligne (remettre à HIGH)
    digitalWrite(rows[r], HIGH);
  }
}
