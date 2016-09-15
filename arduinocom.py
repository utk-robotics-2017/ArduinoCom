import serial

class pi_to_arduino:
    def __init__(self, port):
        self.usb = serial.Serial(
                   port = port,
                   baudrate = 115200,
                   parity = serial.PARITY_ODD,
                   stopbits = serial.STOPBITS_TWO,
                   bytesize = serial.SEVENBITS
                   )
        self.usb.isOpen()

    def send(self, command):
        self.usb.write(command)

    def read(self):
        output = ''
        while self.usb.inWaiting() > 0:
            print("received")
            output += self.usb.read(1)
        if output != '':
            return out;
        else:
            return "No response"


if __name__ == "__main__":
    test = pi_to_arduino("/dev/mega")

    test.send("ping")
    print(test.read())
