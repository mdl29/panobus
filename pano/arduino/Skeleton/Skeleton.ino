#include <avr/sleep.h> //for die()

#define REQ_LENGTH 21 //require length, don't set it if you want a changing value or I don't know why 

void die (); //put arduino to sleep mode, better than exit who just put arduino in a while(1);

void setup() {
    Serial.begin(9600);
}

void loop() {

    byte length; //Should be a byte
    byte* buf = NULL;
    byte i = 0; //index counter, ugly, but I can't do otherwise, 

    // /!\ Should fail if the arduino is not connected BEFORE the rpi
    while(true){ // Block until end of data
        //receive data
        if (Serial.available() > 0) { //if receinving data

            if(!buf){ //if receiving new data block, set up correct stuff
                length = Serial.read(); //length of receiving data

#ifdef REQ_LENGTH
                if(length != REQ_LENGTH){
                    die(); //If occur, the is a problem, (bad rpi-side ?)
                }
#endif

                buf = (byte*) malloc(length);
                continue;
            }

            buf[i++] = Serial.read();

            if(i == length)
                break;
        }
    }

    //process data
    for(i = 0; i < length; i++){
        Serial.print(buf[i]);
        Serial.print('\n');
        //PROCESS DATA AND SEND TO LEDS
    }

    free(buf);
}

void die(){
    set_sleep_mode( SLEEP_MODE_PWR_DOWN  );
    while(true){
        sleep_enable();
        cli();
        sleep_cpu();
    }
}
