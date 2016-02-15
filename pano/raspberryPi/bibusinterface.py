"""
A module which contain a purely virtual interface between an element (to be defined) and bibus API
"""
import sched #for a 60sec scheduler
import time # for a 60sec scheduler
import json # For the file import
import sys
import os
import bibus

class BibusInterface:
    """
    Abstract class
    Only need to reimplement sendData
    """
    def __init__(self):
        print("Starting...")
        self.interval = 30
        self.max_time = 600 # 10 [min] -> used for proportionallity (cf update_data)

        self._bibus = bibus.Bibus()
        print("Don't hesitate to open a new issue on https://github.com/mdl29/panobus on any bug")
        file = "{}/data/arret_lycee_rel.json".format(os.path.dirname(os.path.realpath(sys.argv[0])))
        self.load(file)
        self.sched = sched.scheduler(time.time, time.sleep)

    def kill(self):
        """
        Stop the scheduler and exit the loop
        """
        try:
            if not self.sched.empty():
                for event in self.sched.queue:
                    self.sched.cancel(event)
            del self.sched
        except Exception:
            pass

    def load(self, file):
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
        return a dict : {id, [(remaining_time0, remaining_time1), time_to_go] ... }
        """
        for arret in self.config:
            for route in arret["route"]:
                for dest in route["dest"]:
                    id_ = dest['id']
                    time_to_go = arret["time2Go"]
                    bibus_remaining_time = self._bibus.get_remaining_times(route["name"],
                                                                           arret["name"],
                                                                           dest["name"])

                    # test data integrity
                    try: # value n 1
                        remaining_time = bibus_remaining_time[0][0]['Remaining_time']

                    except IndexError:
                        print('Any data received from bibus: {} -> I got {}'.format(
                            self._bibus.HOST + bibus_remaining_time[1],
                            bibus_remaining_time[0]))

                        self.update_data(id_, 0)
                        continue

                    #transform the 'hh:mm:ss' format to seconds
                    t_tmp = remaining_time.split(':')
                    remaining_time_val = int(t_tmp[0])*3600 + int(t_tmp[1])*60 +\
                            int(t_tmp[2]) - time_to_go #[s]
                    print("first ", remaining_time_val)

                    if remaining_time_val < 0:

                        try: #value n 2
                            remaining_time = bibus_remaining_time[0][1]['Remaining_time']
                        except IndexError:
                            self.update_data(id_, 3600)
                            continue

                        #transform the 'hh:mm:ss' format to seconds
                        t_tmp = remaining_time.split(':')
                        remaining_time_val = int(t_tmp[0])*3600 + int(t_tmp[1])*60 +\
                                int(t_tmp[2]) - time_to_go #[s]
                        print("bis", remaining_time_val)

                        if remaining_time_val < 0: # possible but ... really unexpected
                            self.update_data(id_, 3600)

                    self.update_data(id_, remaining_time_val)

    def update_data(self, id_, remaining_time=None):
        """
        after receiving data, this process data
        return a dict : {id: value between 0 and 255 depending of remaining_time}
        look algo for more details
        """
        #order by key
        if remaining_time is None:
            data = 0
        if remaining_time > self.max_time:
            data = 255
        else:
            data = int(254/self.max_time * remaining_time) # -> between 0 and 255

        self.send_data(id_, data)

    def send_data(self, id_, data):
        """
            See protocole.md for more informations
        """
        raise NotImplementedError


    def loop(self):
        """
            A loop restarting all 30sec which do the whole cycle
        """
        #should don't be changed, look to subfunctions instead
        self.get_data()

        try:
            self.sched.enter(self.interval, 1, self.loop, ()) #Wait for an interval (30s by default)
        except:
            return

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

    def clear(self):
        """Should be redefined if used."""
        pass
