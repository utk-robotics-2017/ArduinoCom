#!/usr/bin/env python3


class Pid:
    def interact(self, parseResults):
        def help(name):
            self.__dict__["help_" + name]()

        name = parseResults.parsed[0]
        args = parseResults.parsed[1].split()

        if len(args) == 0:
            help(name)

        elif args[0] == "get_constants":
            if len(args) != 1:
                help(name)
                return

            constants = self.s.get_appendage(name).get_constants()
            kp = constants[0]
            ki = constants[1]
            kd = constants[2]

            print("kp: {};  ki: {};  kd: {};".format(kp, ki, kd))

        elif args[0] == "set_constants":
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

            self.s.get_appendage(name).set_constants(kp, ki, kd)

        elif args[0] == "set_setpoint":
            if len(args) != 2:
                help(name)
                return

            try:
                setpoint = float(args[1])
            except ValueError:
                help(name)
                return

            self.s.get_appendage(name).set_setpoint(setpoint)

        elif args[0] == "get_values":
            if len(args) != 1:
                help(name)
                return

            values = self.s.get_appendage(name).get_values()
            input = values[0]
            output = values[1]
            setpoint = values[2]

            print("input: {:.2f};  output: {:.2f};  setpoint: {:.2f};"
                  .format(input, output, setpoint))

        elif args[0] == "off":
            if len(args) != 1:
                help(name)
                return

            self.s.get_appendage(name).off()

        else:
            help(name)

    def help(self):
        print("usage: <pid:str> get_constants")
        print("usage: <pid:str> set_constants <kp:float> <ki:float> <kd:float>")
        print("       <pid:str> set_setpoint <setpoint:float>")
        print("       <pid:str> get_values")
        print("       <pid:str> off")

    def complete(self, text, line, begidx, endidx):
        return [i for i in ["get_constants",
                            "set_constants",
                            "set_setpoint",
                            "get_values",
                            "off"] if i.startswith(text)]
