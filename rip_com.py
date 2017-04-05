#!/usr/bin/env python3

import os
import types
import logging
import importlib

try:
    from cmd2 import Cmd  # , options, make_option
except ImportError as err:
    print("Maybe you should pip3 install cmd2 (the better cmd class)")

from rip.head.spine.core import get_spine

rc_dict = {}

# RipCom-specific things.
current_search_path = os.path.dirname(os.path.realpath(__file__)) + "/appendages"
current_import_path = "appendages"
file_list = []
for f in os.listdir(current_search_path):
    if os.path.isfile(current_search_path + "/" + f) and f[-3:] == ".py" and f not in ["__init__.py", "units.py"]:
        file_list.append(f)
for f in file_list:
    module = importlib.import_module("{0:s}.{1:s}".format(current_import_path, f[:-3]))
    class_name = f[:-3].replace('_', ' ').title().replace(' ', '')
    rc_dict[class_name] = getattr(module, class_name)

# Points to the current robot's code.
CURRENT_ARDUINO_CODE_DIR = "/Robot/CurrentArduinoCode"


class rip_com(Cmd):
    intro = "Welcome to RipCom. Type help or ? for commands.\nCtrl-D to exit."
    prompt = "[RC]> "
    doc_header = "Documentation available for:"
    undoc_header = "Not documented:"
    gs = None
    s = None
    appendages = None
    device = None

    def __init__(self):
        super().__init__()
        self.refreshDevices()

    def refreshDevices(self):
        self.registeredDevices = [d for d in os.listdir(CURRENT_ARDUINO_CODE_DIR)
                                  if os.path.isdir("{0:s}/{1:s}".format(CURRENT_ARDUINO_CODE_DIR, d)) and
                                  not d == ".git" and os.path.exists("{0:s}/{1:s}/{1:s}.json"
                                                                     .format(CURRENT_ARDUINO_CODE_DIR, d))]
        if len(self.registeredDevices) != 0:
            self.registeredDevices.sort()

        self.connectedDevices = [d for d in self.registeredDevices
                                 if os.path.exists("/dev/{0:s}".format(d))]
        if len(self.connectedDevices) != 0:
            self.connectedDevices.sort()

        self.lockedDevices = [d for d in self.connectedDevices
                              if os.path.exists("/var/lock/{0:s}.lck".format(d))]
        if len(self.lockedDevices) != 0:
            self.lockedDevices.sort()

    def do_connect(self, parseResults):
        self.refreshDevices()

        args = parseResults.parsed[1].split()
        if len(args) != 1:
            self.help_connect()
            return

        for arduinoName in args:
            if arduinoName not in self.connectedDevices:
                print("Arduino \"{}\" is not available.".format(arduinoName))
                return

        self.gs = get_spine(devices=args)
        self.s = self.gs.__enter__()
        self.appendages = self.s.get_appendage_dict()

        def registerMethods(RCClass):
            self.__dict__["do_" + name] = types.MethodType(RCClass.interact, self)
            self.__dict__["help_" + name] = types.MethodType(RCClass.help, self)
            self.__dict__["complete_" + name] = types.MethodType(RCClass.complete, self)

        for name, appendage in self.appendages.items():
            if appendage.__class__.__name__ in rc_dict:
                registerMethods(rc_dict[appendage.__class__.__name__])
            else:
                print("{0:s} not found among RC imports".format(appendage.label))

        self.device = arduinoName

    def help_connect(self):
        print("usage: connect <ArduinoNames...>")
        print("Normally, ArduinoName could be something as simple as 'mega'")

    def complete_connect(self, text, line, begidx, endidx):
        return [i for i in self.connectedDevices if i.startswith(text)]

    def do_disconnect(self, parseResults):
        if self.appendages is not None:
            for name in self.appendages:
                del self.__dict__["do_" + name]
                del self.__dict__["help_" + name]
                del self.__dict__["complete_" + name]
            self.appendages = None

            self.gs.__exit__(None, None, None)
            self.s = None
            self.gs = None

    def help_disconnect(self):
        print("usage: disconnect")
        print("Disconnects from a connected arduino.")

    def do_list(self, parseResults):
        self.refreshDevices()
        self.print_topics("Connected Devices", self.connectedDevices, 15, 80)
        self.print_topics("Locked Devices", self.lockedDevices, 15, 80)

    def help_list(self):
        print("Lists the currently connected arduinos")

    def do_rmlock(self, parseResults):
        self.refreshDevices()
        arduinoName = parseResults.parsed[1]

        if arduinoName != "":
            if arduinoName == self.device:
                print("You are currently connected to {0:s}, lockfile not removed.".format(arduinoName))
            elif arduinoName in self.lockedDevices:
                try:
                    os.remove("/var/lock/{0:s}.lck".format(arduinoName))
                    print("Removed the {0:s} lockfile.".format(arduinoName))
                except PermissionError:
                    print("You don't have permission to remove the {0:s} lockfile.".format(arduinoName))
            elif arduinoName in self.connectedDevices:
                print("{0:s} is not locked.".format(arduinoName))
            elif arduinoName in self.registeredDevices:
                print("{0:s} is not connected.".format(arduinoName))
            else:
                print("{0:s} is not registered.".format(arduinoName))
        else:
            for arduinoName in self.lockedDevices:
                if arduinoName == self.device:
                    print("You are currently connected to {0:s}, lockfile not removed.".format(arduinoName))
                else:
                    try:
                        os.remove("/var/lock/{0:s}.lck".format(arduinoName))
                        print("Removed the {0:s} lockfile.".format(arduinoName))
                    except PermissionError:
                        print("You don't have permission to remove the {0:s} lockfile.".format(arduinoName))

    def help_rmlock(self):
        print("Removes lockfiles for connected devices.")
        print("If no device name is specified, removes all lockfiles.\n")
        print("usage: rmlock")
        print("       rmlock <device:str>")

    def complete_rmlock(self, text, line, begidx, endidx):
        return [i for i in self.lockedDevices if i.startswith(text)]

    def do_exit(self, parseResults):
        self.do_disconnect(None)
        return True

    def help_exit(self):
        print("Disconnects from any connected arduinos, and exits ArduinoCom.")

    def do_quit(self, parseResults):
        return self.do_exit(parseResults)

    def help_quit(self):
        print("Alias for exit")

    def do_EOF(self, parseResults):
        print()
        return self.do_exit(parseResults)
    do_eof = do_EOF

    def help_help(self):
        print("Prints help for commands")

    def get_names(self):
        names = dir(self)
        names.remove("do_EOF")
        names.remove("do_eof")
        names.remove("do_q")
        return names


# Initializes the command interface loop on the terminal.
# Uses __main__ detection so that this file can be used as an import from other pys.
if __name__ == '__main__':
    rc = rip_com()
    rc.debug = True
    rc.case_insensitive = True
    logging.disable(logging.INFO)
    rc.cmdloop()
