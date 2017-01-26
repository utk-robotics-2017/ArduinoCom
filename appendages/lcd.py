# arduino_com, rip, rip_com

class Lcd:
    def interact(self, parseResults):
        def help(name):
            self.__dict__["help_" + name]()

        name = parseResults.parsed[0]
        args = parseResults.parsed[1].split()

        if len(args) == 0:
            help(name)
        elif args[0] == "write":
            self.s.get_appendage(name). # whatever in rip
        elif args[0] == "clear":
        else:
            help(name)
            
    def help(self):
        print("usage: <lcd:str> write <value:str>")
        print("       <lcd:str> clear")

    def complete(self, text, line, begidx, endidx):
        return [i for i in ["write", "clear"] if i.startswith(text)]
