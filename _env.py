# ######################################################################
# 
# Program:  _env.py
# Language: Python ver 3
# Author:   Bob
#
# Purpose:  Create global dictionary contains select global environment 
#           variables
#
# History:  18Nov2019 Initial creation                               RNB
#
# Notes:
#
# ######################################################################

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