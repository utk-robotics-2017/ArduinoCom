#!/usr/bin/env python3


class Encoder:
    def interact(self, parseResults):
        def help(name):
            self.__dict__["help_" + name]()

        name = parseResults.parsed[0]
        args = parseResults.parsed[1].split()

        if len(args) == 0:
            help(name)

        elif args[0] == "read":
            if len(args) != 1:
                help(name)
                return

            angle = self.s.get_appendage(name).read()
            value = angle.base_value
            print("{}: {}".format(name, value))

        elif args[0] == "zero":
            if len(args) != 1:
                help(name)
                return

            self.s.get_appendage(name).zero()

        else:
            help(name)

    def help(self):
        print("usage: <encoder:str> read")
        print("       <encoder:str> zero")

    def complete(self, text, line, begidx, endidx):
        return [i for i in ["read", "zero"] if i.startswith(text)]
