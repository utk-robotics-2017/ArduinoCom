from PyCmdMessenger import PyCmdMessenger

# configure_arduino
# get name of board grabdevice in core?
# make sure it exists
# grab config and do messages (command map / messenger)
# initialize arduino and commands

devname = input("Enter devname: ")

arduino = PyCmdMessenger.ArduinoBoard("/dev/" + devname, baud_rate=115200)

# setup
commands = [["lol",""],
            commands_config = arduino['commands']

            commands = [None] * len(commands_config)
            commands[0] = ["kAcknowledge", "i"]
            commands[1] = ["kError", "i"]
            commands[2] = ["kUnknown", ""]
            commands[3] = ["kSetLed", "?"]
            commands[4] = ["kPing", ""]
            commands[5] = ["kPingResult", "i"]
            commands[6] = ["kPong", ""]

            self.command_map[devname] = {}
            self.command_map[devname][0] = "kAcknowledge"
            self.command_map[devname][1] = "kError"
            self.command_map[devname][2] = "kUnknown"
            self.command_map[devname][3] = "kSetLed"
            self.command_map[devname][4] = "kPing"
            self.command_map[devname][5] = "kPingResult"
            self.command_map[devname][6] = "kPong"
            ["kUnknown", ""],
            ["what am i doing?", "?"]]
c = PyCmdMessenger.CmdMessenger(arduino, commands)

c.send("kUnknown")

msg = c.receive();

print(msg)
