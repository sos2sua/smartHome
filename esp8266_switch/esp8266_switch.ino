
#include <ESP8266WiFi.h>        // Include the Wi-Fi library
#include <ESP8266WiFiMulti.h>   // Include the Wi-Fi-Multi library
#include <ESP8266mDNS.h>        // Include the mDNS library
#include <ESP8266WebServer.h>   // Include the Web server

ESP8266WiFiMulti wifiMulti;     // Create an instance of the ESP8266WiFiMulti class, called 'wifiMulti'
ESP8266WebServer server(80);
MDNSResponder mdns;

int GPIO0=0; 
int GPIO2=2;

void isAlive();
void channel1on();
void channel1off();
void channel2on();
void channel2off();

void setup() {
  Serial.begin(115200);         // Start the Serial communication to send messages to the computer
  delay(10);
  Serial.println('\n');

  pinMode(GPIO0, OUTPUT);
  pinMode(GPIO2, OUTPUT);
  digitalWrite(GPIO0, HIGH);
  digitalWrite(GPIO2, HIGH);

  wifiMulti.addAP("wifi ssid 1", "pass1");   // add Wi-Fi networks you want to connect to
  wifiMulti.addAP("wifi ssid 2", "pass2");
  wifiMulti.addAP("wifi ssid 3", "pass3");

  Serial.println("Connecting ...");
  int i = 0;
  while (wifiMulti.run() != WL_CONNECTED) { // Wait for the Wi-Fi to connect: scan for Wi-Fi networks, and connect to the strongest of the networks above
    delay(1000);
    Serial.print(++i); Serial.print(' ');
  }
  Serial.println('\n');
  Serial.print("Connected to ");
  Serial.println(WiFi.SSID());              // Tell us what network we're connected to
  Serial.print("IP address:\t");
  Serial.println(WiFi.localIP());           // Send the IP address of the ESP8266 to the computer

  if (!mdns.begin("switch1",WiFi.localIP())) {             // Start the mDNS responder for switch1.local
    Serial.println("Error setting up MDNS responder!");
  }
  Serial.println("mDNS responder started");

  server.on("/", isAlive);  //Associate handler function to path
  server.on("/ch1/on", channel1on);
  server.on("/ch1/off", channel1off);
  server.on("/ch2/on", channel2on);
  server.on("/ch2/off", channel2off);

  server.begin(); //Start server
  Serial.println("HTTP server started");
  mdns.addService("http", "tcp", 80);
}

void loop() {
  server.handleClient();
  mdns.update();
}

void isAlive() {
  server.send(200, "text/plain", "Switch1 active");
  Serial.println("Responded to keepalive");
}
void channel1on() {
  server.send(200, "text/plain", "0");
  digitalWrite(GPIO0, LOW);
  Serial.println("Channel1 turned on.");
}
void channel1off() {
  server.send(200, "text/plain", "1");
  digitalWrite(GPIO0, HIGH);
  Serial.println("Channel1 turned off.");
}
void channel2on() {
  server.send(200, "text/plain", "0");
  digitalWrite(GPIO2, LOW);
  Serial.println("Channel2 turned on.");
}
void channel2off() {
  server.send(200, "text/plain", "1");
  digitalWrite(GPIO2, HIGH);
  Serial.println("Channel2 turned off.");
}
