#!/usr/bin/env python3

from .units import Length


class Ultrasonic:
    def interact(self, parseResults):
        def help(name):
            self.__dict__["help_" + name]()

        name = parseResults.parsed[0]
        args = parseResults.parsed[1].split()

        if len(args) == 0:
            help(name)

        elif args[0] == "set_distance":
            if len(args) != 2:
                help(name)
                return

            try:
                val = float(args[1])
            except ValueError:
                help(name)
                return

            self.s.get_appendage(name).set_distance(val)

        elif args[0] == "read":
            if len(args) != 1:
                help(name)
                return

            val = self.s.get_appendage(name).read()
            print("{}: {} cm".format(name, val.to(Length.cm)))

        else:
            help(name)

    def help(self):
        print("usage: <ultrasonic:str> set_distance <distance:float>")
        print("       <ultrasonic:str> read")

    def complete(self, text, line, begidx, endidx):
        return [i for i in ["set_distance", "read"] if i.startswith(text)]
