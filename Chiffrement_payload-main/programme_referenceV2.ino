// Carte Intel curie Arduino / Genuino 101
// Ajouter les bibliothèques Ressources -> Ressources Librairies :
// Bibliothèque : Wifi ESP8266 - Arduino
// Bibliothèque : MQTT - Arduino
// Outils -> Inclure une bibliothèque -> Ajouter la bibliothèque .ZIP 

#include <SPI.h>
#include <Countdown.h>
#include <IPStack.h>
#include <MQTTClient.h>
#include <WiFiEsp.h>

#include <stdlib.h>     /* srand, rand */
#include <time.h>       /* time */
// Variables => pins des input et output
const int led_D5 = 13;
const int led_D6 = 12;
const int bouton_S2 = 8;
const int bouton_S3 = 9;
bool ChangeLed_D5=false, ChangeLed_D6=false;
bool Bp_S2 =true, Bp_S3 =true;

WiFiEspClient c;
IPStack ipstack(c);
MQTT::Client<IPStack, Countdown> client = MQTT::Client<IPStack, Countdown>(ipstack);

// Noms des topics
// String subLED  = "isima/G4/LEDs/#";
// String subBP   = "isima/G4/BPs/#";
// String pubBP1  = "isima/G4/BPs/BP1";
// String pubBP2  = "isima/G4/BPs/BP2";
// String pubLED1 = "isima/G4/LEDs/LED1";
// String pubLED2 = "isima/G4/LEDs/LED2";

char subLED[16]="\x24\x12\x1b\x04\x00\x62\x26\x46\x46\x2d\x08\x25\x01\x46\x42";
char subBP[15]="\x24\x12\x1b\x04\x00\x62\x26\x46\x46\x23\x1d\x12\x5d\x4a";
char pubBP1[17]="\x24\x12\x1b\x04\x00\x62\x26\x46\x46\x23\x1d\x12\x5d\x2b\x31\x7c";
char pubBP2[17]="\x24\x12\x1b\x04\x00\x62\x26\x46\x46\x23\x1d\x12\x5d\x2b\x31\x7f";
char pubLED1[19]="\x24\x12\x1b\x04\x00\x62\x26\x46\x46\x2d\x08\x25\x01\x46\x2d\x08\x25\x43";
char pubLED2[19]="\x24\x12\x1b\x04\x00\x62\x26\x46\x46\x2d\x08\x25\x01\x46\x2d\x08\x25\x40";

// char *subLED ="\x24\x12\x1b\x04\x00\x62\x26\x46\x46\x2d\x08\x25\x01\x46\x42"; 
// char  *subBP="\x24\x12\x1b\x04\x00\x62\x26\x46\x46\x23\x1d\x12\x5d\x4a"; 
// char *pubBP1="\x24\x12\x1b\x04\x00\x62\x26\x46\x46\x23\x1d\x12\x5d\x2b\x31\x7c"; 
// char *pubBP2="\x24\x12\x1b\x04\x00\x62\x26\x46\x46\x23\x1d\x12\x5d\x2b\x31\x7f"; 
// char *pubLED1="\x24\x12\x1b\x04\x00\x62\x26\x46\x46\x2d\x08\x25\x01\x46\x2d\x08\x25\x43"; 
// char *pubLED2="\x24\x12\x1b\x04\x00\x62\x26\x46\x46\x2d\x08\x25\x01\x46\x2d\x08\x25\x40"; 

// Broker
const char* broker_ip = "192.168.1.136";
const int broker_port = 1883;
const char* clientID = "GROUPE_4";
const char* username = "G4";
const char* password = "...";

// WIFI
const char* wifiID = "ZZ_HSH";
const char* wifiPSWD = "WIFI_ZZ_F5";



// Fonction de chiffrement message
const char* chiffrement[25];//message de longueur 24 max
const char* key = "Maria";
const int keySize = 5;

char * Xor(char * input, int inputSize, char *key, int keySize, char * output){
  //TODO
  int index_key = 0;
  int i;
  for(i=0; i<inputSize; i++){
    output[i] = (in[i] ^ key[index_key]);
    index_key = (i+1) % keySize;
  }
  output[i] = '\0';
  return output;
}

