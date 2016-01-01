"""
An implementation which send to files data
"""
import bibusinterface

class Bibus2Logs(bibusinterface.BibusInterface):
    """
    An implementation which send to files data
    """
    def __init__(self):
        super().__init__()

    def kill(self):
        super().kill()

    def send_data(self, processData):
        for _ in sorted(processData):
            print(processData)
