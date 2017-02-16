#!/usr/bin/env python3


class SoftwarePwm:
    def interact(self, parseResults):
        def help(name):
            self.__dict__["help_" + name]()

        name = parseResults.parsed[0]
        args = parseResults.parsed[1].split()

        if len(args) == 0:
            help(name)
        elif args[0] == "set_pwm":
            if len(args) != 2:
                help(name)
                return

            try:
                val = int(args[1])
            except ValueError:
                help(name)
                return

            self.s.get_appendage(name).set_pwm(val)

        else:
            help(name)

    def help(self):
        print("usage: <stepper:str> set_pwm <value:int>")

    def complete(self, text, line, begidx, endidx):
        return [i for i in ["set_pwm"] if i.startswith(text)]
