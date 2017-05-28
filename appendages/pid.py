#!/usr/bin/env python3


class Pid:
    def interact(self, parseResults: list) -> None:
        def help(name: str):
            self.__dict__["help_" + name]()

        name = parseResults.parsed[0]
        args = parseResults.parsed[1].split()

        if len(args) == 0:
            help(name)

        elif args[0] == "modify_constants":
            if len(args) != 4:
                help(name)
                return

            try:
                kp = float(args[1])
                ki = float(args[2])
                kd = float(args[3])
            except ValueError:
                help(name)
                return

            self.s.get_appendage(name).modify_constants(kp, ki, kd)

        elif args[0] == "set":
            if len(args) != 2:
                help(name)
                return

            try:
                setpoint = float(args[1])
            except ValueError:
                help(name)
                return

            self.s.get_appendage(name).set(setpoint)

        elif args[0] == "off":
            if len(args) != 1:
                help(name)
                return

            self.s.get_appendage(name).off()

        elif args[0] == "display":
            if len(args) != 1:
                help(name)
                return

            val = self.s.get_appendage(name).display()
            print("{}: {}".format(name, val))

        else:
            help(name)

    def help(self):
        print("usage: <pid:str> modify_constants <kp:float> <ki:float> <kd:float>")
        print("       <pid:str> set <setpoint:float>")
        print("       <pid:str> off")
        print("       <pid:str> display")

    def complete(self, text: str, line: str, begidx: int, endidx: int):
        return [i for i in ["modify_constants", "set", "off", "display"] if i.startswith(text)]
