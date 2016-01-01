"""
A module which contain a purely virtual interface between an element (to be defined) and bibus API
"""
import sched #for a 60sec scheduler
import time # for a 60sec scheduler
import json # For the file import

import bibus

class BibusInterface:
    """
    Abstract class
    Only need to reimplement sendData
    """
    def __init__(self):
        print("Starting...")
        self.interval = 30

        self._bibus = bibus.Bibus()
        print("Don't hesitate to open a new issue on https://github.com/mdl29/panobus on any bug")

        self.load()
        self.sched = sched.scheduler(time.time, time.sleep)

    def kill(self):
        """
        Stop the scheduler and exit the loop
        """
        if not self.sched.empty():
            for event in self.sched.queue:
                self.sched.cancel(event)
        self.interval = -1

    def load(self, file="data/arret_lycee_rel.json"):
        """
        load the good file (effect may be quite long)
        """

        print("Processing data file...")
        try:
            with open(file) as json_config:
                try:
                    self.config = json.load(json_config)
                except ValueError: #the exception depend of the version of python
                    print("Can't read json ! Malformed JSON ?")
                    return -1


        except FileNotFoundError:
            print("File not found !")
            return -1

        print("File {} readed".format(file))

    def start(self):
        """
        start the loop, should be started once only
        """
        self.sched.enter(0, 1, self.loop, ()) # No wait the first time
        self.sched.run()


    def get_data(self):
        """
        get the remaining_time of each stops specified by the load fct
        return a dict : {%id, [(remaining_time0, remaining_time1), time_to_go] ... }
        """
        data = {}
        for arret in self.config:
            for route in arret["route"]:
                for dest in route["dest"]:
                    remaining_time = self._bibus.get_remaining_times(route["name"],
                                                                     arret["name"], dest["name"])

                    data[dest["id"]] = [(-1, -1), -1]

                    # test data integrity
                    try:
                        remaining_time0 = remaining_time[0][0]['Remaining_time']

                        #transform the 'hh:mm:ss' format to seconds
                        t_tmp = remaining_time0.split(':')
                        remaining_time_val0 = int(t_tmp[0])*3600 + int(t_tmp[1])*60 + int(t_tmp[2])
                    except IndexError:
                        print('Bad URI ? : {} -> I got {}'.format(remaining_time[1],
                                                                  remaining_time[0]))
                        continue


                    try:
                        remaining_time1 = remaining_time[0][1]['Remaining_time']

                        #transform the 'hh:mm:ss' format to seconds
                        t_tmp = remaining_time1.split(':')
                        remaining_time_val1 = int(t_tmp[0])*3600 + int(t_tmp[1])*60 + int(t_tmp[2])
                    except IndexError:
                        remaining_time_val1 = -1

                    data[dest["id"]][1] = arret["time2Go"]
                    data[dest["id"]][0] = (remaining_time_val0, remaining_time_val1)
        return data

    @staticmethod
    def process_data(data):
        """
        after receiving data, this process data
        return a dict : {id: value between 0 and 255 depending of remaining_time}
        look algo for more details
        """
        #order by key
        processed_data = dict()
        for key in sorted(data):
            val = -1
            time_to_go = data[key][1]
            if data[key][0][0] - time_to_go > 0:
                val = data[key][0][0] - time_to_go

            elif data[key][0][1] - time_to_go > 0:
                val = data[key][0][1] - time_to_go

            if val > 600 or val < 0:
                processed_data[key] = 255
            else:
                processed_data[key] = int(254/600 * val)
        return processed_data

    def send_data(self, processed_data):
        """
            See protocole.md for more informations
        """
        raise NotImplementedError


    def loop(self):
        """
            A loop restarting all 30sec which do the whole cycle
        """
        #should don't be changed, look to subfunctions instead
        data = self.get_data()
        processed_data = self.process_data(data)
        print("Send to the led")
        self.send_data(processed_data)
        if self.interval >= 0:
            self.sched.enter(self.interval, 1, self.loop, ()) #Wait for an interval (30s by default)


    def set_update_interval(self, interval):
        """
        set the scheduler interval
        arg have to be an int of a string castable to int
        """
        try:
            interval = int(interval)
        except ValueError:
            return

        self.interval = interval
