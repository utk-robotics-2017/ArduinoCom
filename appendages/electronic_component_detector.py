class ElectronicComponentDetector:
    def interact(self, parseResults):
        def help(name):
            self.__dict__["help_" + name]()

        name = parseResults.parsed[0]
        args = parseResults.parsed[1].split()

        if len(args) == 0:
            help(name)

        elif args[0] == "decode":
            pad = -1
            if len(args) == 0:
                help(name)
                return
            if len(args) == 1:
                pad = 9
            if len(args) == 2:
                try:
                    pad = int(args[1])
                except ValueError:
                    help(name)
                    return

                if pad not in [0, 1, 2, 3, 4, 9]:
                    help(name)
                    return
            else:
                help(name)
                return

            val = self.s.get_appendage(name).decode(pad=str(pad))[0]
            code = []
            for i in range(5):
                code.append(val >> (i * 3) & 7)
            print("{0:s}: raw: {1:d}, raw_b: {2:s}, {3:s} , decoded: {4:s}".format(
                name,
                val,
                "".join(str(val >> (15 - i) & 1) for i in range(16)),
                "{} ".format(val >> 15 & 1) +
                    " ".join("{:03b}".format(i) for i in reversed(code)),
                "".join(str(i) for i in code)))

        else:
            help(name)

    def help(self):
        print("usage: <ECD:str> decode")
        print("usage: <ECD:str> decode <pad:int>")
        print("")
        print("pad: [0, 1, 2, 3, 4, 9]")

    def complete(self, text, line, begidx, endidx):
        return [i for i in ["decode"] if i.startswith(text)]

