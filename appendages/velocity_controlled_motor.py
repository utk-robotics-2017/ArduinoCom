class VelocityControlledMotor:
    def interact(self, parseResults):
        def help(name):
            self.__dict__["help_" + name]()

        name = parseResults.parsed[0]
        args = parseResults.parsed[1].split()

        if len(args) == 0:
            help(name)

        elif args[0] == "drive":
            try:
                val = int(args[1])
            except ValueError:
                help(name)
                return

            self.s.get_appendage(name).drive(val)

        elif args[0] == "set":
            try:
                val = float(args[1])
            except ValueError:
                help(name)
                return

            self.s.get_appendage(name).set(val)

        elif args[0] == "get_velocity":
            val = self.s.get_appendage(name).get_velocity()
            print("{}: {}".format(name, val))

        elif args[0] == "get_position":
            val = self.s.get_appendage(name).get_position()
            print("{}: {}".format(name, val))

        elif args[0] == "set_position":
            try:
                val = float(args[1])
            except ValueError:
                help(name)
                return

            self.s.get_appendage(name).set_position(val)

        elif args[0] == "stop":
            self.s.get_appendage(name).stop()

        else:
            help(name)

    def help(self):
        print("usage: <vcm:str> drive <value:int>")
        print("       <vcm:str> set <velocity:float>")
        print("       <vcm:str> get_velocity")
        print("       <vcm:str> get_position")
        print("       <vcm:str> set_position <position:float>")
        print("       <vcm:str> stop")

    def complete(self, text, line, begidx, endidx):
        return [i for i in ["drive", "set", "get_velocity", "get_position", "set_position", "stop"] if i.startswith(text)]

