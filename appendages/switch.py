class Switch:
    def interact(self, parseResults):
        def help(name):
            self.__dict__["help_" + name]()

        name = parseResults.parsed[0]
        args = parseResults.parsed[1].split()

        if len(args) == 0:
            help(name)

        elif args[0] == "read":
            if len(args) != 1:
                help(name)
                return

            val = self.s.get_appendage(name).read()
            print("{}: {}".format(name, val))

        elif args[0] == "read_until_change":
            if len(args) != 1:
                help(name)
                return

            val = self.s.get_appendage(name).read()
            print("{} start state: {}".format(name, val))
            time.sleep(0.1)

            while val == self.s.get_appendage(name).read():
                time.sleep(0.1)
            print("{} state changed".format(name, val))

        else:
            help(name)

    def help(self):
        print("usage: <switch:str> read")
        print("       <switch:str> read_until_change")
        print("")
        print("value: [-1023, 1023]")

    def complete(self, text, line, begidx, endidx):
        return [i for i in ["read", "read_until_change"] if i.startswith(text)]