void incrementer(char *compteur){
  //supposé de taille 3
  int i = 2;
  int continuer = 1;
  while(i>=0 && continuer)
  {
    if(compteur[i] == '9')
    {
      compteur[i] = '0';
      i--;
    }else{
      compteur[i] += 1;
      continuer = 0;
    }
  }
}

void ramdon_char(char number[5]){
  for(int i=0; i<5; i++)
  {
    number[i] = '0' + rand() % 10;
  }
}

void rotate_char(char *msg)
{
  int taille = 0;
  while(msg[taille] != '\0') taille++;

  int decalage =  rand() % taille;
  int i = 0;
  char tmp = msg[decalage];

  while(i!=taille)
  {
    msg[decalage] = msg[ (decalage-1) % taille  ];
    decalage = (decalage+1)%taille;
    tmp = msg[decalage];
    i++;
  }

}

void CallBackBpMsg(MQTT::MessageData& md){
  MQTT::Message &message = md.message;
  MQTTString &topic = md.topicName;

  Serial.print("Message BP arrived: qos ");
  Serial.print(message.qos);
  Serial.print(", retained ");
  Serial.print(message.retained);
  Serial.print(", dup ");
  Serial.print(message.dup);
  Serial.print(", packetid ");
  Serial.println(message.id);
  
  char* topicName = new char[topic.lenstring.len+1]();
  memcpy(topicName,topic.lenstring.data,topic.lenstring.len);
  Serial.print(", topic ");
  Serial.println(topicName);
  
  char* msgPL = new char[message.payloadlen+1]();
  memcpy(msgPL,message.payload,message.payloadlen);


  //Si le message était chiffré :
  /***********************************************************************/
  // Xor(msgPL, message.payloadlen+1, (char*) key, keySize, chiffrement);
  // int i = 0;
  // while(chiffrement[i] != '\0'){
  //   msgPl[i] = chiffrement[i];
  //   i++;
  // }
  /***********************************************************************/
  Serial.print("Payload ");
  Serial.println(msgPL);

 
  
  if(!strncmp(&topic.lenstring.data[topic.lenstring.len-3],"BP1",3)){
    if(!strncmp(msgPL,"ON",2)){
      ChangeLed_D6=true;
    }
  }
  if(!strncmp(&topic.lenstring.data[topic.lenstring.len-3],"BP2",3)){
    if(!strncmp(msgPL,"ON",2)){
      ChangeLed_D5=true;
    }
  }
  delete msgPL;
  delete topicName;
}

void CallBackLedMsg(MQTT::MessageData& md){
  MQTT::Message &message  = md.message;
  MQTTString &topic = md.topicName;
  
  Serial.print("Message LED arrived: qos ");
  Serial.print(message.qos);
  Serial.print(", retained ");
  Serial.print(message.retained);
  Serial.print(", dup ");
  Serial.print(message.dup);
  Serial.print(", packetid ");
  Serial.println(message.id);
  char* topicName = new char[topic.lenstring.len+1]();
  memcpy(topicName,topic.lenstring.data,topic.lenstring.len);
  Serial.print(", topic ");
  Serial.println(topicName);
    char* msgPL = new char[message.payloadlen+1]();
  memcpy(msgPL,message.payload,message.payloadlen);
  Serial.print("Payload ");
  Serial.println(msgPL);
  if (!strncmp(&topic.lenstring.data[topic.lenstring.len-4],"LED1",4)){
    if (!strncmp(msgPL,"ON",2))
      digitalWrite(led_D6,HIGH);
    else
      digitalWrite(led_D6,LOW);
  }      
  if (!strncmp(&topic.lenstring.data[topic.lenstring.len-4],"LED2",4)){
    if (!strncmp(msgPL,"ON",2))
      digitalWrite(led_D5,HIGH);
    else
      digitalWrite(led_D5,LOW);
  }
  delete msgPL;
  delete topicName;
}

