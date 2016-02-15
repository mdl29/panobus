"""
An implementation of the BibusInterface
"""
import bibusinterface
import ledHandler

class Bibus2Leds(bibusinterface.BibusInterface):
    """
    An interface between the bibus api and the ruban of led
    """
    def __init__(self):
        self.led = ledHandler.LedHandler()
        self.led.led_arret()
        super().__init__()

    def kill(self):
        def nop(self):
	        quit() #good bye...
        self.send_data = nop
        self.led.off()
        print ("test")
        super().kill()

    def send_data(self, id_, data):
        self.led.update_led(id_,data)

    def clear(self):
        self.led.off()
        self.led.led_arret()
