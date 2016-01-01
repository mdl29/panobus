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
        self.led.off()
        super().kill()

    def send_data(self, processData):
        out = bytearray()
        out.append(len(processData))

        for key in sorted(processData): # sort by key (here, an index)
            out.append(processData[key])

        self.led.led_time(out)
        print("Send to the led")
