from neopixel import *

class LedHandler:

    colorBank={"L8":[0,230,30],
             "L5":[220,108,2],
             "L7":[197,30,32],
             "L12":[91,190,100],
             "la":[255,0,0],
             "pret":[255,50,0],
             "proche":[20,255,20],
             "approche":[0,200,255],
             "loin":[0,0,255]}

    LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (800khz)
    LED_DMA        = 5       # Cannal DMA a utiliser pour generer le signal PWM  
    LED_LUMINOSITE = 255    # 0 -> sombre  255 forte luminositee
    LED_INVERT     = False   # True pour invertir le signal 
   
    def __init__(self):
        info("Led should be turn on")
        # Intialisation de la librairie
        strip = Adafruit_NeoPixel(33, 18, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_LUMINOSITE)
        strip.begin()
        #timer = Adafruit_NeoPixel(21, 19, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_LUMINOSITE)
        #timer.begin()
        
    def set_led(ruban,led_num,couleur):
        ruban.setPixelColorRGB(led_num,Color(couleur[0],couleur[1],couleur[2]))
        ruban.show()
    
    def led_arret():
        for i in range(12):
             if i<3:
                set_led(strip,21+i,colorBank[L8])
             if i==3:
                set_led(strip,21+i,colorBank[L12])
             if i==4 or i==5:
                set_led(strip,21+i,colorBank[L5])
             if i==6:
                set_led(strip,21+i,[255,0,0])
             if i >= 7:
                set_led(strip,21+i,colorBank[L7])
    
    def led_time(data):
        for i in data:
            if data[i] > 255:
                set_led(strip,i,colorBank[loin])
            elif data[i] > 200:
                set_led(strip,i,colorBank[approche])
            elif data[i] > 100:
                set_led(strip,i,colorBank[proche])
            elif data[i] > 50:
                set_led(strip,i,colorBank[pret])
            elif data[i] < 10:
                set_led(strip,i,colorBank[la])
    def off():
		for i in range(33):
			set_led(strip,i,Color(0,0,0))

		
  
			

