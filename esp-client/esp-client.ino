/*
 * Copyright (c) 2018, circuits4you.com
 * All rights reserved.
 * Create a TCP Server on ESP8266 NodeMCU. 
 * TCP Socket Server Send Receive Demo
*/
 
#include <ESP8266WiFi.h>
 
#define SendKey 0  //Button to send data Flash BTN on NodeMCU
 
int port = 8888;  //Port number
WiFiServer server(port);
 
//Server connect to WiFi Network
const char *ssid = "Espanha";  //Enter your wifi SSID
const char *password = "02rafaluca03";  //Enter your wifi Password

char buf[10];
 
int count=0;
//=======================================================================
//                    Power on setup
//=======================================================================
void setup() 
{
  Serial.begin(115200);
  pinMode(SendKey,INPUT_PULLUP);  //Btn to send data
  Serial.println();
 
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password); //Connect to wifi
 
  // Wait for connection  
  Serial.println("Connecting to Wifi");
  while (WiFi.status() != WL_CONNECTED) {   
    delay(500);
    Serial.print(".");
    delay(500);
  }
 
  Serial.println("");
  Serial.print("Connected to ");
  Serial.println(ssid);
 
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());  
  server.begin();
  Serial.print("Open Telnet and connect to IP:");
  Serial.print(WiFi.localIP());
  Serial.print(" on port ");
  Serial.println(port);
}
//=======================================================================
//                    Loop
//=======================================================================
 
void loop() 
{
  WiFiClient client = server.available();
  
  if (client) {
    if(client.connected())
    {
      Serial.println("Client Connected");
    }
    
    while(client.connected()){
          
      if(client.available()>=10){
        // read data from the connected client
        for (int i=0; i<10; i++) {
          buf[i] = client.read();
        }
        Serial.println(buf);
        client.write('1');
        client.stop();
        Serial.println("Client disconnected");
      }
    }
  }
}
