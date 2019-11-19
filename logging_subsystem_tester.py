#!/usr/bin/python3
# ######################################################################
#
# Program:  logging_subsystem_tester.py
#
# Purpose:  Tester for the logging_subsystems class
#
# Notes:
#
# ######################################################################

import _env
import _utils
import sys
import logging
from time import sleep
from contextlib import redirect_stdout
import logging_subsystem

# create opscommon
# make logging and datetime imports from opscommon

def func_name():
    """
    :return: name_of_caller
    """
    return sys._getframe(1).f_code.co_name
    # end of func_name

def main():

    # TODO 2019-04-10: virtual env needs to add root directory, remove
    # need to append sys.path
    
    sys.path.append('.')

    """Illustrate usage of logging_subsystem."""
    print('starting logging subsystem test, running as main')
    # issue a couple of logging messages using root logger w/defaults
    logging.info('Setup logging subsystem')
    logging.getLogger().setLevel(logging.INFO)

    logging.critical('root logger critical example')
    logging.warning('root logger warning example')

    #
    # creating logger_subsystem instance, called loggerpp
    #
    loggerpp = logging_subsystem.LoggerPlus(logdir='logs')

    #
    # calling setLogger method, vanilla, method NOT creating a logfile
    #
    print('\nlogging init call = init()')
    loggerpp.setLogger(logdir=None)

    # Generate some log messages. ( debug should not appear )
    print('\nPhase 1 testing')
    logging.critical('*1* This function illustrates how to use the logging_subsystem extension package.')
    logging.warning('*1* All messages are sent to both the console and either to STDERR or a logfile')
    logging.warning('*1* The logfile\'s name encodes the time when the program was started as a runid.')
    logging.debug('*1* This is a sample debug message')
    logging.info('*1* This is a sample info with %s parm','string')

    # log messages to local file and messages to console
    print('\nPhase 2 testing')
    print('logging init call = init(logdir=\'logs1\')')
    loggerpp.setLogger(logdir='logs1')
    logging.critical('*2* This function illustrates how to use the logging_subsystem extension package.')
    logging.info('*2* Default loglevel is 20 (INFO)')
    logging.warning('*2* All messages are sent to both the console and either to STDERR or a logfile')
    logging.warning('*2* The logfile\'s name encodes the time when the program was started as a runid.')
    logging.debug('*2* This is a sample debug message')
    logging.info('*2* This is a sample info message')
    sleep(2)
    logging.critical('*2* This function illustrates how to use the logging_subsystem extension package.')
    logging.info('*2* Default loglevel is 20 (INFO)')
    logging.warning('*2* All messages are sent to both the console and either to STDERR or a logfile')
    logging.debug('*2* This is a sample debug message')
    logging.info('*2* This is a sample info message')
    # log messages to file in directory [logs] and messages to console
    # each call creates a new file

    sleep(2)
    print('\nPhase 3 testing')
    print('logging init call = init(logdir=\'logs\',loglevel=logging.DEBUG)')
    print('log level before setter', logging.getLogger().level)
    loggerpp.setLogger(logdir='logs',loglevel=logging.DEBUG)
    print('log level after setter', logging.getLogger().level)
    #logging.getLogger().setLevel(logging.DEBUG)
    #print('log level', logging.getLogger().level)
    logging.critical('*3* This function illustrates how to use the logging_subsystem package.')
    logging.info('*3* loglevel 10 (Debug) file should have 3 DEBUG messages from setup')
    logging.warning('*3* All messages are sent to both the console and either to STDERR or a logfile')
    logging.debug('*3* This is a sample debug message')
    logging.info('*3* This is a sample info message')
    loggerpp.setLogger(loglevel=logging.WARNING)
    logging.warning('*3* Resetting logger level to warning, next info message should NOT appear')
    logging.info('*3* Info should not be recorded')

    # log messages to file in directory [logs] and messages to console
    print('\nPhase 4 testing')
    print('logging init call = init(logdir=\'logs\',loglevel=logging.INFO)')
    loggerpp.setLogger(logdir='logs',loglevel=logging.INFO)
    logging.critical('*4* This function illustrates how to use the logging_subsystem package.')
    logging.info('*4* loglevel 10 (Debug) file should have 3 DEBUG messages from setup')
    logging.warning('*4* All messages are sent to both the console and either to STDERR or a logfile')
    logging.warning('*4* The logfile\'s name encodes the time when the program was started as a runid.')
    logging.debug('*4* This is a sample debug message')
    # end of main()

if __name__ == '__main__':
    """
        Sample main with additional functions
    """
    _env.init()
    pgmname = _env.vars['pgmname']
    print('Program Name {}'.format(_env.vars['pgmname']))

    main()
    sys.exit(0)
# end of program