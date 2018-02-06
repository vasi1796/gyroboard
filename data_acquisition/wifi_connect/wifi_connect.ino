
/*-----------------ESP8266 Serial WiFi Module---------------*/
#define SSID "HomeNet"     // "SSID-WiFiname" 
#define PASS "123@ndrei!"       // "password"
/*-----------------------------------------------------------*/

//Variables
int error;
void setup()
{
  Serial.begin(9600); //or use default 115200.
  
  Serial.println("AT");
  delay(2000);
  //Serial.println("wtf");
  if(Serial.find("OK")){
    connectWiFi();
  }
}

void loop(){
  //Read temperature and humidity values from DHT sensor:
  start: //label 
  error=0;
  //Resend if transmission is not completed 
  if (error==1){
    goto start; //go to label "start"
  }
  
  delay(3600000); //Update every 1 hour
}
 
boolean connectWiFi(){
  Serial.println("AT+CWMODE=1");
  delay(2000);
  String cmd="AT+CWJAP=\"";
  cmd+=SSID;
  cmd+="\",\"";
  cmd+=PASS;
  cmd+="\"";
  Serial.println(cmd);
  delay(5000);
  if(Serial.find("OK")){
    return true;
  }else{
    return false;
  }
}
