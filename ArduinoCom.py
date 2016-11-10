#!/usr/bin/env python3

import os
import log

try:
    import curses
except ImportError as err:
    log.error("Could not import curses, is it installed?")
    log.trace(err)

import PyCmdMessenger.PyCmdMessenger

log.DEBUG_LEVEL = 3


def interface_wrapper(terminal_screen):
    terminal_screen.clear()

    application_interface = interface(terminal_screen)

    application_interface.start_loop()

    terminal_screen.refresh()
    terminal_screen.getkey()


class interface:
    env_windows = {}

    def __init__(self, terminal_screen):
        terminal_screen.clear()
        self.create_main_ui(terminal_screen)

    def create_main_ui(self, terminal_screen):
        terminal_screen.resize(curses.LINES - 20, curses.COLS)
        terminal_screen.addstr("Loading ArduinoCom...")

        # Make a Title/Status window at the top:
        terminal_screen.mvwin(2, 0)
        terminal_screen.refresh()
        self.env_windows["ui_statusbar"] = curses.newwin(1, curses.COLS, 0, 0)
        self.env_windows["ui_statusbar"].addstr("ArduinoCom Main Console")
        self.env_windows["ui_statusbar"].refresh()
        terminal_screen.refresh()

        # Make a pad for the console in/out to the arduino.
        self.env_windows["console_pad"] = curses.newpad(curses.LINES - 20, curses.COLS)
        # Move the console below the status bar
        self.env_windows["console_pad_coords"] = 2, 0, curses.LINES - 20, curses.COLS
        self.env_windows["console_pad_scroll"] = 0
        self.env_windows["console_pad"].addstr(log.info("Pad Initialized."))
        # self.env_windows["console_pad"].refresh(self.env_windows["console_pad_scroll"], 0, *self.env_windows["console_pad_coords"])

    def start_loop(self):
        pass
        # This will be filled later

if __name__ == "__main__":
    log.info("ArduinoCom CLI loading...")

    log.info("Starting environment...")
    curses.wrapper(interface_wrapper)

    # End of program.
