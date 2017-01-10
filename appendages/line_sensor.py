import time

class LineSensor:
    def interact(self, parseResults):
        def help(name):
            self.__dict__["help_" + name]()

        name = parseResults.parsed[0]
        args = parseResults.parsed[1].split()

        if len(args) == 0:
            help(name)

        elif args[0] == "set_value":
            try:
                val = int(args[1])
            except ValueError:
                help(name)
                return

            self.s.get_appendage(name).set_value(val)

        elif args[0] == "read":
            val = self.s.get_appendage(name).read()
            print("{}: {}".format(name, val))

        else:
            help(name)

    def help(self):
        print("       <line_sensor:str> set_value <value:int>")
        print("       <line_sensor:str> read")

    def complete(self, text, line, begidx, endidx):
        return [i for i in ["set_value", "read"] if i.startswith(text)]

