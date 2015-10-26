#include <avr/sleep.h> //for die()


#define REQ_LENGTH 21 //require length, don't set it if you want a changing value or I don't know why 

unsigned short int length = -1; //Should be a byte
unsigned short int* buf = NULL;
unsigned short int i = 0; //index counter, ugly, but I can't do otherwise, 
                          //I HATE this system of void main(){setup(); while(1){loop();}} ! I need to keep the hand on every things !!! ;-(
bool completeDataReceive  = false;

void die (); //put arduino to sleep mode, better than exit who just put arduino in a while(1);

void setup() {
    Serial.begin(9600);
}

void getData(){
    //receive data
    if (Serial.available() > 0) { //if receinving data

        if(completeDataReceive || !buf){ //if receiving new data block, set up correct stuff
            if(buf){ //if already allocated, free it (may be call the same times as malloc)
                free(buf);
                buf = NULL;
            }

            completeDataReceive = false; //set it to don't process not complete data
            length = Serial.read(); //length of receiving data

#ifdef REQ_LENGTH
            if(length != REQ_LENGTH){
                die(); //If occur, the is a problem, (bad rpi-side ?)
            }
#endif

            buf = (unsigned short int*) malloc(length);
            return;
        }

        buf[i++] = Serial.read();

        if(i == length){ //if finish to receive data, reset needed stuff
            i = 0;
            completeDataReceive = true;
        }
    }
}


void loop() {
    // /!\ Should fail if the arduino is not connected BEFORE the rpi

    getData();

    //process data
    if(completeDataReceive){
        for(unsigned short int j = 0; j < length; j++){
            Serial.print(buf[j]);
            Serial.print('\n');
            //PROCESS DATA AND SEND TO LEDS
        }
        length = 0;
    }
}

void die(){
    set_sleep_mode( SLEEP_MODE_PWR_DOWN  );
    sleep_enable();
    cli();
    sleep_cpu();
    while(1);
}
