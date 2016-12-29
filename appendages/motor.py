class Motor:
    def interact(self, parseResults):
        def help():
            self.__dict__["help_" + name]()

        name = parseResults.parsed[0]
        args = parseResults.parsed[1].split()

        if len(args) == 0:
            help()

        elif args[0] == "drive":
            if len(args) != 2:
                help()
                return
            try:
                value = int(args[1])
            except ValueError:
                help()
                return

            self.s.get_appendage(name).drive(value)

        elif args[0] == "stop":
            if len(args) != 1:
                help()
                return
            self.s.get_appendage(name).stop()

        else:
            help()

    def help(self):
        print("usage: <motor:str> drive <value:int>")
        print("       <motor:str> stop")

    def complete(self, text, line, begidx, endidx):
        return [i for i in ["drive", "stop"] if i.startswith(text)]

