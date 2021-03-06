"""
An implementation which send to files data
"""

import bibusinterface

class Bibus2Logs(bibusinterface.BibusInterface):
    """
    An implementation which send to files data
    """
    def __init__(self, log_file=""):
        super().__init__()

    def update_data(self, id_, remaining_time=None):
        if not remaining_time:
            remaining_time = 'UNKNOW'
        print("bus id n°", id_, "arrive in nearly", remaining_time, "seconds")
