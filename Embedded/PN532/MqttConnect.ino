
#include <Arduino.h>
#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <TimeLib.h>
#include "AsyncWait.h"
#include "globals.h"
#include <ArduinoJson.h>
#include "FunctionHandler.h"

SetupWifi setupWifi(
    STASSID, STAPSK
);

const char* mqtt_server = MQTT_SERVER;
std::function<void(String&, String&)> mqttCallback = nullptr;
bool isConnected = false;

static PubSubClient pubsubClient(setupWifi.getWiFiClient());

// Handle incomming messages from the broker
void callback(char* topic, byte* payload, unsigned int length) {
    String topicStr;
    String payloadStr;

    for (int i = 0; topic[i]; i++) {
        topicStr += topic[i];
    }

    for (unsigned int i = 0; i < length; i++) {
        payloadStr += (char)payload[i];
    }

    Serial.println("");
    Serial.println("Message arrived - [");
    Serial.print(topicStr);
    Serial.print("] ");
    Serial.println(payloadStr);
    mqttCallback(topicStr, payloadStr);
}
void callbackFromHost(String &topicStr, String &payloadStr) {
  // Create routines for your topic callbacks 
  // if (topicStr == topic_from_host) {
  //       mqttCallback(topicStr, payloadStr);
  // } 
  // Check if the received message matches the expected format
  // if (payloadStr.indexOf("\"status\": \"FAILED\"") != -1) {
  //   // Blink both LEDs
  //   digitalWrite(ledPinAck, LOW);
  //   digitalWrite(ledPinNak, HIGH);
  //   delay(500);
  // }
  // if (payloadStr.indexOf("\"status\": \"SUCCESS\"") != -1) {
  //   // Blink both LEDs
  //   digitalWrite(ledPinAck, HIGH);
  //   digitalWrite(ledPinNak, LOW);
  //   delay(500);
  // } 
  Serial.println("Handling on the default handler, need a check to control this behaiour");
}
void authCallBack(String &topicStr, String &payloadStr) {

}


void publishMessage(String message, char* topic) {
  // Convert the message to a char array
  const char* messageArray = message.c_str();
  unsigned int messageLength = message.length();
  pubsubClient.publish(topic, (uint8_t*)messageArray, messageLength);
}
void publishMessage(String message) {
  // Convert the message to a char array
  const char* messageArray = message.c_str();
  unsigned int messageLength = message.length();
  Serial.println("TOPIC TO HOST: ");
  Serial.print(topic_to_host);
  pubsubClient.publish(topic_to_host, (uint8_t*)messageArray, messageLength);
}
void publishMessage(JsonObject data) {
  DynamicJsonDocument jsonDoc(256); 
  jsonDoc["data"] = data;
  String jsonString;
  serializeJson(jsonDoc, jsonString);
  publishMessage(jsonString);
}

void publishMessage(JsonObject data, char* topic) {
  DynamicJsonDocument jsonDoc(256); 
  jsonDoc["data"] = data;
  String jsonString;
  serializeJson(jsonDoc, jsonString);
  publishMessage(jsonString, topic);
}
void publishActivity(String action, JsonObject& metaData) {
   DynamicJsonDocument jsonDoc(256); // Adjust the size according to your JSON payload
  JsonObject data = jsonDoc.createNestedObject("data");
  data["name"] = THINGNAME;
  data["action"] = action;
  // Check if metaData is empty
  if (!metaData.isNull()) {
    JsonObject appendedMetaData = data.createNestedObject("meta_data");
    appendedMetaData = metaData;
  }
  data["meta_data"]["timestamp"] =  time(nullptr);
  publishMessage(data, topic_client_connection);
}
void publishActivity(String action) {
  DynamicJsonDocument jsonDoc(256); // Adjust the size according to your JSON payload
  JsonObject data = jsonDoc.createNestedObject("data");
  data["name"] = THINGNAME;
  data["action"] = action;
  data["meta_data"]["timestamp"] = time(nullptr);
  publishMessage(data, topic_client_connection);
}
void sendConnectActivity() {
  publishActivity("Connected");
}
// Reconnect to the MQTT client.
void reconnectToMQTT(unsigned long currentMilliSec) {
  // if we are connected nothing further needs to be done.
  if (!pubsubClient.connected()) {
    static AsyncWait waitToRetry;
    if (!waitToRetry.isWaiting(currentMilliSec)) {
      DEBUG_LOG("Attempting MQTT connection...");
      // Attempt to connect
      if (pubsubClient.connect(DEVICE_ID, MQTT_USER, MQTT_PASS)) {
        DEBUG_LOGLN("connected");
        sendConnectActivity();
        pubsubClient.subscribe(topic_from_host);
        DEBUG_LOG("Subcribed to: ");
        DEBUG_LOGLN(topic_from_host);
        
      } else {
        DEBUG_LOGLN(" try again in 5 seconds.");
        waitToRetry.startWaiting(currentMilliSec, 5000);
      } 
    }
    // return;
  }
}


void mqttSetup() {
  setupConfig();
  #ifdef DEBUG
  Serial.begin(115200); // Start serial communication at 115200 baud
  #endif
  setupWifi.setupWifi();
  Serial.println("Got to connecting mqtt");
  pubsubClient.setServer(mqtt_server, 1883);
  if (mqttCallback == nullptr) {
    mqttCallback = callbackFromHost;
  }
  pubsubClient.setCallback(callback); // Initialize the callback routine
}


#ifdef DEBUG
void startupTest(MilliSec currentMilliSec) {
  static AsyncWait startupTestWait;
  static uint8_t startupTestValue;
  static bool firstTime = true;
  static const unsigned turnOnSeconds = 1; // 1 second.
  static const unsigned nextIterationDuration = 1250; // 1,250 milliseconds.

  bool changed = false;

  if (firstTime) {
    firstTime = false;
    startupTestValue = 0;
    changed = zones.turnOn(startupTestValue, turnOnSeconds, currentMilliSec);
    startupTestWait.startWaiting(currentMilliSec, nextIterationDuration);
  }

  if (startupTestValue >= 0 && startupTestValue <= 7) {
    if (!startupTestWait.isWaiting(currentMilliSec)) {
      ++startupTestValue;
      changed = zones.turnOn(startupTestValue, turnOnSeconds, currentMilliSec);
      startupTestWait.startWaiting(currentMilliSec, nextIterationDuration);
    }
  }

  if (changed) {
    Serial.println("Handle something here");
  }
}
#endif // DEBUG


void mqttLoop() {
  setupWifi.loopWifi();
  if (!setupWifi.isReadyForProcessing()) {
      Serial.println("WIFI NOT CONNECTED");
    // The WiFi is not ready yet so
    // don't do any further processing.
    return;
  }
  while(!pubsubClient.connected()) {
      // Reconnect if connection is lost.
      MilliSec currentMilliSec = millis();
      reconnectToMQTT(currentMilliSec);
  }
  
  pubsubClient.loop();

  { // App code.
      MilliSec currentMilliSec = millis();

      #ifdef DEBUG
      startupTest(currentMilliSec);
      #endif

  }
}
