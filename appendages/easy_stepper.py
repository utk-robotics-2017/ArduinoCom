#!/usr/bin/env python3


class EasyStepper:
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
                val = int(args[1])
            except ValueError:
                help(name)
                return

            self.s.get_appendage(name).set_speed(val)

        elif args[0] == "step_angle":
            if len(args) is not 2 and len(args) is not 3:
                help(name)
                return

            try:
                val = int(args[1])
            except ValueError:
                help(name)
                return

            if len(args) is 3:
                try:
                    timeout = float(args[2])
                except ValueError:
                    help(name)
                    return
                self.s.get_appendage(name).step_angle(val, timeout=timeout)
            else:
                self.s.get_appendage(name).step_angle(val)

        elif args[0] == "step":
            if len(args) is not 2 and len(args) is not 3:
                help(name)
                return

            try:
                val = int(args[1])
            except ValueError:
                help(name)
                return

            if len(args) is 3:
                try:
                    timeout = float(args[2])
                except ValueError:
                    help(name)
                    return
                self.s.get_appendage(name).step(val, timeout=timeout)
            else:
                self.s.get_appendage(name).step(val)

        else:
            help(name)

    def help(self):
        print("usage: <stepper:str> set_speed <speed:int> ( >= 53 )")
        print("       <stepper:str> step_angle <angle:int> ?<timeout:float>")
        print("       <stepper:str> step <steps:int> ?<timeout:float>")

    def complete(self, text, line, begidx, endidx):
        return [i for i in ["set_speed", "step_angle", "step"] if i.startswith(text)]
