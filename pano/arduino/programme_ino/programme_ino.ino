/*
Code du Projet Panobus
 Pour un pano implenté dans le Lycée avec 21 arrets referencés
 */

#include <Adafruit_NeoPixel.h>

#define arret_size 21


//DEFINITIONS DES COULEURS A REVOIR SUR LES VRAIES LEDS
#define R5 220//Original 220
#define G5 108//Original 108
#define B5 2//Original 2

#define R7 190//Original 190
#define G7 30//Original 84
#define B7 32//Original 86

#define R8 0//Original 0
#define G8 230//Original 119
#define B8 30//Original 48

#define R12 91//Original 91
#define G12 190//Original 171
#define B12 100//Original 154

#define R_LA 255
#define G_LA 0
#define B_LA 0

#define R_PRET 255
#define G_PRET 50
#define B_PRET 0

#define R_PROCHE 20
#define G_PROCHE 250
#define B_PROCHE 20

#define R_APPROCHE 0
#define G_APPROCHE 200
#define B_APPROCHE 255

#define R_LOIN 0
#define G_LOIN 0
#define B_LOIN 255

Adafruit_NeoPixel tempsAttenteLeds = Adafruit_NeoPixel(21, 6, NEO_GRB + NEO_KHZ800);
Adafruit_NeoPixel arretLeds = Adafruit_NeoPixel(12, 7, NEO_GRB + NEO_KHZ800);


int arret[arret_size];
int incomming=0;
int increment = 0 ;
long lastUpdate;
int compteurTest;

void setup(){
  Serial.begin(9600);

  tempsAttenteLeds.begin();
  arretLeds.begin();

  for(int i=0;i<3;i++){
    arretLeds.setPixelColor(i, arretLeds.Color(R8,G8,B8));
  }
  arretLeds.setPixelColor(3, arretLeds.Color(R12,G12,B12));
  arretLeds.setPixelColor(4, arretLeds.Color(R5,G5,B5));
  arretLeds.setPixelColor(5, arretLeds.Color(R8,G8,B8));
  arretLeds.setPixelColor(6, arretLeds.Color(255,255,255));
  for(int i=7;i<12;i++){
    arretLeds.setPixelColor(i, arretLeds.Color(R7,G7,B7));
  }
}

void loop(){
  if(millis()-lastUpdate>1&&compteurTest<5){
    testLeds();
    Serial.println(compteurTest);
  }
  else if(millis()-lastUpdate>600000 && compteurTest>=5){
    Serial.println(compteurTest);
    for(int i = 0;i<22;i++){
        tempsAttenteLeds.setPixelColor(i, tempsAttenteLeds.Color(0,0,0));
    }
    for(int i = 0;i<12;i++){
        arretLeds.setPixelColor(i, arretLeds.Color(0,0,0));
    }
  }
  getData();
}

void getData(){

  if(Serial.available()>0){
    incomming = Serial.read();
    /*Serial.print("increment: ");
     Serial.print(increment);
     Serial.print(" incomming : ");
     Serial.println(incomming);*/
    if(increment == 0 && incomming != arret_size){
      Serial.print("Erreur ");
      Serial.print(arret_size);
      Serial.print(" ");
      Serial.println(incomming);
      increment=0;
    }
    else if(increment == 0 && incomming == arret_size){
      Serial.println("No erreur");
      digitalWrite(13,HIGH);
      lastUpdate=millis();
    }
    arret[increment-1]=incomming-10;
    increment++;
    if(increment-1 == arret_size){
      Serial.println("FIN DE RECEPTION");
      digitalWrite(13,LOW);
      printData();
      increment = 0 ;
    }
  }
}

void printData(){
  for( int i = 0; i <arret_size;i++){
    if(actual==i||actual+2==i){
      Serial.print("*");
    }
    if(arret[i]>240){
      Serial.println("BUS LOIN");
      tempsAttenteLeds.setPixelColor(i, tempsAttenteLeds.Color(R_LOIN,G_LOIN,B_LOIN));
    }
    else if(arret[i]>150){
      Serial.println("BUS EN APPROCHE");
      tempsAttenteLeds.setPixelColor(i, tempsAttenteLeds.Color(R_APPROCHE,G_APPROCHE,B_APPROCHE));
    }
    else if(arret[i]>100){
      Serial.println("BUS PROCHE");
      tempsAttenteLeds.setPixelColor(i, tempsAttenteLeds.Color(R_PROCHE,G_PROCHE,B_PROCHE));
    }
    else if(arret[i]>50){
      Serial.println("BUS PRET");
      tempsAttenteLeds.setPixelColor(i, tempsAttenteLeds.Color(R_PRET,G_PRET,B_PRET));
    }
    else if(arret[i]<5){
      Serial.println("BUS LA");
      tempsAttenteLeds.setPixelColor(i, tempsAttenteLeds.Color(R_LA,G_LA,B_LA));
    }
  }

}

void testColor(int r,int g, int b){
  analogWrite(11,r);
  analogWrite(10,g);
  analogWrite(9,b);

}

void testLeds(){
  Serial.println("No more data leds test mode");
  for(int i = 0;i<21;i++){
    for(int j = 0;j<255;j++){
      for(int k =0; k <255;k++){
        for(int l =0; l <255;l++){
          tempsAttenteLeds.setPixelColor(i, tempsAttenteLeds.Color(j,k,l));
          delay(10);
        }
      }
    }
  }
  for(int i = 21;i>0;i--){
    for(int j = 255;j>=0;j--){
      for(int k =255; k>=0;k--){
        for(int l =255; l>=0;l--){
          tempsAttenteLeds.setPixelColor(i, tempsAttenteLeds.Color(j,k,l));
          delay(10);
        }
      }
    }
  }
  lastUpdate=millis();
  compteurTest++;

}


