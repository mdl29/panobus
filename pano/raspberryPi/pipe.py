import os
import fcntl


"""
A class to communicate with other programs throught a named pipe
@args :- pipeName -> the path to the named Pipe eg: /tmp/bibusPipe
"""
class Pipe():
    def __init__(self, pipeName):
        self.pipeName = pipeName

        if os.path.exists(self.pipeName):
            os.remove(self.pipeName)

        os.mkfifo(self.pipeName)

        self.pipe = os.open(self.pipeName, os.O_RDONLY | os.O_NONBLOCK)

    """
    Destructor
    """
    def __del__(self):
        if self.pipe:
            os.close(self.pipe)
            try:
                os.remove(self.pipeName)
            except Exception as e:
                raise e

    """
    Read in the field and create a generator on each line of the file
    This call is non-blocking and can return "" if no more data for the moment
    Should be exception safe but I'm not really sure
    """
    def readlines(self):
        buffer = bytearray()
    
        while True:
            if not self.pipe:
                return
            try:
                block = os.read(self.pipe,256)
            except BlockingIOError :
                yield ""
        
            if block:
                buffer.extend(block)
            else:
                if buffer:
                    yield buffer.decode()
                    buffer.clear()
                else:
                    yield ""

            while True:
                (line,_,buffer) = buffer.partition(b'\n')

                if not buffer:
                    buffer = line
                    break

                yield line.decode()
