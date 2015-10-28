/*
Code du Projet Panobus
Pour un pano implenté dans le Lycée avec 21 arrets referencés
*/

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

int arret[arret_size];
int incomming=0;
int increment = 0 ;
int leds[arret_size][3];//En attente des adressables
int actual;//Pour les test

void setup(){
  Serial.begin(9600);
  actual = 18;
  leds[actual][0]=11;
  leds[actual][1]=10;
  leds[actual][2]=9;
}
void loop(){
  /*testColor(R_LOIN,G_LOIN,B_LOIN);
  delay(1000);
  testColor(R_APPROCHE,G_APPROCHE,B_APPROCHE);
  delay(1000);
  testColor(R_PROCHE,G_PROCHE,B_PROCHE);
  delay(1000);
  testColor(R_PRET,G_PRET,B_PRET);
  delay(1000);
  testColor(R_LA,G_LA,B_LA);
  delay(1000);*/
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
    }
    arret[increment-1]=incomming-10;
    increment++;
    if(increment-1 == arret_size){
      Serial.println("FIN DE RECEPTION");
      printData();
      increment = 0 ;
    }
  }
}

void printData(){
  for( int i = 0; i <arret_size;i++){
    if(actual==i){
      Serial.print("*");
    }
    if(arret[i]>240){
      Serial.println("BUS LOIN");
      analogWrite(leds[i][0],R_LOIN);
      analogWrite(leds[i][1],G_LOIN);
      analogWrite(leds[i][2],B_LOIN);
    }
    else if(arret[i]>150){
      Serial.println("BUS EN APPROCHE");
      analogWrite(leds[i][0],R_APPROCHE);
      analogWrite(leds[i][1],G_APPROCHE);
      analogWrite(leds[i][2],B_APPROCHE);
    }
    else if(arret[i]>100){
      Serial.println("BUS PROCHE");
      analogWrite(leds[i][0],R_PROCHE);
      analogWrite(leds[i][1],G_PROCHE);
      analogWrite(leds[i][2],B_PROCHE);
    }
    else if(arret[i]>50){
      Serial.println("BUS PRET");
      analogWrite(leds[i][0],R_PRET);
      analogWrite(leds[i][1],G_PRET);
      analogWrite(leds[i][2],B_PRET);
    }
    else if(arret[i]<5){
      Serial.println("BUS LA");
      analogWrite(leds[i][0],R_LA);
      analogWrite(leds[i][1],G_LA);
      analogWrite(leds[i][2],B_LA);
    }
  }

}

void testColor(int r,int g, int b){
  analogWrite(11,r);
  analogWrite(10,g);
  analogWrite(9,b);
  
}
