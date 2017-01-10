class Pid:
    def interact(self, parseResults):
        def help(name):
            self.__dict__["help_" + name]()

        name = parseResults.parsed[0]
        args = parseResults.parsed[1].split()

        if len(args) == 0:
            help(name)

        elif args[0] == "modify_constants":
            try:
                kp = float(args[1])
                ki = float(args[2])
                kd = float(args[3])
            except ValueError:
                help(name)
                return

            self.s.get_appendage(name).modify_constants(kp, ki, kd)

        elif args[0] == "set":
            try:
                setpoint = float(args[1])
            except ValueError:
                help(name)
                return

            self.s.get_appendage(name).set(setpoint)

        elif args[0] == "off":
            self.s.get_appendage(name).off()

        elif args[0] == "display":
            val = self.s.get_appendage(name).display()
            print("{}: {}".format(name, val))

        else:
            help(name)

    def help(self):
        print("usage: <pid:str> modify_constants <kp:float> <ki:float> <kd:float>")
        print("       <pid:str> set <setpoint:float>")
        print("       <pid:str> off")
        print("       <pid:str> display")

    def complete(self, text, line, begidx, endidx):
        return [i for i in ["modify_constants", "set", "off", "display"] if i.startswith(text)]

