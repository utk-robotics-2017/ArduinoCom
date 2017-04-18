#!/usr/bin/env python3


class I2CEncoder:
    def interact(self, parseResults):
        def help(name):
            self.__dict__["help_" + name]()

        name = parseResults.parsed[0]
        args = parseResults.parsed[1].split()

        if len(args) == 0:
            help(name)

        elif args[0] == "set_pid_source":
            if len(args) != 2:
                help(name)
                return

            pid_source = args[1]

            if pid_source not in ["position", "velocity"]:
                help(name)
                return

            self.s.get_appendage(name).set_pid_source(pid_source)

        elif args[0] == "get_position":
            if len(args) != 1:
                help(name)
                return

            val = self.s.get_appendage(name).get_position()
            print("{}: {:.2f}".format(name, val.base_value))

        elif args[0] == "raw_position":
            if len(args) != 1:
                help(name)
                return

            val = self.s.get_appendage(name).raw_position()
            print("{}: {:d}".format(name, int(val)))

        elif args[0] == "get_speed":
            if len(args) != 1:
                help(name)
                return

            val = self.s.get_appendage(name).get_speed()
            print("{}: {}".format(name, val.base_value))

        elif args[0] == "get_velocity":
            if len(args) != 1:
                help(name)
                return

            val = self.s.get_appendage(name).get_velocity()
            print("{}: {}".format(name, val.base_value))

        elif args[0] == "zero":
            if len(args) != 1:
                help(name)
                return

            self.s.get_appendage(name).zero()

        elif args[0] == "pid_get":
            if len(args) != 1:
                help(name)
                return

            val = self.s.get_appendage(name).pid_get()
            print("{}: {}".format(name, val.base_value))

        else:
            help(name)

    def help(self):
        print("usage: <i2c_encoder:str> set_pid_source <source:str>")
        print("       <i2c_encoder:str> get_position")
        print("       <i2c_encoder:str> raw_position")
        print("       <i2c_encoder:str> get_speed")
        print("       <i2c_encoder:str> get_velocity")
        print("       <i2c_encoder:str> zero")
        print("       <i2c_encoder:str> pid_get")
        print("")
        print("pid_source:   [\"position\", \"velocity\"]")
        print("position:     degrees")
        print("raw_position: ticks")
        print("velocity:     rpm")

    def complete(self, text, line, begidx, endidx):
        return [i for i in ["set_pid_source", "get_position",
                            "raw_position", "get_speed",
                            "get_velocity", "zero", "pid_get"] if i.startswith(text)]
