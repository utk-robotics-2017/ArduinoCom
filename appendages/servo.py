#!/usr/bin/env python3


class Servo:
    def interact(self, parseResults: list) -> None:
        def help(name: str):
            self.__dict__["help_" + name]()

        name = parseResults.parsed[0]
        args = parseResults.parsed[1].split()

        if len(args) == 0:
            help(name)

        elif args[0] == "set":
            if len(args) != 2:
                help(name)
                return

            try:
                value = int(args[1])
            except ValueError:
                help(name)
                return

            self.s.get_appendage(name).set(value)

        elif args[0] == "detach":
            if len(args) != 1:
                help(name)
                return

            self.s.get_appendage(name).detach()

        else:
            help(name)

    def help(self):
        print("usage: <servo:str> set <value>")
        print("       <servo:str> detach")
        print("")
        print("value: [0, 180]")

    def complete(self, text: str, line: str, begidx: int, endidx: int):
        return [i for i in ["set", "detach"] if i.startswith(text)]
