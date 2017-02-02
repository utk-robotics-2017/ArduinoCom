#!/usr/bin/env python3


class Arm:
    def interact(self, parseResults):
        def help(name):
            self.__dict__["help_" + name]()

        name = parseResults.parsed[0]
        args = parseResults.parsed[1].split()

        if len(args) == 0:
            help(name)

        elif args[0] == "set":
            if len(args) != 6:
                help(name)
                return

            rot = []
            try:
                for i in range(1, 6):
                    value = int(args[i])
                    if value < 0 or value > 180:
                        help(name)
                        return
                    rot.append(value)
            except ValueError:
                help(name)
                return

            self.s.get_appendage(name).set(rot)

        elif args[0] == "detach":
            if len(args) != 1:
                help(name)
                return

            self.s.get_appendage(name).detach()

        else:
            help(name)

    def help(self):
        print("usage: <arm:str> set <rot[0]> <rot[1]> <rot[2]> <rot[3]> <rot[4]>")
        print("       <arm:str> detach")
        print("")
        print("rot values: [0, 180]")

    def complete(self, text, line, begidx, endidx):
        return [i for i in ["set", "detach"] if i.startswith(text)]
