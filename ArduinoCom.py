#!/usr/bin/env python3

import os
import sys
import log
import signal

try:
    import urwid
except ImportError as err:
    log.info("Maybe sudo apt install python3-urwid ?")
    log.error("Could not import urwid.")
    log.trace(err)
    sys.exit()

import cmd
import PyCmdMessenger

# Shamelessly stolen:
# from: http://zderadicka.eu/terminal-interfaces-in-python/
# import commander
import urwid_com_window

log.DEBUG_LEVEL = 3

color_pallette = [
    ('title_bg', 'black', 'grey'),
    ('bg', 'black', 'grey')
]

global baud_rate
baud_rate = 115200

global ac_CmdMessengerInstance
global ac_ArduinoInstance
global ac_Commands
global ac_port
ac_port = ""


class Commands(cmd.Cmd):
    intro = "Welcome to ArduinoCom. Type help or ? for commands.\nCtrl-D or quit to exit."
    prompt = "A-C > "
    doc_header = "Documentation available for:"
    undoc_header = "Not documented:"

    def do_echo(self, *args):
        return ' '.join(args)

    def do_raise(self, *args):
        """raise (no arguments)
Literally just raises a test exception.
There are no easter eggs in this program.
        """
        raise Exception('An air roar!')

    def do_c(self, *args):
        self.do_connect(*args)

    def do_connect(self, *args):
        """connect [com port]
Connects to an arduino
Example: connect /dev/mega
        """
        if args[0] == "":
            print("Wrong usage of connect.")
            # return "Nope."
        else:
            global ac_port
            ac_port = args[0]
            global ac_ArduinoInstance, baud_rate
            ac_ArduinoInstance = PyCmdMessenger.ArduinoBoard(ac_port, baud_rate=baud_rate)
            # TODO ac_Commands
            global ac_CmdMessengerInstance
            ac_CmdMessengerInstance = PyCmdMessenger(ac_ArduinoInstance, ac_Commands)
            # Starts the urwid window, using an output frame and then an input box
            print("Attempting to start connection...")

    def do_quit(self, *args):
        self.do_exit(args)

    def do_exit(self, *args):
        """exit
No Arguments.
Exits the program.
        """
        print("Goodbye.\n")
        sys.exit(0)

    def do_EOF(self, *args):
        print("EOF: Exiting Program.")
        self.do_exit()


def urwid_keyhandler(key):
    if key in ('q', 'Q'):
        raise urwid.ExitMainLoop()


def sigint_handler(signal, frame):
    sys.exit("SigInt Caught.")

if __name__ == "__main__":
    log.info("ArduinoCom CLI loading...")

    Commands().cmdloop()

    # End of program.
