#!/usr/bin/env python3

import sys
import random
import time
# import json
import signal
# import socket
# import os
# import os.path

import tornado.ioloop
import tornado.websocket
import tornado.httpserver

# We are not ArduinoGen, we are ArduinoCom.
# from ArduinoGen import ArduinoGen

clients = set()
clientId = 0

port = 9000

# Now ensures that the pin is always 5 numbers.
pin = random.randint(10000, 99999)


# Generic log function for timestamping
def log(wsId, message):
    print(("{}\tClient {:2d}\t{}".format(
        time.strftime("%H:%M:%S", time.localtime()), wsId, message
    )))


class arduinoCom(tornado.websocket.WebSocketHandler):
    # Not sure what this does...
    def check_origin(self, origin):
        return True

    # Opens a new connection for a client, and adds it to our clients.
    def open(self):
        global clients, clientId

        self.id = clientId
        clientId += 1
        clients.add(self)

        self.verified = False

        log(self.id, "connected with ip: " + self.request.remote_ip)

    # Main function for all incoming data and messages,
    def on_message(self, message):
        if not self.verified:
            # User is not verified, try to verify using a PIN.
            try:
                clientPin = int(message)
            except ValueError:  # Wrong PIN,
                self.write_message("Invalid Pin")
                log(self.id, "entered an invalid pin: " + message)
                return

            if clientPin == pin:  # Client pin matches
                self.verified = True
                self.write_message("Verified")
                log(self.id, "entered correct pin")
            else:
                self.write_message("WrongPin")
                log(self.id, "entered wrong pin")

            self.write_message("Verified")

        else:  # This means the user is verified.
            # TODO things
            if message.startswith("PostMessage"):
                self.write_message("PrintMessage" + "Your POST message: " +
                                   message.replace("PostMessage", "", 1))
            # This is the case when we don't cover that input function
            else:
                self.write_message("PrintMessage" +
                                   "Command did not match any action, doing nothing.")
                log("Command was not used: " + message)

        ''' # Code from ArduinoGen, not for ArduinoCom
            cmd = "Lock"
            if message[:len(cmd)] == cmd:
                if hasattr(self, 'device'):
                    self.write_message("ClientHasLock")
                    log(self.id, "tried to lock, but already has a device lock")
                else:
                    devName = message[len(cmd):]

                    dev = list([x for x in arduinos if x["name"] == devName])
                    if len(dev):
                        dev = dev[0]
                    else:
                        self.write_message("DeviceNotRegistered")
                        log(self.id, devName + " device not registered")
                        return

                    if dev["locked"]:
                        self.write_message("DeviceInUse")
                        log(self.id, devName + " device is in use")
                    else:
                        dev["locked"] = True
                        self.device = dev
                        lockFileName = lockFolderAbsPath + "/" + self.device["name"] + ".lck"
                        with open(lockFileName, "w") as f:
                            f.write("Locked by ArduinoGenServer")

                        for client in clients:
                            client.write_message("DeviceList" + json.dumps(arduinos))
                        log(self.id, "updated devices")

                        self.write_message("LockedDevice" + devName)
                        log(self.id, "locked " + devName)
                return

            cmd = "Unlock"
            if message[:len(cmd)] == cmd:
                if not hasattr(self, 'device'):
                    self.write_message("ClientNoLock")
                    log(self.id, "tried to unlock, but doesn't have a device lock")
                else:
                    lockFileName = lockFolderAbsPath + "/" + self.device["name"] + ".lck"
                    os.remove(lockFileName)
                    self.device["locked"] = False
                    self.write_message("UnlockedDevice" + self.device["name"])
                    log(self.id, "unlocked " + self.device["name"])
                    del self.device

                    for client in clients:
                        client.write_message("DeviceList" + json.dumps(arduinos))
                    log(self.id, "updated devices")
                return

            cmd = "GetComponents"
            if message[:len(cmd)] == cmd:
                if not hasattr(self, 'device'):
                    self.write_message("ClientNoLock")
                    log(self.id, "tried to get components, but doesn't have a device lock")
                else:
                    deviceJsonFile = confFolderAbsPath + "/" + self.device["name"] + ".json"
                    if not os.path.exists(deviceJsonFile):
                        self.write_message("[]")
                        log(self.id, "no file, sending empy list")
                    else:
                        with open(deviceJsonFile, 'r') as jsonFile:
                            jsonData = jsonFile.read().replace('\n', '')
                            self.write_message("ComponentList" + jsonData)
                            log(self.id, "requested " + self.device["name"] + "'s components")
                return

            cmd = "PostComponents"
            if message[:len(cmd)] == cmd:
                if not hasattr(self, 'device'):
                    self.write_message("ClientNoLock")
                    log(self.id, "tried to post components, but doesn't have a device lock")
                else:
                    deviceJsonFile = confFolderAbsPath + "/" + self.device["name"] + ".json"
                    with open(deviceJsonFile, 'w') as jsonFile:
                        jsonFile.write(message[len(cmd):])
                        self.write_message("PostedComponents")
                        log(self.id, "posted " + self.device["name"] + "'s components")
                return

            cmd = "GenCode"
            if message[:len(cmd)] == cmd:
                if not hasattr(self, 'device'):
                    self.write_message("ClientNoLock")
                    log(self.id, "tried to generate arduino code, but doesn't have a device lock")
                else:
                    deviceJsonFile = confFolderAbsPath + "/" + self.device["name"] + ".json"
                    with open(deviceJsonFile, 'w') as jsonFile:
                        jsonFile.write(message[len(cmd):])
                        self.write_message("PostedComponents")
                        log(self.id, "posted " + self.device["name"] + "'s components")

                    log(self.id, "generating arduino code for " + self.device["name"])

                    ag = ArduinoGen(arduino=self.device["name"])
                    ag.setParentFolder(os.path.dirname(os.path.realpath(__file__)))
                    ag.setupFolder()
                    ag.readConfig(deviceJsonFile)
                    ag.generateOutput()
                    log(self.id, "generated arduino code for " + self.device["name"])
                    self.write_message("GeneratedArduinoCode")
                return

            cmd = "WriteComponents"
            if message[:len(cmd)] == cmd:
                if not hasattr(self, 'device'):
                    self.write_message("ClientNoLock")
                    log(self.id, "tried to write components, but doesn't have a device lock")
                else:
                    deviceJsonFile = confFolderAbsPath + "/" + self.device["name"] + ".json"
                    with open(deviceJsonFile, 'w') as jsonFile:
                        jsonFile.write(message[len(cmd):])
                        self.write_message("PostedComponents")
                        log(self.id, "posted " + self.device["name"] + "'s components")

                    log(self.id, "writing components to " + self.device["name"])

                    ag = ArduinoGen(arduino=self.device["name"])
                    ag.setParentFolder(os.path.dirname(os.path.realpath(__file__)))
                    ag.setupFolder()
                    ag.readConfig(deviceJsonFile)
                    ag.generateOutput()
                    ag.upload()
                    log(self.id, "written components to " + self.device["name"])
                    self.write_message("WrittenComponents")
                return
        '''

    def on_close(self):
        # When the client closes the connection,
        # We should free any resources they had locked.

        # Remove the client from the list.
        clients.remove(self)
        log(self.id, "disconnected")

        '''
        if hasattr(self, 'device'):
            dev = self.device
            dev["locked"] = False
            lockFileName = lockFolderAbsPath + "/" + dev["name"] + ".lck"
            os.remove(lockFileName)
            log(self.id, "unlocked " + dev["name"])

            clients.remove(self)

            for client in clients:
                client.write_message("DeviceList" + json.dumps(arduinos))
            log(self.id, "updated devices")
        else:
            clients.remove(self)

        log(self.id, "disconnected")
        '''


class SetupTLS(tornado.web.RequestHandler):
    def get(self):
        self.write("Please accept the TLS certificate to use websockets from this device.")


def make_app():
    return tornado.httpserver.HTTPServer(tornado.web.Application([
        (r"/", arduinoCom),
        (r"/setuptls", SetupTLS)
    ]))  # , ssl_options={
    #     "certfile": "/etc/ssl/certs/tornado.crt",
    #     "keyfile": "/etc/ssl/certs/tornado.key"
    # })


def sigInt_handler(signum, frame):
    print("Closing Server")

    while clients:
        client = next(iter(clients))
        client.close(reason="Server Closing")
        # client.on_close()

    tornado.ioloop.IOLoop.current().stop()
    print("Server is closed")
    sys.exit(0)


if __name__ == "__main__":
    app = make_app()
    app.listen(port)
    signal.signal(signal.SIGINT, sigInt_handler)
    print(("Pin: {:05d}".format(pin)))
    tornado.ioloop.IOLoop.current().start()
