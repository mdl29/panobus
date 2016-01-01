from neopixel import *

class LedHandler:

    colorBank = {"L8":[0, 230, 30],
                 "L5":[220, 108, 2],
                 "L7":[197, 30, 32],
                 "L12":[91, 190, 100],
                 "la":[255, 0, 0],
                 "pret":[255, 50, 0],
                 "proche":[20, 255, 20],
                 "approche":[0, 200, 255],
                 "loin":[0, 0, 255]}

    LED_FREQ_HZ = 800000  # LED signal frequency in hertz (800khz)
    LED_DMA = 5       # Cannal DMA a utiliser pour generer le signal PWM
    LED_LUMINOSITE = 255    # 0 -> sombre  255 forte luminositee
    LED_INVERT = False   # True pour invertir le signal
    LED_NBR = 33
    strip = Adafruit_NeoPixel(LED_NBR, 18, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_LUMINOSITE)
    def __init__(self):
        # Intialisation de la librairie
        print("Strip object created")
        self.strip.begin()
        print("Strip begin")
        #timer = Adafruit_NeoPixel(21, 19, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_LUMINOSITE)
        #timer.begin()

    def set_led(self, led_num, couleur):
        print("Set color to led:", led_num)
        self.strip.setPixelColor(led_num, Color(couleur[0], couleur[1], couleur[2]))
        self.strip.show()

    def led_arret(self):
        print("Set up led arret")
        for i in range(21, 33, 1):
            if i < 24:
                self.set_led(i, self.colorBank["L8"])
            if i == 24:
                self.set_led(i, self.colorBank["L12"])
            if i == 25 or i == 26:
                self.set_led(i, self.colorBank["L5"])
            if i == 27:
                self.set_led(i, [255, 0, 0])
            if i >= 28:
                self.set_led(i, self.colorBank["L7"])

    def led_time(self, data):
        for i in range(len(data)):
            print(data[i])
            if data[i] > 255:
                self.set_led(i, self.colorBank["loin"])
            elif data[i] > 200:
                self.set_led(i, self.colorBank["approche"])
            elif data[i] > 100:
                self.set_led(i, self.colorBank["proche"])
            elif data[i] > 50:
                self.set_led(i, self.colorBank["pret"])
            elif data[i] < 50:
                self.set_led(i, self.colorBank["la"])
    def off(self):
        for i in range(self.LED_NBR):
            self.set_led(i, [0, 0, 0])
