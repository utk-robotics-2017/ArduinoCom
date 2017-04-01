#!/usr/bin/env python3


class UnderDampedPositionControlledMotor:
    def interact(self, parseResults):
        def help(name):
            self.__dict__["help_" + name]()

        name = parseResults.parsed[0]
        args = parseResults.parsed[1].split()

        if len(args) == 0:
            help(name)

        elif args[0] == "set_voltage":
            if len(args) != 2:
                help(name)
                return

            try:
                val = int(args[1])
            except ValueError:
                help(name)
                return

            self.s.get_appendage(name).set_voltage(val)

        elif args[0] == "set_position":
            if len(args) != 2:
                help(name)
                return

            try:
                val = float(args[1])
            except ValueError:
                help(name)
                return

            self.s.get_appendage(name).set_position(val)

        elif args[0] == "set_allowed_direction":
            if len(args) != 2:
                help(name)
                return

            if args[1] == "DIRECT":
                val = 0
            elif args[1] == "FORWARD":
                val = 0
            elif args[1] == "REVERSE":
                val = 1
            else:
                try:
                    val = int(args[1])
                except ValueError:
                    help(name)
                    return
                if val != 0:
                    val = 1

            self.s.get_appendage(name).set_allowed_direction(val)

        elif args[0] == "set_mode":
            if len(args) != 2:
                help(name)
                return

            if args[1] == "MANUAL":
                val = 0
            elif args[1] == "AUTO":
                val = 1
            else:
                try:
                    val = int(args[1])
                except ValueError:
                    help(name)
                    return

            self.s.get_appendage(name).set_mode(val)

        elif args[0] == "get_position":
            if len(args) != 1:
                help(name)
                return

            val = self.s.get_appendage(name).get_position()
            print("{}: {} degrees".format(name, val.base_value))


        elif args[0] == "get_velocity":
            if len(args) != 1:
                help(name)
                return

            val = self.s.get_appendage(name).get_velocity()
            print("{}: {} rpms".format(name, val.base_value))

        elif args[0] == "stop":
            if len(args) != 1:
                help(name)
                return

            self.s.get_appendage(name).stop()

        else:
            help(name)

    def help(self):
        print("usage: <udpcm:str> set_voltage <voltage:int>")
        print("       <udpcm:str> set_position <position:float>")
        print("       <udpcm:str> set_allowed_direction <direction:str|int>")
        print("       <udpcm:str> set_mode <mode:str|int>")
        print("       <udpcm:str> get_position")
        print("       <udpcm:str> get_velocity")
        print("       <udpcm:str> stop")
        print()
        print("direction: \"DIRECT|FORWARD|REVERSE\"")
        print("           0|1")
        print("mode: \"MANUAL|AUTO\"")
        print("      0|1")

    def complete(self, text, line, begidx, endidx):
        return [i for i in ["set_voltage", "get_position", "set_position", "set_allowed_direction", "set_mode", "get_position", "stop"]
                if i.startswith(text)]
