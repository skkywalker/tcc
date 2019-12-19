#include <MultiStepper.h>
#include <AccelStepper.h>
#include <ESP8266WiFi.h>
 
//#define SendKey 0  //Button to send data Flash BTN on NodeMCU

const int dirPinl = 13; // D7
const int stepPinl = 12; // D6
const int dirPinr = 2; //D4
const int stepPinr = 16; //D0
 
int port = 8888;
WiFiServer server(port);

AccelStepper left = AccelStepper(1, stepPinl, dirPinl);
AccelStepper right = AccelStepper(1, stepPinr, dirPinr);
 
//Server connect to WiFi Network
const char *ssid = "Espanha";
const char *password = "02rafaluca03";

char buf[6];

float left_rps = 0.0;
float right_rps = 0.0;

void setup() 
{
  Serial.begin(115200);
  left.setMaxSpeed(600);
  right.setMaxSpeed(600);
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
          
      if(client.available()>=6){
        // read data from the connected client
        for (int i=0; i<6; i++) {
          buf[i] = client.read();
        }
        
        left_rps = (buf[0] - '0') + 0.1*(buf[1] - '0') + 0.01*(buf[2] - '0');
        right_rps = (buf[3] - '0') + 0.1*(buf[4] - '0') + 0.01*(buf[5] - '0');
        
        Serial.print("Left PPS: ");
        Serial.println(int(left_rps*200));
        left.setSpeed(int(left_rps*200));
        Serial.print("Right PPS: ");
        Serial.println(int(right_rps*200));
        right.setSpeed(int(right_rps*200));
        client.write("okay");
        client.stop();
        Serial.println("Client disconnected");
      }
    }
    
  }
}
