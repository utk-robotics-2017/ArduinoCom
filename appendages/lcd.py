#!/usr/bin/env python3


class Lcd:
    def interact(self, parseResults):
        def help(name):
            self.__dict__["help_" + name]()

        name = parseResults.parsed[0]
        args = parseResults.parsed[1].split()

        if len(args) == 0:
            help(name)

        elif args[0] == "write":
            if len(args) < 2:
                help(name)
                return
            self.message = " ".join(args[1:])
            print("Writing message to LCD: " + self.message)
            self.s.get_appendage(name).write(self.message)

        elif args[0] == "clear":
            self.s.get_appendage(name).clear()

        elif args[0] == "writepos":
            if len(args) < 3:
                help(name)
                return
            try:
                horizontal = int(args[1])
                vertical = int(args[2])
            except ValueError as err:
                help(name)
                return
            self.s.get_appendage(name).setpos(horizontal, vertical)
            if len(args) > 3:
                self.s.get_appendage(name).write(args[3:])

        else:
            help(name)

    def help(self):
        print("usage: <lcd:str> write <value:str>")
        print("       <lcd:str> clear")
        print("       <lcd:str> writepos <value:int> <value:int> <value:str>")

    def complete(self, text, line, begidx, endidx):
        return [i for i in ["write", "clear", "writepos"] if i.startswith(text)]
