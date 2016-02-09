#! /usr/bin/python3
"""
Look at Readme.md
"""
import threading
import json
from sys import argv

from pipe import Pipe

PIPE_START = "\n\n\n\n==================================== PIPE START ====================================\n\n"
PIPE_END =   "\n\n===================================== PIPE END ====================================\n\n\n\n"
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
        if not line:
            continue
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
        except KeyError:
            print("Bad command", command)
            continue

        print(PIPE_START)
        try:
            fct(*args)
        except Exception as e:
            print("ERROR in pipe", e.args)
        print(PIPE_END)

def main():
    """
    Main fonction
    """
    try:
        interface = argv[1]
    except IndexError:
        interface = "logs"

    if interface == "leds":
        from bibus2leds import Bibus2Leds
        i_bibus = Bibus2Leds
    elif interface == "logs":
        from bibus2logs import Bibus2Logs
        i_bibus = Bibus2Logs
    else:
        raise ValueError("Values in data/interface  should be 'leds' or 'logs'")


    event = threading.Event()
    event.set()
    bibus = i_bibus()

    def quit_():
        """
        Stop the program
        """
        print("quit is taken in count, could be quite long before exit")
        bibus.kill()
        event.clear()

    fct_array = {
        "quit" : quit_,
        "reload_efault_json": lambda *args: bibus.load(),
        "load_file": lambda *args: bibus.load(args[0]),
        "set_update_interval": lambda *args: bibus.set_update_interval(args[0]),
        "kill_pipe": lambda *args: event.clear(),
        "clear_leds" : lambda *args: bibus.clear(),
        "help" : lambda *args: print("\n".join(fct_array.keys())),
        }

    try:
        thread = threading.Thread(target=parse_pipe, args=(event, fct_array))

        thread.start()
        bibus.start()

    except KeyboardInterrupt:
        quit_()


if __name__ == "__main__":
    main()
