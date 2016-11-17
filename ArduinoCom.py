#!/usr/bin/env python3

import os
import sys
import log

try:
    import urwid
except ImportError as err:
    log.info("Maybe sudo apt install python3-urwid ?")
    log.error("Could not import urwid.")
    log.trace(err)
    sys.exit()

import cmd
import PyCmdMessenger.PyCmdMessenger

# Shamelessly stolen:
# from: http://zderadicka.eu/terminal-interfaces-in-python/
# import commander

log.DEBUG_LEVEL = 3

color_pallette = [
    ('title_bg', 'black', 'grey'),
    ('bg', 'black', 'grey')
]


class Commands(cmd.Cmd):
    intro = "Welcome to ArduinoCom. Type help or ? for commands.\n"
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

    def do_connect(self, *args):
        """connect [com port]
Connects to an arduino
Usage: Not completed yet.
        """
        raise NotImplementedError

    def do_EOF(self, *args):
        raise urwid.ExitMainLoop()


def urwid_keyhandler(key):
    if key in ('q', 'Q'):
        raise urwid.ExitMainLoop()

if __name__ == "__main__":
    log.info("ArduinoCom CLI loading...")

    Commands().cmdloop()

    # End of program.
