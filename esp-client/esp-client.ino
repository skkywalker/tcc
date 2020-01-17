#include <MultiStepper.h>
#include <AccelStepper.h>
#include <ESP8266WiFi.h>
 
#define MAX_PPS 600
#define PULSES_PER_ROTATION 200

/* Setup dos pinos para controle dos motores */
const int dirPinl = 13;   // D7
const int stepPinl = 12;  // D6
const int dirPinr = 2;    // D4
const int stepPinr = 16;  // D0

const int sleepPin = 0;   // D3
 
/* Definicao do servidor */
int port = 8888;
WiFiServer server(port);
const char *ssid = "ap-tcc";
const char *password = "<senha>";

/* Variaveis do motor - comunicacao */
AccelStepper left = AccelStepper(1, stepPinl, dirPinl);
AccelStepper right = AccelStepper(1, stepPinr, dirPinr);
 
unsigned char buf[2];
float left_rps = 0.0;
float right_rps = 0.0;

void setup() 
{
  Serial.begin(115200);

  left.setMaxSpeed(MAX_PPS);
  right.setMaxSpeed(MAX_PPS);
  
  left.setSpeed(0);
  right.setSpeed(0);
 
  Serial.println("Criando Access Point ....");
  WiFi.softAP(ssid, password);
  Serial.println("AP sucesso!");
  IPAddress IP = WiFi.softAPIP();
  Serial.print("AP IP address: ");
  Serial.println(IP);

  server.begin();
  Serial.print("Server ready on port: ");
  Serial.println(port);

  pinMode(sleepPin, OUTPUT);
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
        for (int i=0; i<2; i++) {
          buf[i] = client.read();
        }

        Serial.print("Bytes recebidos: ");
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
