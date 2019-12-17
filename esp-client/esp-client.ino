#include <MultiStepper.h>
#include <AccelStepper.h>

/*
 * Copyright (c) 2018, circuits4you.com
 * All rights reserved.
 * Create a TCP Server on ESP8266 NodeMCU. 
 * TCP Socket Server Send Receive Demo
*/
 
#include <ESP8266WiFi.h>
 
#define SendKey 0  //Button to send data Flash BTN on NodeMCU

const int dirPin = 13;
const int stepPin = 12;
 
int port = 8888;  //Port number
WiFiServer server(port);

AccelStepper stepper = AccelStepper(1, stepPin, dirPin);
 
//Server connect to WiFi Network
const char *ssid = "Espanha";  //Enter your wifi SSID
const char *password = "02rafaluca03";  //Enter your wifi Password

char buf[6];

float left_rps = 0.0;
float right_rps = 0.0;

void setup() 
{
  Serial.begin(115200);
  stepper.setMaxSpeed(600);
  stepper.setSpeed(0);
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


 
void loop() 
{
  WiFiClient client = server.available();
  stepper.runSpeed();
  
  if (client) {
    if(client.connected()) Serial.println("Client Connected");

    while(client.connected()){
      stepper.runSpeed();
          
      if(client.available()>=6){
        // read data from the connected client
        for (int i=0; i<6; i++) {
          buf[i] = client.read();
        }
        
        left_rps = (buf[0] - '0') + 0.1*(buf[1] - '0') + 0.01*(buf[2] - '0');
        right_rps = (buf[3] - '0') + 0.1*(buf[4] - '0') + 0.01*(buf[5] - '0');
        
        Serial.print("Left PPS: ");
        Serial.println(int(left_rps*200));
        stepper.setSpeed(int(left_rps*200));
        Serial.print("Right PPS: ");
        Serial.println(right_rps);
        client.write("okay");
        client.stop();
        Serial.println("Client disconnected");
      }
    }
    
  }
}
