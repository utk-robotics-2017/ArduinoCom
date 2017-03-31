#!/usr/bin/env python3


class PositionControlledMotor:
    def interact(self, parseResults):
        def help(name):
            self.__dict__["help_" + name]()

        name = parseResults.parsed[0]
        args = parseResults.parsed[1].split()

        if len(args) == 0:
            help(name)

        elif args[0] == "set_voltage":
            if len(args) != 2:
                help(name)
                return

            try:
                val = int(args[1])
            except ValueError:
                help(name)
                return

            self.s.get_appendage(name).set_voltage(val)

        elif args[0] == "set_position":
            if len(args) != 2:
                help(name)
                return

            try:
                val = float(args[1])
            except ValueError:
                help(name)
                return

            self.s.get_appendage(name).set_position(val)

        elif args[0] == "set_allowed_direction":
            if len(args) != 2:
                help(name)
                return

            try:
                val = int(args[1])
            except ValueError:
                help(name)
                return

            self.s.get_appendage(name).set_allowed_direction(val)

        elif args[0] == "get_position":
            if len(args) != 1:
                help(name)
                return

            val = self.s.get_appendage(name).get_position()
            print("{}: {}".format(name, val))

        elif args[0] == "stop":
            if len(args) != 1:
                help(name)
                return

            self.s.get_appendage(name).stop()

        else:
            help(name)

    def help(self):
        print("usage: <pcm:str> set_voltage <voltage:int>")
        print("       <pcm:str> set_position <position:float>")
        print("       <pcm:str> get_position")
        print("       <pcm:str> stop")

    def complete(self, text, line, begidx, endidx):
        return [i for i in ["set_voltage", "get_position", "set_position", "stop"]
                if i.startswith(text)]
