//TODO: implement secure credentials as a runtime config file
//      rather than a header file.
#include "secrets.h"
#include <SoftwareSerial.h>
#include <PN532_SWHSU.h>
#include <PN532.h>
#include <ArduinoJson.h>
#include "SetupWifi.h"
#include "FunctionHandler.h"


SoftwareSerial SWSerial( D6, D5 ); // RX, TX

PN532_SWHSU pn532swhsu( SWSerial );
PN532 nfc( pn532swhsu );
String tagId = "None", dispTag = "None";
byte nuidPICC[4];
bool found_reader = false;

const int ledPinAck = D7;
const int ledPinNak = D8;

void initReader() {
  Serial.println("Initializing Reader");
  nfc.begin();
  uint32_t versiondata = nfc.getFirmwareVersion();

  if(!versiondata)
  {
    Serial.print("Didn't Find PN53x Module");
    while (1); // Halt
    // TODO send activity to notify module failure
    if(found_reader) {
      found_reader = false;
    }
  }
  else
  {
    found_reader = true;
      // Got valid data, print it out!
    Serial.print("Found chip PN5");
    // Serial.println((versiondata >> 24) & 0xFF, HEX);
    // Serial.print("Firmware ver. ");
    // Serial.print((versiondata >> 16) & 0xFF, DEC);
    // Serial.print('.'); 
    // Serial.println((versiondata >> 8) & 0xFF, DEC);
    // Configure board to read RFID tags
    nfc.SAMConfig();
  }
}

void handleAuthentication(String &payloadStr) {
  // Check if the received message matches the expected format
    if (payloadStr.indexOf("\"status\": \"FAILED\"") != -1) {
      // Blink both LEDs
      digitalWrite(ledPinAck, LOW);
      digitalWrite(ledPinNak, HIGH);
      delay(500);
    }
    if (payloadStr.indexOf("\"status\": \"SUCCESS\"") != -1) {
      // Blink both LEDs
      digitalWrite(ledPinAck, HIGH);
      digitalWrite(ledPinNak, LOW);
      delay(500);
    }
}
void receiveFromHost(String &topicStr, String &payloadStr) {
  // Create routines for your topic callbacks 
  if (topicStr == topic_from_host) {
        handleAuthentication(payloadStr);
  } 
   
  Serial.println("Handling on the default handler");
}
void sendForProcessing(String cardNumber) {
  DynamicJsonDocument jsonDoc(256); // Adjust the size according to your JSON payload
  JsonObject data = jsonDoc.createNestedObject("data");
  data["name"] = THINGNAME;
  data["action"] = "card_Scan";
  data["card_number"] = cardNumber;
  publishMessage(data);
} 
 
void readNFC() {
  boolean success;
  uint8_t uid[] = { 0, 0, 0, 0, 0, 0, 0 };  // Buffer to store the returned UID
  uint8_t uidLength;                       // Length of the UID (4 or 7 bytes depending on ISO14443A card type)
  success = nfc.readPassiveTargetID(PN532_MIFARE_ISO14443A, &uid[0], &uidLength);
  if (success)
  {
    Serial.print("UID Length: ");
    Serial.print(uidLength, DEC);
    Serial.println(" bytes");
    Serial.print("UID Value: ");
    for (uint8_t i = 0; i < uidLength; i++)
    {
      nuidPICC[i] = uid[i];
      // Serial.print(" "); Serial.print(uid[i], DEC);
    }
    Serial.println();
    tagId = tagToString(nuidPICC);
    dispTag = tagId;
    Serial.print(F("tagId is : "));
    Serial.println(tagId);
    Serial.println("");
    sendForProcessing(tagId);
    delay(1000);  // 1 second halt
  }
  else
  {
    // PN532 probably timed out waiting for a card
    // Serial.println("Timed out! Waiting for a card...");
  }
}
void initialSetup(){
  pinMode(ledPinAck, OUTPUT);
  pinMode(ledPinNak, OUTPUT);
  mqttCallback = receiveFromHost;
  mqttSetup();
  initReader();
}
void setup(void) {
  Serial.begin(115200);
  Serial.println("Hello Maker!");
  //  Serial2.begin(115200, SERIAL_8N1, RXD2, TXD2);
  initialSetup();
}
 
void loop() {
  mqttLoop();
  if(found_reader){
    readNFC();
  }
}
String tagToString(byte id[4]) {
  String tagId = "";
  for (byte i = 0; i < 4; i++)
  {
    if (i < 3) tagId += String(id[i]);
    else tagId += String(id[i]);
  }
  return tagId;
}
