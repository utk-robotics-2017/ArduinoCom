#!/usr/bin/env python3

import os
import types
import logging

try:
    from cmd2 import Cmd  # , options, make_option
except ImportError as err:
    print("Maybe you should pip3 install cmd2 (the better cmd class)")

try:
    from rip.head.spine.core import get_spine

    from rip.head.spine.appendages.motor import Motor as SpineMotor
    from rip.head.spine.appendages.switch import Switch as SpineSwitch
    from rip.head.spine.appendages.servo import Servo as SpineServo
    from rip.head.spine.appendages.electronic_component_detector import ElectronicComponentDetector as SpineElectronicComponentDetector
    from rip.head.spine.appendages.encoder import Encoder as SpineEncoder
    from rip.head.spine.appendages.arm import Arm as SpineArm
    from rip.head.spine.appendages.four_wheel_drive import FourWheelDrive as SpineFourWheelDrive
    from rip.head.spine.appendages.i2c_encoder import I2CEncoder as SpineI2CEncoder
    from rip.head.spine.appendages.line_sensor import LineSensor as SpineLineSensor
    from rip.head.spine.appendages.pid import Pid as SpinePid
    from rip.head.spine.appendages.stepper import Stepper as SpineStepper
    from rip.head.spine.appendages.ultrasonic import Ultrasonic as SpineUltrasonic
    from rip.head.spine.appendages.velocity_controlled_motor import VelocityControlledMotor as SpineVelocityControlledMotor
except ImportError as err:
    print("Unable to import one or more RIP appendages,")
    print("Ensure submodules are up to date, try: git submodule update --init --recursive")
    print("Ensure imports can find the RIP instance,\n envvar PYTHONPATH=\"path/to/folder/with/rip\" can be used.")
    print("Specific Error: " + str(err))

# RipCom-specific things.
try:
    from appendages.motor import Motor as RCMotor
    from appendages.switch import Switch as RCSwitch
    from appendages.servo import Servo as RCServo
    from appendages.electronic_component_detector import ElectronicComponentDetector as RCElectronicComponentDetector
    from appendages.encoder import Encoder as RCEncoder
    from appendages.arm import Arm as RCArm
    from appendages.four_wheel_drive import FourWheelDrive as RCFourWheelDrive
    from appendages.i2c_encoder import I2CEncoder as RCI2CEncoder
    from appendages.line_sensor import LineSensor as RCLineSensor
    from appendages.pid import Pid as RCPid
    from appendages.stepper import Stepper as RCStepper
    from appendages.ultrasonic import Ultrasonic as RCUltrasonic
    from appendages.velocity_controlled_motor import VelocityControlledMotor as RCVelocityControlledMotor
except ImportError as err:
    print("Couldn't import a rip_com appendage.")
    print("This should be reported to the rip_com maintainer(s):")
    print(str(err))

# Points to the current robot's code.
CURRENT_ARDUINO_CODE_DIR = "/Robot/CurrentArduinoCode"


class ArduinoCom(Cmd):
    intro = "Welcome to RipCom. Type help or ? for commands.\nCtrl-D to exit."
    prompt = "[RC]> "
    doc_header = "Documentation available for:"
    undoc_header = "Not documented:"
    gs = None
    s = None
    appendages = None

    def __init__(self):
        super().__init__()
        self.registeredDevices = [d for d in os.listdir(CURRENT_ARDUINO_CODE_DIR)
                                  if os.path.isdir("{0:s}/{1:s}".format(CURRENT_ARDUINO_CODE_DIR, d)) and
                                  not d == ".git" and os.path.exists("{0:s}/{1:s}/{1:s}.json"
                                                                     .format(CURRENT_ARDUINO_CODE_DIR, d))]
        self.connectedDevices = [d for d in self.registeredDevices
                                 if os.path.exists("/dev/{0:s}".format(d))]

    def do_connect(self, parseResults):
        args = parseResults.parsed[1].split()
        if len(args) != 1:
            self.help_connect()
            return
        arduinoName = args[0]

        if arduinoName not in self.connectedDevices:
            print("Arduino \"{}\" is not available.".format(arduinoName))
            return

        self.gs = get_spine(devices=[arduinoName])
        self.s = self.gs.__enter__()
        self.appendages = self.s.get_appendage_dict()

        def registerMethods(RCClass):
            self.__dict__["do_" + name] = types.MethodType(RCClass.interact, self)
            self.__dict__["help_" + name] = types.MethodType(RCClass.help, self)
            self.__dict__["complete_" + name] = types.MethodType(RCClass.complete, self)

        # TODO There should be a better way to do this than to register each one hardcoded.
        for name, appendage in self.appendages.items():
            if isinstance(appendage, SpineMotor):
                registerMethods(RCMotor)
            elif isinstance(appendage, SpineSwitch):
                registerMethods(RCSwitch)
            elif isinstance(appendage, SpineServo):
                registerMethods(RCServo)
            elif isinstance(appendage, SpineElectronicComponentDetector):
                registerMethods(RCElectronicComponentDetector)
            elif isinstance(appendage, SpineEncoder):
                registerMethods(RCEncoder)
            elif isinstance(appendage, SpineArm):
                registerMethods(RCArm)
            elif isinstance(appendage, SpineFourWheelDrive):
                registerMethods(RCFourWheelDrive)
            elif isinstance(appendage, SpineI2CEncoder):
                registerMethods(RCI2CEncoder)
            elif isinstance(appendage, SpineLineSensor):
                registerMethods(RCLineSensor)
            elif isinstance(appendage, SpinePid):
                registerMethods(RCPid)
            elif isinstance(appendage, SpineStepper):
                registerMethods(RCStepper)
            elif isinstance(appendage, SpineUltrasonic):
                registerMethods(RCUltrasonic)
            elif isinstance(appendage, SpineVelocityControlledMotor):
                registerMethods(RCVelocityControlledMotor)

    def help_connect(self):
        print("usage: connect <ArduinoName>")
        print("Normally, ArduinoName could be something as simple as 'mega'")

    def complete_connect(self, text, line, begidx, endidx):
        return [i for i in self.connectedDevices if i.startswith(text)]

    def do_disconnect(self, parseResults):
        if self.appendages is not None:
            for name in self.appendages:
                del self.__dict__["do_" + name]
                del self.__dict__["help_" + name]
                del self.__dict__["complete_" + name]
            self.appendages = None

            self.gs.__exit__(None, None, None)
            self.s = None
            self.gs = None

    def help_disconnect(self):
        print("usage: disconnect")
        print("Disconnects from a connected arduino.")

    def do_exit(self, parseResults):
        self.do_disconnect(None)
        return True

    def help_exit(self):
        print("Disconnects from any connected arduinos, and exits ArduinoCom.")

    def do_quit(self, parseResults):
        return self.do_exit(parseResults)

    def help_quit(self):
        print("Alias for exit")

    def do_EOF(self, parseResults):
        print()
        return self.do_exit(parseResults)
    do_eof = do_EOF

    def help_help(self):
        print("Prints help for commands")

    def get_names(self):
        names = dir(self)
        names.remove("do_EOF")
        names.remove("do_eof")
        names.remove("do_q")
        return names


# Initializes the command interface loop on the terminal.
# Uses __main__ detection so that this file can be used as an import from other pys.
if __name__ == '__main__':
    rc = ArduinoCom()
    rc.debug = True
    rc.case_insensitive = True
    logging.disable(logging.INFO)
    rc.cmdloop()
