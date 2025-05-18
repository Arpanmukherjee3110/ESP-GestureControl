const int RELAY_PIN = D1; 
const int LED_PIN = D4; 
const int LED1 = D2;   
const int LED2 = D3; 
const int LED3 = D5;

void setup() {
  pinMode(RELAY_PIN, OUTPUT);
  pinMode(LED_PIN, OUTPUT);
  pinMode(LED1, OUTPUT);
  pinMode(LED2, OUTPUT);
  pinMode(LED3, OUTPUT);
  digitalWrite(RELAY_PIN, HIGH); 
  digitalWrite(LED1, LOW);
  digitalWrite(LED2, LOW);
  digitalWrite(LED3, LOW);
  
  Serial.begin(115200);  
  while (!Serial);  
  Serial.println("ESP32 Ready (115200 baud)");
}

void loop() {
  if (Serial.available() > 0) {
    String data = Serial.readStringUntil('\n');
    data.trim();
    
    if (data.length() > 0) {
      int fingerCount = data.toInt();
      
      
      digitalWrite(LED_PIN, HIGH);
      delay(50);
      digitalWrite(LED_PIN, LOW);
      
      

      if (fingerCount == 1) {
        digitalWrite(RELAY_PIN, LOW);
        digitalWrite(LED1, LOW);
        digitalWrite(LED2, LOW);
        digitalWrite(LED3, LOW);
        
      } 
      else if (fingerCount == 2) {
        digitalWrite(RELAY_PIN, HIGH);
        digitalWrite(LED1, HIGH);
        digitalWrite(LED2, LOW);
        digitalWrite(LED3, LOW);
        
      }
      else if (fingerCount == 3) {
        digitalWrite(RELAY_PIN, HIGH);
        digitalWrite(LED2, HIGH);
        digitalWrite(LED1, LOW);
        digitalWrite(LED3, LOW);
        
      }
      else if (fingerCount == 4) {
        digitalWrite(RELAY_PIN, HIGH);
        digitalWrite(LED3, HIGH);
        digitalWrite(LED1, LOW);
        digitalWrite(LED2, LOW);
      }
      else if(fingerCount == 0){
        digitalWrite(RELAY_PIN, HIGH);
        digitalWrite(LED1, LOW);
        digitalWrite(LED2, LOW);
        digitalWrite(LED3, LOW);
      }
    }
  }
  delay(10);
}

// void setup() {
//   Serial.begin(9600); // Must match Python baud rate
// }

// void loop() {
//   if (Serial.available() > 0) {
//     String data = Serial.readStringUntil('\n');
// if (data=="Hello from Python!"){
//   digitalWrite(13, HIGH);
//   delay(400);
//   digitalWrite(13, LOW);
// }
//     Serial.println("Received: " + data); // Optional: send feedback
//   }
// }
