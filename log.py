#!/usr/bin/env python3

import sys
import traceback
import datetime

import logging

logging.basicConfig(format='\r[%(asctime)s] [%(levelname)s]: %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG
                    )

# Light Blue
logging.addLevelName(logging.INFO, "\033[1;94m%s\033[1;0m" % logging.getLevelName(logging.INFO))
# Yellow
logging.addLevelName(logging.WARNING, "\033[1;33m%s\033[1;0m" % logging.getLevelName(logging.WARNING))
# Red
logging.addLevelName(logging.ERROR, "\033[1;31m%s\033[1;0m" % logging.getLevelName(logging.ERROR))
# Inverted Red
logging.addLevelName(logging.CRITICAL, "\033[1;41m%s\033[1;0m" % logging.getLevelName(logging.CRITICAL))

DEBUG_APPLICATION = False
DEBUG_LEVEL = 0
LOG_TRACES = False


class bcolors:
    PURPLE_H = '\033[95m'  # High Purple
    BLUE = '\033[34m'
    SUCCESS = '\033[32m'  # Norm Green
    DEBUG = '\033[90m'  # Grey
    INFO = '\033[37m'  # # Norm White
    WARNING = '\033[93m'  # High Yellow
    CRITICAL = '\033[91m'  # High Red
    ENDC = '\033[0m'  # Reset
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def debug(message):
    if DEBUG_APPLICATION:
        logging.debug(message)
    return wrap_end(bcolors.DEBUG + "[DEBUG] " + message)


def debug1(message):
    if DEBUG_LEVEL >= 1:
        # print(bcolors.DEBUG + "[DEBUG1] " + message + bcolors.ENDC)
        logging.debug(message)


def debug2(message):
    if DEBUG_LEVEL >= 2:
        # print(bcolors.DEBUG + "[DEBUG2] " + message + bcolors.ENDC)
        logging.debug(message)


def debug3(message):
    if DEBUG_LEVEL >= 3:
        # print(bcolors.DEBUG + "[DEBUG3] " + message + bcolors.ENDC)
        logging.debug(message)


# Multi-line debugging output
# If the message includes a \n, you should use this
def trace(message):
    if DEBUG_APPLICATION and LOG_TRACES:
        # print(bcolors.DEBUG + "[TRACE] BEGIN >>> " + bcolors.ENDC)
        for line in message.split("\n"):
            print(bcolors.DEBUG + "[TRACE] " + line + bcolors.ENDC)
            logging.debug(line)
        # print(bcolors.DEBUG + "[TRACE] END <<<" + bcolors.ENDC)


def info(message):
    logging.info(message)
    return wrap_end(bcolors.INFO + "[INFO] " + message)


def warn(message):
    logging.warning(message)
    return wrap_end(bcolors.WARNING + "[WARN] " + message)


def warning(message):
    # Just an alias
    warn(message)


def error(message):
    logging.error(message)
    return wrap_end(bcolors.CRITICAL + "[ERROR] " + message)


def fatal(message):
    logging.critical(message)
    return wrap_end(bcolors.CRITICAL + "[FATAL] " + message)


def gettimestamp():
    return '[{:%Y-%m-%d_%H:%M:%S}]'.format(datetime.datetime.now())


def wrap_end(message):
    return wrap(message) + bcolors.ENDC


def wrap(message):
    return gettimestamp() + message


if __name__ == "__main__":
    logging.debug("Debug info")
    logging.info("Info info, with info")
    logging.warning("Warning info")
    logging.error("Error info")
    logging.critical("Critical info")

    logging.info("Timestamp: " + gettimestamp())
