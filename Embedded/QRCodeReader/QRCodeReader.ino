#include <Arduino.h>
#include <ESP32QRCodeReader.h>
#include <ArduinoJson.h>
#include "SetupWifi.h"
#include "FunctionHandler.h"
#include "secrets.h"

ESP32QRCodeReader reader(CAMERA_MODEL_AI_THINKER);

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

void onQrCodeTask(void *pvParameters)
{
  struct QRCodeData qrCodeData;

  while (true)
  {
    if (reader.receiveQrCode(&qrCodeData, 100))
    {
      Serial.println("Found QRCode");
      if (qrCodeData.valid)
      {
        String payloadString((const char *)qrCodeData.payload);

        Serial.print("Payload: ");
        Serial.println(payloadString);
        sendForProcessing(payloadString);
      }
      else
      {
        Serial.print("Invalid: ");
        Serial.println((const char *)qrCodeData.payload);
      }
    }
    vTaskDelay(100 / portTICK_PERIOD_MS);
  }
}

void setup()
{
  Serial.begin(115200);
  Serial.println();

  reader.setup();

  Serial.println("Setup QRCode Reader");

  reader.beginOnCore(1);

  Serial.println("Begin on Core 1");

  xTaskCreate(onQrCodeTask, "onQrCode", 4 * 1024, NULL, 4, NULL);
  
  mqttCallback = receiveFromHost;
  mqttSetup();
}

void loop()
{
  mqttLoop();
  delay(100);
}