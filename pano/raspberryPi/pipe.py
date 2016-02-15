"""
A class which read from a pipe data
"""
import os


class Pipe: #pylint: disable=R0903
    """
    A class to communicate with other programs throught a named pipe
    @args :- pipeName -> the path to the named Pipe eg: /tmp/pipe
    """

    def __init__(self, pipe_name):
        self.pipe_name = pipe_name

        if os.path.exists(self.pipe_name):
            os.remove(self.pipe_name)

        os.mkfifo(self.pipe_name)

        self.pipe = os.open(self.pipe_name, os.O_RDONLY | os.O_NONBLOCK)

    def __del__(self):
        """
        Destructor
        """

        if self.pipe:
            os.close(self.pipe)
            os.remove(self.pipe_name)

    def readlines(self):
        """
        Read in the field and create a generator on each line of the file
        This call is non-blocking and can return "" if no more data for the moment
        Should be exception safe but I'm not really sure
        """

        buffer = bytearray()

        while True:
            if not self.pipe:
                return
            try:
                block = os.read(self.pipe, 256)
            except:
                yield ""

            if block:
                buffer.extend(block)
            else:
                if buffer:
                    yield buffer.decode()
                    buffer = bytearray()
                else:
                    yield ""

            while True:
                (line, _, buffer) = buffer.partition(b'\n')

                if not buffer:
                    buffer = line
                    break

                yield line.decode()
