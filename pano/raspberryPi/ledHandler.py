try:
    from neopixel import Adafruit_NeoPixel, Color
except ImportError:
    from fakeneopixel import Adafruit_NeoPixel, Color

class LedHandler:

    colorBank = {"L8":[0, 50, 5],
                 "L5":[200, 40, 0],
                 "L7":[160, 30, 20],
                 "L12":[91, 190, 100],
                 "la":[255, 0, 0],
                 "pret":[255, 50, 0],
                 "proche":[20, 255, 20],
                 "approche":[0, 200, 255],
                 "loin":[0, 0, 255],
                 "blanc":[255, 255, 100]}

    rubanArret = ["L8",
                  "L7",
                  "L8",
                  "L8",
                  "L12",
                  "L5",
                  "blanc",
                  "L5",
                  "L7",
                  "L7",
                  "L7",
                  "L7"]

    LED_FREQ_HZ = 800000  # LED signal frequency in hertz (800khz)
    LED_DMA = 5       # Cannal DMA a utiliser pour generer le signal PWM
    LED_LUMINOSITE = 255    # 0 -> sombre  255 forte luminositee
    LED_INVERT = False   # True pour invertir le signal
    LED_NBR = 33
    strip = Adafruit_NeoPixel(LED_NBR, 18, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_LUMINOSITE)

    def __init__(self):
        # Intialisation de la librairie
        self.strip.begin()

    def set_led(self, led_num, couleur):
        """set led of id led_ to color(a tuple of rgb))"""
        self.strip.setPixelColor(led_num, Color(couleur[0], couleur[1], couleur[2]))
        self.strip.show()

    def led_off(self, led):
        """switch of led of id led"""
        self.set_led(led, [0, 0, 0])

    def led_arret(self):
        print("Set up led arret")
        for i in range(len(self.rubanArret)):
            self.set_led(21+i, self.colorBank[self.rubanArret[i]])

    def update_led(self, id_, data):
        """Set the led of id id_ to the good color (look at code to know more"""
        if data >= 255:
            self.set_led(id_, self.colorBank["loin"])
        elif data >= 200:
            self.set_led(id_, self.colorBank["approche"])
        elif data >= 100:
            self.set_led(id_, self.colorBank["proche"])
        elif data >= 50:
            self.set_led(id_, self.colorBank["pret"])
        elif data > 0:
            self.set_led(id_, self.colorBank["la"])
        else:
            self.led_off(id_)

    def off(self):
        """Switch off every leds"""
        for i in range(self.LED_NBR):
            self.led_off(i)
