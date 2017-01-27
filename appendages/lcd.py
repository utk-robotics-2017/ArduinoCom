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
            self.s.get_appendage(name).write(self.message)  # TODO name in rip.spine

        elif args[0] == "clear":
            self.s.get_appendage(name).write(" ")

        else:
            help(name)

    def help(self):
        print("usage: <lcd:str> write <value:str>")
        print("       <lcd:str> clear")

    def complete(self, text, line, begidx, endidx):
        return [i for i in ["write", "clear"] if i.startswith(text)]
