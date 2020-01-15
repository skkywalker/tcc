#include <MultiStepper.h>
#include <AccelStepper.h>
#include <ESP8266WiFi.h>
 
//#define SendKey 0  //Button to send data Flash BTN on NodeMCU

#define MAX_PPS 600
#define PULSES_PER_ROTATION 200

const int dirPinl = 13; // D7
const int stepPinl = 12; // D6
const int dirPinr = 2; //D4
const int stepPinr = 16; //D0
const int sleepPin = 0; //D3
 
int port = 8888;
WiFiServer server(port);

AccelStepper left = AccelStepper(1, stepPinl, dirPinl);
AccelStepper right = AccelStepper(1, stepPinr, dirPinr);
 
//Server connect to WiFi Network
const char *ssid = "Espanha";
const char *password = "02rafaluca03";

unsigned char buf[2];

float left_rps = 0.0;
float right_rps = 0.0;

void setup() 
{
  Serial.begin(115200);
  left.setMaxSpeed(MAX_PPS);
  right.setMaxSpeed(MAX_PPS);
  pinMode(sleepPin, OUTPUT);
  left.setSpeed(0);
  right.setSpeed(0);
  //pinMode(SendKey,INPUT_PULLUP);  //Btn to send data
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
  digitalWrite(sleepPin, LOW);
}


 
void loop() 
{
  WiFiClient client = server.available();
  left.runSpeed();
  right.runSpeed();
  
  if (client) {
    if(client.connected()) Serial.println("Client Connected");

    while(client.connected()){
      left.runSpeed();
      right.runSpeed();
          
      if(client.available()>=2){
        // read data from the connected client
        for (int i=0; i<2; i++) {
          buf[i] = client.read();
        }

        Serial.print("Received message: ");
        Serial.print(buf[0]);
        Serial.print(" ");
        Serial.println(buf[1]);
        
        left_rps = (float)buf[0]/100;
        right_rps = (float)buf[1]/100;

        if(left_rps > 3.0) left_rps = 3.0;
        if(right_rps > 3.0) right_rps = 3.0;

        Serial.print("Left RPS: ");
        Serial.println(left_rps);
        Serial.print("Right RPS: ");
        Serial.println(right_rps);

        if(left_rps > 0 || right_rps > 0) digitalWrite(sleepPin, HIGH);
        else digitalWrite(sleepPin, LOW);

        left.setSpeed(int(left_rps*PULSES_PER_ROTATION));
        right.setSpeed(int(right_rps*PULSES_PER_ROTATION));
        client.stop();
        Serial.println("Client disconnected");
      }
    }
  }
}