void WifiConnect(){
  Serial1.begin(9600);
  while(!Serial1);
    Serial.begin(9600);
  while(!Serial);
  WiFi.init(&Serial1);
  WiFi.begin((char*) wifiID, wifiPSWD);
}

void BrokerConnect(){
  MQTTPacket_connectData configMQTT = MQTTPacket_connectData_initializer;
  
  configMQTT.clientID.cstring = (char*)clientID;
  configMQTT.username.cstring = (char*) username;
  configMQTT.password.cstring = (char*) password;
  configMQTT.willFlag = 0;
  ipstack.connect((char *) broker_ip, broker_port);
  int rc = client.connect(configMQTT);
  if(rc == 0)
    Serial.println("Connected OK");
  else
    Serial.println("Not Connected ERROR");
  client.subscribe(subBP, MQTT::QOS0, CallBackBpMsg); //Xor(subBP, 14,  (char*)key, keySize, (char*)chiffrement)
  client.subscribe(subLED, MQTT::QOS0, CallBackLedMsg); //Xor(subLED, 15, (char*)key, keySize, (char*)chiffrement)
}


void PortsSetup(){
  // initialisation des broches 12 et 13 comme étant des sorties
  pinMode(led_D5, OUTPUT);
  pinMode(led_D6, OUTPUT);
  // initialisation des broches 8 et 9 comme étant des entrées
  pinMode(bouton_S2, INPUT);
  pinMode(bouton_S3, INPUT);
}
void setup() {
  WifiConnect();
  BrokerConnect();
  PortsSetup();
}

void loop() {
  char *numero = "000";
  char random_number[5];
  client.yield(100);
  if (Bp_S2 != digitalRead(bouton_S2)){
    Bp_S2 = !Bp_S2;
    MQTT::Message message;
    message.qos = MQTT::QOS0;
    message.retained = false;
    message.payload = (void *)(Bp_S2?"OFF":"ON");
    message.payloadlen = strlen(Bp_S2?"OFF":"ON");

    //Si l'on souhaite ajouter de l'aléa:
    // ramdon_char(random_number)


    /**** Si l'on souhaite mettre du chiffrement sur le message envoyer par le bouton 1 ***/

    Xor((char*)message.payload, message.payloadlen, (char*)key, keySize,  (char*)chiffrement);

    //ajout d'un compteur dans le message
    int taille = strlen((char*) chiffrement);
    chiffrement[taille] = numero[0];
    chiffrement[taille+1] = numero[1];
    chiffrement[taille+2] = numero[2];
    chiffrement[taille+3] = '\0';

    incrementer(numero);
    
    
    //On insere le nouveau message
    message.payload = (void*) chiffrement;
    message.payloadlen = strlen((char*) chiffrement) + 3;

    /***************************************************************************************/

    client.publish(pubBP1, message);
  }
  if (Bp_S3 != digitalRead(bouton_S3)){
    Bp_S3 = !Bp_S3;
    MQTT::Message message;
    message.qos = MQTT::QOS0;
    message.retained = false;
    message.payload = (void *)(Bp_S3?"OFF":"ON");
    message.payloadlen = strlen(Bp_S3?"OFF":"ON");
    
    client.publish(Xor(pubBP2, 16, (char*)key, keySize, (char*)chiffrement), message); 
  }
  if(ChangeLed_D6){
    MQTT::Message message;
    message.qos = MQTT::QOS0;
    message.retained = true;
    message.payload = (void *)(!digitalRead(led_D6)?"ON":"OFF");
    message.payloadlen = strlen(!digitalRead(led_D6)?"ON":"OFF");
    client.publish(Xor(pubLED1, 18, (char*)key, keySize, (char*)chiffrement), message);  
    ChangeLed_D6=false;
  }
  if(ChangeLed_D5){
    MQTT::Message message;
    message.qos = MQTT::QOS0;
    message.retained = true;
    message.payload = (void *)(!digitalRead(led_D5)?"ON":"OFF");
    message.payloadlen = strlen(!digitalRead(led_D5)?"ON":"OFF");
    client.publish( Xor(pubLED2, 18,(char*) key, keySize, (char*)chiffrement), message); 
    ChangeLed_D5=false;
  }
}
