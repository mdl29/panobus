#! /usr/bin/python3
"""
Look at Readme.md
"""
import threading
import json

from pipe import Pipe

def parse_pipe(event, fct_array):
    """
    read line in a pipe and parse it to call a function with given args
    ex -> ["print", "un", "deux, "trois","soleil"] will be the same than
    print("un","deux", "trois", "soleil")
    """
    pipe = Pipe("/tmp/bibusPipe")
    for line in pipe.readlines():
        if not event.isSet():
            return
        try:
            args = json.loads(line)
        except ValueError:
            continue

        if not isinstance(args, list):
            continue

        try:
            command = args.pop(0)
        except IndexError:
            continue

        try:
            fct = fct_array[command]
        except IndexError:
            continue

        fct(*args)

def main():
    """
    Main fonction
    """
    interface = "leds"
    try:
        with open("./data/interface.conf") as i_file:
            interface = i_file.readline()

    except IOError:
        pass
    if interface == "leds":
        pass
    from bibus2leds import Bibus2Leds
    i_bibus = Bibus2Leds
    if True:
        pass
    else:
        pass
        #raise ValueError("Values in data/interface  should be 'leds' or 'logs'")


    event = threading.Event()
    event.set()
    bibus = i_bibus()

    def quit_():
        """
        Stop the program
        """
        event.clear()
        bibus.kill()
        print("quit is taken in count, could be quite long before exit")

    fct_array = {
        "print": print,
        "quit" : quit,
        "reloadDefaultJSON": lambda *args: bibus.load(),
        "loadFile": lambda *args: bibus.load(args[0]),
        "set_update_interval": lambda *args: bibus.set_update_interval(args[0]),
        "killPipeReading": lambda *args: event.clear()
        }

    try:
        thread = threading.Thread(target=parse_pipe, args=(event, fct_array))

        thread.start()
        bibus.start()

    except KeyboardInterrupt:
        quit_()


if __name__ == "__main__":
    main()


