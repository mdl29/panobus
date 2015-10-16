#! /usr/bin/python3
import bibus

import sched, time, json
from datetime import datetime

class Bibus2Arduino:

    def __init__(self):
        print("Starting...")

        self.b = bibus.Bibus()

        print("Bibus API last version :", self.b.getVersion()[0]['Number'],"released the", self.b.getVersion()[0]["Date"])
        print("Bibus API used version : 1.1 released the 09/09/2015")
        print("Don't hesitate to open a new issue on https://github.com/mdl29/panobus on any bug")

        self.json_data=open('data/arret.json')
        self.arret = json.load(self.json_data)
        print("Info du fichier json des arrets")
        for arret in range(len(self.arret)):
            for route in range(len(self.arret[arret])):
                for dest in range(len(self.arret[arret]["route"][route]["dest"])):
                    print(self.arret[arret]["name"]," a pour destination, sur la ligne ",self.arret[arret]["route"][route]["name"],self.arret[arret]["route"][route]["dest"][dest])

        self.s = sched.scheduler(time.time, time.sleep)
        self.s.enter(6, 1, self.loop)
        self.s.run()
    
    def getData(self):
        print("get data")
        for arret in range(len(self.arret)):
            for route in range(len(self.arret[arret])):
                for dest in range(len(self.arret[arret]["route"][route]["dest"])):
                    print("\n",self.b.getRemainingTimes(self.arret[arret]["route"][route]["name"], self.arret[arret]["name"],self.arret[arret]["route"][route]["dest"][dest]))

    def processData(self,data):
        pass

    def sendData(self, processData):
		#See the file protocole.md for more information
        pass

    def loop(self):
        data = self.getData()
        processedData = self.processData(data)
        self.sendData(processedData)

        self.s.enter(6, 1, self.loop) #Wait for one minute

if __name__=="__main__":
    Bibus2Arduino()

print("Shut down normally...")
