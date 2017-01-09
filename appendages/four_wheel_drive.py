class FourWheelDrive:
    def interact(self, parseResults):
        def help(name):
            self.__dict__["help_" + name]()

        name = parseResults.parsed[0]
        args = parseResults.parsed[1].split()

        if len(args) == 0:
            help(name)

        elif args[0] == "drive":
            if len(args) == 2:
                try:
                    all_drive = int(args[1])
                except ValueError:
                    help(name)
                    return

                self.s.get_appendage(name).drive([all_drive])

            elif len(args) == 3:
                try:
                    left_drive = int(args[1])
                    right_drive = int(args[2])
                except ValueError:
                    help(name)
                    return
                
                self.s.get_appendage(name).drive([left_drive, right_drive])

            elif len(args) == 5:
                try:
                    left_front_drive = int(args[1])
                    right_front_drive = int(args[2])
                    left_back_drive = int(args[3])
                    right_back_drive = int(args[4])
                except ValueError:
                    help(name)
                    return

                self.s.get_appendage(name).drive([left_front_drive, right_front_drive, left_back_drive, right_back_drive])

            else:
                help(name)
                return

        elif args[0] == "stop":
            self.s.get_appendage(name).stop()

        elif args[0] == "drive_pid":
            if len(args) == 2:
                try:
                    all_drive = int(args[1])
                except ValueError:
                    help(name)
                    return

                self.s.get_appendage(name).drive_pid([all_drive])

            elif len(args) == 3:
                try:
                    left_drive = int(args[1])
                    right_drive = int(args[2])
                except ValueError:
                    help(name)
                    return

                self.s.get_appendage(name).drive_pid([left_drive, right_drive])

            elif len(args) == 5:
                try:
                    left_front_drive = int(args[1])
                    right_front_drive = int(args[2])
                    left_back_drive = int(args[3])
                    right_back_drive = int(args[4])
                except ValueError:
                    help(name)
                    return

                self.s.get_appendage(name).drive_pid([left_front_drive, right_front_drive, left_back_drive, right_back_drive])

            else:
                help(name)
                return


        elif args[0] == "rotate_pid":
            if len(args) != 3:
                help(name)
                return

            try:
                left = int(args[1])
                right = int(args[2])
            except ValueError:
                help(name)
                return

            self.s.get_appendage(name).rotate_pid(left, right)

        elif args[0] == "get_left_velocity":
            val = self.s.get_appendage(name).get_left_velocity()
            print("{}: {}".format(name, val))

        elif args[0] == "get_right_velocity":
            val = self.s.get_appendage(name).get_right_velocity()
            print("{}: {}".format(name, val))

        elif args[0] == "get_left_front_velocity":
            val = self.s.get_appendage(name).get_left_front_velocity()
            print("{}: {}".format(name, val))

        elif args[0] == "get_left_back_velocity":
            val = self.s.get_appendage(name).get_left_back_velocity()
            print("{}: {}".format(name, val))

        elif args[0] == "get_right_front_velocity":
            val = self.s.get_appendage(name).get_right_front_velocity()
            print("{}: {}".format(name, val))

        elif args[0] == "get_right_back_velocity":
            val = self.s.get_appendage(name).get_right_back_velocity()
            print("{}: {}".format(name, val))

        elif args[0] == "get_left_position":
            val = self.s.get_appendage(name).get_left_position()
            print("{}: {}".format(name, val))

        elif args[0] == "get_right_position":
            val = self.s.get_appendage(name).get_right_position()
            print("{}: {}".format(name, val))

        elif args[0] == "set_pid_type":
            pid_type = args[1]

            if pid_type not in ["distance", "angle"]:
                help(name)
                return

            self.s.get_appendage(name).set_pid_type(pid_type)

        elif args[0] == "pid_get":
            val = self.s.get_appendage(name).pid_get()
            print("{}: {}".format(name, val))

        elif args[0] == "pid_set":
            try:
                val = int(args[1])
            except ValueError:
                help(name)
                return

            self.s.get_appendage(name).pid_set(val)

        else:
            help(name)
            return

    def help(self):
        print("usage: <fwd:str> drive <(all)drive_value:int>")
        print("       <fwd:str> drive <(left)drive_value:int> <(right)drive_value:int>")
        print("       <fwd:str> drive <(left_front)drive_value:int> <(right_front)drive_value:int>")
        print("                       <(left_back)drive_value:int> <(right_back)drive_value:int>")
        print("       <fwd:str> stop")
        print("       <fwd:str> drive_pid <(all)drive_value:int>")
        print("       <fwd:str> drive_pid <(left)drive_value:int> <(right)drive_value:int>")
        print("       <fwd:str> drive_pid <(left_front)drive_value:int> <(right_front)drive_value:int>")
        print("                           <(left_back)drive_value:int> <(right_back)drive_value:int>")
        print("       <fwd:str> rotate_pid <(left)drive_value:int> <(right)drive_value:int>")
        print("       <fwd:str> get_left_velocity")
        print("       <fwd:str> get_right_velocity")
        print("       <fwd:str> get_left_front_velocity")
        print("       <fwd:str> get_left_back_velocity")
        print("       <fwd:str> get_right_front_velocity")
        print("       <fwd:str> get_right_back_velocity")
        print("       <fwd:str> get_left_position")
        print("       <fwd:str> get_right_position")
        print("       <fwd:str> set_pid_type <type:str>")
        print("       <fwd:str> pid_get")
        print("       <fwd:str> pid_set <drive_value:int>")
        print("")
        print("drive_value: [-1023, 1023]")
        print("pid_type: [\"distance\", \"angle\"]")

    def complete(self, text, line, begidx, endidx):
        return [i for i in ["drive", "stop", "drive_pid", "rotate_pid",
                            "get_left_velocity", "get_right_velocity",
                            "get_left_front_velocity", "get_left_back_velocity",
                            "get_right_front_velocity", "get_right_back_velocity",
                            "get_left_position", "get_right_position",
                            "set_pid_type", "pid_get", "pid_set"] if i.startswith(text)]

