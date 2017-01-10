class Stepper:
    def interact(self, parseResults):
        def help(name):
            self.__dict__["help_" + name]()

        name = parseResults.parsed[0]
        args = parseResults.parsed[1].split()

        if len(args) == 0:
            help(name)

        elif args[0] == "set_distance":
            try:
                val = float(args[1])
            except ValueError:
                help(name)
                return

            self.s.get_appendage(name).set_distance(val)

        elif args[0] == "read":
            val = self.s.get_appendage(name).read()
            print("{}: {}".format(name, val))

        else:
            help(name)

    def help(self):
        print("usage: <pid:str> set_distance <distance:float>")
        print("       <pid:str> read")

    def complete(self, text, line, begidx, endidx):
        return [i for i in ["set_distance", "read"] if i.startswith(text)]

