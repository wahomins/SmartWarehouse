
#include <Keypad.h>
#include <Keypad_I2C.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include "secrets.h"
#include <ArduinoJson.h>
#include "SetupWifi.h"
#include "FunctionHandler.h"


#define I2CADDR 0x25 // Set the Address of the PCF8574
#define SCREEN_WIDTH 128 // OLED display width, in pixels
#define SCREEN_HEIGHT 64 // OLED display height, in pixels

int const intrusion_pin = 15;
int const siren_pin=13;
int const buzzer_pin= 14;
char state[] = "DISARMED"; // Disarmed = 0, Armed =1
char input_password[4]; 
char password_Db[] = "1234" ;
char pound_key = '#';
int keyPresses =0;
bool intruder_detected = false;
bool keying_pass = false;
// Declaration for an SSD1306 display connected to I2C (SDA, SCL pins)
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, -1);

unsigned long lastExecutionTime = 0;
unsigned long interval = 4000;  // 7 seconds interval

const byte ROWS = 4; // Set the number of Rows
const byte COLS = 4; // Set the number of Columns

// Set the Key at Use (4x4)
char keys [ROWS] [COLS] = {
  {'1', '2', '3', 'A'},
  {'4', '5', '6', 'B'},
  {'7', '8', '9', 'C'},
  {'*', '0', '#', 'D'}
};

// define active Pin (4x4)
byte rowPins [ROWS] = {0, 1, 2, 3}; // Connect to Keyboard Row Pin
byte colPins [COLS] = {4, 5, 6, 7}; // Connect to Pin column of keypad.

// makeKeymap (keys): Define Keymap
// rowPins:Set Pin to Keyboard Row
// colPins: Set Pin Column of Keypad
// ROWS: Set Number of Rows.
// COLS: Set the number of Columns
// I2CADDR: Set the Address for i2C
// PCF8574: Set the number IC
Keypad_I2C keypad (makeKeymap (keys), rowPins, colPins, ROWS, COLS, I2CADDR, PCF8574);

bool authenticate(){  
  for(int i=0; i<4; i++)
  {
    if(password_Db[i]!= input_password[i]){
    	return false;
    } 
  }
  return true;
}
void printScreen(String text){
  display.fillRect(0, 24, SCREEN_WIDTH, 16, SSD1306_BLACK);
  display.setTextSize(1);
  display.setCursor(0, 24);
  // Display static text
  display.println(text);
  display.display(); 

}
void receiveFromHost(String &topicStr, String &payloadStr) {
  // Create routines for your topic callbacks 
  if (topicStr == topic_from_host) {
    //handle any actions on server receive
  } 
   
  Serial.println("Handling on the default handler");
}

void sendForProcessing(String event, String sev="OK") {
  DynamicJsonDocument jsonDoc(256); // Adjust the size according to your JSON payload
  JsonObject data = jsonDoc.createNestedObject("data");
  data["name"] = THINGNAME;
  data["severity"] = sev;
  data["action"] = event;
  publishMessage(data);
} 
void handleIntrusion(){
  if(strcmp(state,"DISARMED")==0){
    strcpy(state,"ARMED");
    //printOled("ARMED", true, 0, true); 
    Serial.println("ARMED");
   printScreen("ARMED");
   sendForProcessing(state);
   
  }
  else if (strcmp(state,"ARMED")==0){
    if(intruder_detected){
      intruder_detected = false;
    } else {      
      strcpy(state,"DISARMED");     
    }
      digitalWrite(siren_pin, LOW);
      digitalWrite(buzzer_pin, LOW);
      //printOled(state,true, 0, true);
      Serial.println(state);
      printScreen(state);
      sendForProcessing(state); 
  }
  }
void readKey(){
	char key = keypad.getKey();
    if (key){
      Serial.println(key);
      
      String myKey;
      myKey = key;
      bool shld_clear = keyPresses == 0;
      //printOled(myKey, false, keyPresses, shld_clear ? true : false);
      if(key=='#'||keyPresses>3){
      	//Pound Key is pressed, let process 
      
        bool auth = authenticate();
        if(auth){
          keying_pass = false;
        	//printOled("", false, 0, true);
        	handleIntrusion();
        	strcpy(input_password,"");	
        } else {
          	 keying_pass = false;
       		 //printOled("WRONG PASS",false, 0, true);
            printScreen("WRONG PASS");
            sendForProcessing("WRONG PASS", "HIGH");
            Serial.println("WRONG PASS");
        	 strcpy(input_password,"");
      	}
      	keyPresses=0;
      }
      else{
        keying_pass = true;
        input_password[keyPresses]=key;
        Serial.println(input_password);
        printScreen(myKey);
        Serial.println("keyPresses " +keyPresses);
        keyPresses = keyPresses + 1;
      }
     
    }
	// delay(100);
}

void detectIntuder(){

    if(digitalRead(intrusion_pin) == HIGH && strcmp(state,"ARMED")==0){
      unsigned long currentTime = millis();
     // Check if the interval has elapsed since the last execution
      if (currentTime - lastExecutionTime >= interval) {
        lastExecutionTime = currentTime;  // Update the last execution time
        sendForProcessing("Intruder Detected!", "CRITICAL");
      }
      digitalWrite(siren_pin, HIGH);
      digitalWrite(buzzer_pin, HIGH);
      if(!keying_pass) Serial.println("INTRUDER !!"); 
      intruder_detected = true;
      printScreen("Intruder!");
  	}
}

void setup () {
  Wire .begin (); // Call the connection Wire
  keypad.begin (makeKeymap (keys)); // Call the connection
  Serial.begin (9600);
  pinMode(intrusion_pin, INPUT);
  pinMode(siren_pin, OUTPUT);
  pinMode(buzzer_pin, OUTPUT);
  	//printOled(state, true);
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
  display.println("Intrusion System");
  display.setTextSize(1);
  display.println("Enter Password");  
  display.display(); 
  
  mqttCallback = receiveFromHost;
  mqttSetup();
}

void loop () {
  mqttLoop();
  readKey(); 
  detectIntuder();
}