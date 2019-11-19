#!/usr/bin/python3
import _env
import sys
import os
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

    # creating loggerplus instance
    loggerpp = logging_subsystem.LoggerPlus(logdir='logs')

    # log messages to local file and messages to console
    logging.info('Setup logging subsystem')
    logging.getLogger().setLevel(logging.INFO)

    """Illustrate usage of logging_subsystem."""
    print('starting logging subsystem test, running as main')
    # issue a couple of logging messages using root logger w/defaults
    logging.critical('root logger example1')
    logging.warning('root logger example2')

    # log messages to stderr, messages to console, defaults to INFO
    #logging_subsystem.init()

    print('\nlogging init call = init()')
    loggerpp.setLogger()
    # Generate some log messages. ( debug should not appear )
    logging.critical('*1* This function illustrates how to use the logging_subsystem extension package.')
    logging.warning('All messages are sent to both the console and either to STDERR or a logfile')
    logging.warning('The logfile\'s name encodes the time when the program was started as a runid.')
    logging.debug('This is a sample debug message')
    logging.info('This is a sample info with %s parm','string')

    # log messages to local file and messages to console
    print('\nlogging init call = init(logdir=\'logs\')')
    loggerpp.setLogger(logdir='logs')
    logging.critical('*2* This function illustrates how to use the logging_subsystem extension package.')
    logging.info('Default loglevel is 20 (INFO)')
    logging.warning('All messages are sent to both the console and either to STDERR or a logfile')
    logging.warning('The logfile\'s name encodes the time when the program was started as a runid.')
    logging.debug('This is a sample debug message')
    logging.info('This is a sample info message')
    sleep(2)
    logging.critical('*2* This function illustrates how to use the logging_subsystem extension package.')
    logging.info('Default loglevel is 20 (INFO)')
    logging.warning('All messages are sent to both the console and either to STDERR or a logfile')
    logging.warning('The logfile\'s name encodes the time when the program was started as a runid.')
    logging.debug('This is a sample debug message')
    logging.info('This is a sample info message')    
    # log messages to file in directory [logs] and messages to console
    # each call creates a new file

    sleep(2)
    print('\nlogging init call = init(logdir=\'logs\',loglevel=10)')
    loggerpp.setLogger(logdir='logs',loglevel=10)
    logging.critical('*3* This function illustrates how to use the logging_subsystem package.')
    logging.info('loglevel 10 (Debug) file should have 3 DEBUG messages from setup')
    logging.warning('All messages are sent to both the console and either to STDERR or a logfile')
    logging.warning('The logfile\'s name encodes the time when the program was started as a runid.')
    logging.debug('This is a sample debug message')
    logging.info('This is a sample info message')
    logging.getLogger().setLevel(logging.WARNING)
    logging.warning('Resetting logger level to warning, next info message should NOT appear')
    logging.info('Info should not be recorded')

    # log messages to file in directory [logs] and messages to console
    print('\nlogging init call = init(logdir=\'logs\',loglevel=30)')
    loggerpp.setLogger(logdir='logs',loglevel=30)
    logging.critical('*4* This function illustrates how to use the logging_subsystem package.')
    logging.info('loglevel 10 (Debug) file should have 3 DEBUG messages from setup')
    logging.warning('All messages are sent to both the console and either to STDERR or a logfile')
    logging.warning('The logfile\'s name encodes the time when the program was started as a runid.')
    logging.debug('This is a sample debug message')
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