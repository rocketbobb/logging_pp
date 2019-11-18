import os
import sys

def init():

    global vars
    vars = {}
    vars['pgmname'] = os.path.splitext(os.path.basename(sys.argv[0]))[0]


    MANDATORY_ENV_VARS = []

    for var in MANDATORY_ENV_VARS:
        if var not in os.environ:
            raise EnvironmentError("Failed because {} is not set.".format(var))
    return