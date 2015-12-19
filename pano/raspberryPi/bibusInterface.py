import bibus

import sched, time # for a 60sec scheduler
import json # For the file import

"""
Abstract class
Only need to reimplement sendData
"""
class BibusInterface:
    def __init__(self):
        print("Starting...")
        self.interval = 30

        self.b = bibus.Bibus()

        print("Don't hesitate to open a new issue on https://github.com/mdl29/panobus on any bug")

        self.load()
        
        self.s = sched.scheduler(time.time, time.sleep)
        
        self.loop2sleep = 10 #Number of interval do before sleep when no data get

    def kill(self):
        if not self.s.empty():
            for event in self.s.queue:
                self.s.cancel(event)
        self.interval = -1

    def load(self,file = "data/arret_lycee_rel.json"):
         
        print("Processing data file...")
        try:
            with open(file) as json_config:
                try:
                    self.config = json.load(json_config)
                except:
                    warning("Can't read json ! Malformed JSON ?")
                    return -1

        except FileNotFoundError:
            warning("File not found !")
            return -1

        print("File {} readed".format(file))

    def start(self):
        self.s.enter(0, 1, self.loop,()) # No wait the first time
 
        self.s.run()
    

    def getData(self):
        data = {}
        for arret in self.config:
            for route in arret["route"]:
                for dest in route["dest"]:
                    remainingTime = self.b.getRemainingTimes(route["name"],arret["name"], dest["name"])

                    data[dest["id"]] = [(-1,-1),-1] #[(remainingTime0,remainingTime1),time2Go]

                    # test data integrity
                    try:
                        remainingTime0 = remainingTime[0][0]['Remaining_time']
    
                        #transform the 'hh:mm:ss' format to seconds
                        t = remainingTime0.split(':')
                        remainingTimeVal0 = int(t[0])*3600 + int(t[1])*60 + int(t[2])
                    except IndexError:
                        print('Bad URI ? : {} -> I got {}'.format(remainingTime[1], remainingTime[0]))
                        continue
        
                    
                    try:
                        remainingTime1 = remainingTime[0][1]['Remaining_time']
    
                        #transform the 'hh:mm:ss' format to seconds
                        t= remainingTime1.split(':')
                        remainingTimeVal1 = int(t[0])*3600 + int(t[1])*60 + int(t[2])
                    except IndexError:
                        remainingTimeVal1 = -1

                    data[dest["id"]][1] = arret["time2Go"]
                    data[dest["id"]][0] = (remainingTimeVal0,remainingTimeVal1)				
        return data

    def processData(self,data):
        #order by key
        processedData = dict()
        for key in sorted(data):
            val = -1
            time2Go = data[key][1]
            if data[key][0][0] - time2Go > 0 :
                val = data[key][0][0] - time2Go

            elif data[key][0][1] - time2Go > 0:
                val = data[key][0][1] - time2Go

            if val > 600 or val < 0:
                processedData[key] = 255
            else:
                processedData[key] = int(254/600 * val)
        return processedData

    """
        See protocole.md for more informations 
    """
    def sendData(self, processData):
        raise NotImplemented
		

    """
        A loop restarting all 30sec which do the whole cycle 
    """
    def loop(self):

        #should don't be changed, look to subfunctions instead
        data = self.getData()
        processedData = self.processData(data)
        if self.emptyData(data):
            self.loopNbr+=1
            if self.loopNbr>self.loop2sleep:
                self.sendData("no")
                loopNbr=0
        self.sendData(processedData)
        if self.interval >= 0:
            self.s.enter(self.interval, 1, self.loop,()) #Wait for an interval (30s by default)


    def setUpdateInterval(self,i):
        try:
            i  = int(i)
        except:
            return
        
        self.interval = i
    
    def emptyData(self,data):
        empty=True
        for i in data:
            if i!="":
                empty=False
        return empty
			
