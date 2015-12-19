import bibusInterface

class Bibus2Logs(bibusInterface.BibusInterface):
    def __init__(self):
        super().__init__()

    def kill(self):
        super().kill()

    def sendData(self, processData):
        for key in sorted(processData):
            print(processData)
