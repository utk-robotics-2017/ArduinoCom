#!/usr/bin/env python3


class Stepper:
    def interact(self, parseResults):
        def help(name):
            self.__dict__["help_" + name]()

        name = parseResults.parsed[0]
        args = parseResults.parsed[1].split()

        if len(args) == 0:
            help(name)

        elif args[0] == "set_speed":
            if len(args) != 2:
                help(name)
                return

            try:
                val = float(args[1])
            except ValueError:
                help(name)
                return

            self.s.get_appendage(name).set_speed(val)

        elif args[0] == "set_angle":
            if len(args) != 2:
                help(name)
                return

            try:
                val = float(args[1])
            except ValueError:
                help(name)
                return

            self.s.get_appendage(name).set_angle(val)

        elif args[0] == "step":
            if len(args) != 2:
                help(name)
                return

            try:
                val = int(args[1])
            except ValueError:
                help(name)
                return

            self.s.get_appendage(name).step(val)

        else:
            help(name)

    def help(self):
        print("usage: <stepper:str> set_speed <speed:float>")
        print("       <stepper:str> set_angle <angle:float>")
        print("       <stepper:str> step <steps:int>")

    def complete(self, text, line, begidx, endidx):
        return [i for i in ["set_speed", "set_angle", "step"] if i.startswith(text)]
