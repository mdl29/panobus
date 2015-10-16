#! /usr/bin/python3
import bibus

import sched, time # for a 60sec scheduler
import json # For the file import
import logging # For ... logs

logging.basicConfig(filename='bibus.log', level=logging.DEBUG)
debug = logging.debug
info = logging.info
warning = logging.warning

class Bibus2Arduino:
    def __init__(self):
        info("Starting...")
        
        info("Processing data file...")

        with open('data/arret.json') as json_data:
            self.data = json.load(json_data)
        if not self.data:
            raise Exception("Can't load file !")

        self.b = bibus.Bibus()

        debug("Bibus API last version : {} released the {}".format(self.b.getVersion()[0]['Number'],self.b.getVersion()[0]["Date"]))
        debug("Bibus API used version : 1.1 released the 09/09/2015")
        info("Don't hesitate to open a new issue on https://github.com/mdl29/panobus on any bug")


        info("Info du fichier json des arrets")

        for arret in self.data:
            for route in arret["route"]:
                for dest in route["dest"]:
                    debug("Reading JSON ... {}({}) -> {}".format(arret["name"],route["name"], dest))

        self.s = sched.scheduler(time.time, time.sleep)
        self.s.enter(0, 1, self.loop) # No wait the first time
 
        self.s.run()
    

    def getData(self):
        debug("Get data : ")
        for arret in self.data:
            for route in arret["route"]:
                for dest in route["dest"]:
                    remainingTime = self.b.getRemainingTimes(route["name"],arret["name"], dest)
                    try:
                        remainingTimeVal = remainingTime[0][0]['Remaining_time']
                    except IndexError:
                        warning('Bad URI ? : {}'.format(remainingTime[1]))

                    debug("Remaining time for {}({}) -> {} : {}".format(arret["name"],route["name"], dest,remainingTimeVal))

    def processData(self,data):
        pass

    """
        See protocole.md for more informations 
    """
    def sendData(self, processData):
        pass

    """
        A loop restarting all 60sec which do the whole cycle 
    """
    def loop(self):
        #should don't be changed, look to subfunctions instead
        data = self.getData()
        processedData = self.processData(data)
        self.sendData(processedData)

        self.s.enter(60, 1, self.loop) #Wait for one minute

if __name__=="__main__":
    Bibus2Arduino()


info("Shut down normally...")
