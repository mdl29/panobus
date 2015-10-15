#! /usr/bin/python3
import bibus


import sched, time, json
from datetime import datetime

class Bibus2Arduino:
    json_data=open('data/arret.json')
    data = json.load(json_data)
    def __init__(self):
        print("Starting...")

        self.b = bibus.Bibus()

        print("Bibus API last version :", self.b.getVersion()[0]['Number'],"released the", self.b.getVersion()[0]["Date"])
        print("Bibus API used version : 1.1 released the 09/09/2015")
        print("Don't hesitate to open a new issue on https://github.com/mdl29/panobus on any bug")


        print("Info du fichier json des arrets")
        for arret in range(len(self.data["arret"])):
            print(self.data["arret"][arret]["name"]," a pour dest ",self.data["arret"][arret]["dest"][0]," et ", self.data["arret"][arret]["dest"][1])

        self.s = sched.scheduler(time.time, time.sleep)
        self.s.enter(6, 1, self.loop)
        self.s.run()
    
    def getData(self):
        print("get data")
        for i in range(len(self.data["arret"])):
            print(self.b.getRemainingTimes(self.data["arret"][i]["route"][0],self.data["arret"][i]["name"],self.data["arret"][i]["dest"][0]))

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
