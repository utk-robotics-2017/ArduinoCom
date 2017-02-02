#!/usr/bin/env python3


class Motor:
    def interact(self, parseResults):
        def help(name):
            self.__dict__["help_" + name]()

        name = parseResults.parsed[0]
        args = parseResults.parsed[1].split()

        if len(args) == 0:
            help(name)

        elif args[0] == "drive":
            if len(args) != 2:
                help(name)
                return

            try:
                value = int(args[1])
            except ValueError:
                help(name)
                return

            self.s.get_appendage(name).drive(value)

        elif args[0] == "stop":
            if len(args) != 1:
                help(name)
                return

            self.s.get_appendage(name).stop()

        else:
            help(name)

    def help(self):
        print("usage: <motor:str> drive <value:int>")
        print("       <motor:str> stop")
        print("")
        print("value: [-1023, 1023]")

    def complete(self, text, line, begidx, endidx):
        return [i for i in ["drive", "stop"] if i.startswith(text)]
