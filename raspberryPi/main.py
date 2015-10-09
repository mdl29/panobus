#! /usr/bin/python3
import bibus


import sched, time
from datetime import datetime

class Bibus2Arduino:
    def __init__(self):
        print("Starting...")

        self.b = bibus.Bibus()

        print("Bibus API version :", self.b.getVersion()[0]['Number'])
        print("Don't hesitate to open a new issue on https://github.com/mdl29/panobus on any bug")

        self.s = sched.scheduler(time.time, time.sleep)
        self.s.enter(6, 1, self.loop)
        self.s.run()
    
    def getData(self):
        pass

    def processData(self,data):
        pass

    def sendData(self, processData):
        pass

    def loop(self):
        data = self.getData()
        processedData = self.processData(data)
        self.sendData(processedData)

        self.s.enter(6, 1, self.loop) #Wait for one minute

if __name__=="__main__":
    Bibus2Arduino()

print("Shut down normally...")
