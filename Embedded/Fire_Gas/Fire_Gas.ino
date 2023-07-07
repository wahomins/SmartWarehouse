
#include "secrets.h"
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <MQ2.h>
#include <ArduinoJson.h>
#include "SetupWifi.h"
#include "FunctionHandler.h"

#define SCREEN_WIDTH 128 // OLED display width, in pixels
#define SCREEN_HEIGHT 64 // OLED display height, in pixels

// Declaration for an SSD1306 display connected to I2C (SDA, SCL pins)
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, -1);
int Analog_Input = A0;
int lpg, co, smoke;
int siren_pin = 12;
int normal_pin = 13;
int buzzer_pin = 14;
int fan_pin = 15;
MQ2 mq2(Analog_Input);

unsigned long lastExecutionTime = 0;
unsigned long interval = 5000;

void printScreen(String text, int x=0, int y=22){
  display.fillRect(x, y, SCREEN_WIDTH, 16, SSD1306_BLACK);
  display.setTextSize(1);
  display.setCursor(0, 30);
  // Display static text
  display.println(text);
  display.display(); 
}
void printReadings(String text){
  printScreen(text, 0,30);
}
void receiveFromHost(String &topicStr, String &payloadStr) {
  // Create routines for your topic callbacks 
  if (topicStr == topic_from_host) {
    //handle any actions on server receive
  } 
   
}

void sendForProcessing(int reading, String gasType, String severity = "LOW" ) {
  DynamicJsonDocument jsonDoc(256); // Adjust the size according to your JSON payload
  JsonObject data = jsonDoc.createNestedObject("data");
  data["name"] = THINGNAME;
  data["action"] = String(gasType+"_detected");
  data["reading"] = reading;
  data["units"] = "ppm";
  data["severity"] = severity;
  publishMessage(data);
} 
void setup() {
  pinMode(Analog_Input, INPUT);
  pinMode(siren_pin, OUTPUT);
  pinMode(normal_pin, OUTPUT);
  pinMode(buzzer_pin, OUTPUT);
  pinMode(fan_pin, OUTPUT);
  Serial.begin(115200);
  mq2.begin();
  if(!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) { // Address 0x3D for 128x64
    Serial.println(F("SSD1306 allocation failed"));
    for(;;);
  }
  delay(2000);
  display.clearDisplay();

  display.setTextSize(1);
  display.setTextColor(WHITE);
  display.setCursor(0, 0);
  // Display static text
  display.println("FIRE&GAS PANEL");
  display.display(); 
  digitalWrite(buzzer_pin, LOW);
  digitalWrite(normal_pin, LOW);
  digitalWrite(normal_pin, HIGH);

  mqttCallback = receiveFromHost;
  mqttSetup();
}

void handleGasreading(int reading, String gasType ){
  Serial.print(gasType);
  if(reading>0){
    Serial.print(" Reading is:  " );
    Serial.println(reading);
    unsigned long currentTime = millis();
     // Check if the interval has elapsed since the last execution
    String severity = "LOW";
    if(gasType=="SMOKE"){
  //Handle action for smoke
      digitalWrite(normal_pin, LOW);
      digitalWrite(siren_pin, HIGH);
      digitalWrite(buzzer_pin, HIGH);
      if(reading > 2000 && reading < 5000) {
        severity = "HIGH";
      }
      if(reading > 5000) {
        severity = "CRITICAL";
      }
      printScreen("FIRE");
    } else if(gasType=="CO"){
//Handle action for carbon Monoxide
      digitalWrite(normal_pin, LOW);
      digitalWrite(siren_pin, HIGH);
      //digitalWrite(buzzer_pin, HIGH);
      digitalWrite(fan_pin, HIGH);
      printScreen("CARBON MONOXIDE (CO)");
      if(reading > 1000 && reading < 3000) {
        severity = "HIGH";
      }
      if(reading > 50) {
        severity = "CRITICAL";
      }
    } else if(gasType=="LPG"){
        //Handle action for Liquified petroleum gas
        digitalWrite(normal_pin, LOW);
        digitalWrite(siren_pin, HIGH);
      // digitalWrite(buzzer_pin, HIGH);
        digitalWrite(fan_pin, HIGH);
        printScreen("LPG GAS");
        if(reading > 100 && reading < 1000) {
          severity = "HIGH";
        }
        if(reading > 1000) {
          severity = "CRITICAL";
        }
    }
    if (currentTime - lastExecutionTime >= interval) {
      lastExecutionTime = currentTime;  // Update the last execution time
      sendForProcessing(reading, gasType,severity);
      delay(500);
    }
    printReadings(String(gasType + " : " + reading));
  }else{
    printScreen("LEVELS: OK");
    digitalWrite(normal_pin, HIGH);
    digitalWrite(siren_pin, LOW);
    digitalWrite(buzzer_pin, LOW);
  }
}
void readGassensor(){
 float* values= mq2.read(true); //set it false if you don't want to print the values in the Serial
  //lpg = values[0];
  lpg = mq2.readLPG();
  handleGasreading(lpg, "LPG");
  String LPG = String (lpg);
  String CO = String (co);
  String SMOKE = String (smoke);
  //co = values[1];
  co = mq2.readCO();
  handleGasreading(co, "CO");
  //smoke = values[2];
  smoke = mq2.readSmoke();
  handleGasreading(smoke, "SMOKE");
  display.setCursor(0, 24);
  //printScreen("LPG:");
  //printScreen(LPG);
  //printScreen(" CO:");
 // printScreen(CO);
  //display.setCursor(0, 24);
  //SOME TESTS

 // printScreen(SMOKE);
  delay(1000);

}
void loop(){
  mqttLoop();
  readGassensor();
}