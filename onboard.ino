#include <WiFi.h>
#include <ESPAsyncWebServer.h>
#include <ESP32Servo.h>  // Include ESP32Servo library

// Wi-Fi credentials
const char* ssid = "";
const char* password = "";

// Create an AsyncWebServer object on port 80
AsyncWebServer server(80);

Servo myServo;  // Create a Servo object
const int servoPin = 18;  // Pin connected to the servo

void setup() {
  Serial.begin(115200);

  // Connect to Wi-Fi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");
  Serial.print("IP Address: ");
  Serial.println(WiFi.localIP());

  // Attach the servo to the pin
  myServo.attach(servoPin, 500, 2500);  // Configure the servo with a pulse width range

  // Default servo position
  myServo.write(0);  // Start at 0°

  // Define a POST endpoint to receive data
  server.on("/data", HTTP_POST, [](AsyncWebServerRequest *request) {
    String body;
    if (request->hasParam("body", true)) {
      body = request->getParam("body", true)->value();
      Serial.print("Received: ");
      Serial.println(body);  // Print received data

      // Actuate the servo based on the received data
      if (body == "l") {
        myServo.write(90);  // Move to 90°
        Serial.println("Servo moved to 90°");
      } else if (body == "r") {
        myServo.write(0);  // Move to 0°
        Serial.println("Servo moved to 0°");
      } else {
        Serial.println("Invalid command");
      }

      request->send(200, "text/plain", "Data processed");
    } else {
      request->send(400, "text/plain", "No data received");
    }
  });

  // Start the server
  server.begin();
}

void loop() {
  // Nothing to do here as the server runs asynchronously
}




