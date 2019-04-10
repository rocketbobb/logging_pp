#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Duallog

This module contains a function "logging_pp_init()" that sets up file and console logging. All subsequent 
log messages are sent both to the console and to a logfile. Log messages are generated via the "logging" package.

Example:
    >>> import logging_pp
    >>> import logging
    >>> logging_pp.init('mylogs')
    >>> logging.info('Test message')

If run as main, this module illustrates the usage of logging_pp package.
"""

# Import required standard libraries.
import os
import sys
import logging
import datetime

def init(logdir=None, loglevel=logging.INFO):
    """ Set up ops logging (console and logfile).

    When this function is called, it first creates the given directory. It then creates 
    a logfile and passes all log messages to come to it. The logfile name encodes the date
    and time when it was created, for example "20181115-153559.txt". All messages with a
    log level of at least "warn" are also forwarded to the console.

    Args:
        logdir (str): path of the directory where to store the log files. Both a relative or an absolute path may be 
        specified. If a relative path is specified, it is interpreted relative to the working directory.
        If no directory is given, the logs are written to a folder called "logs" in the working directory. 
    """
    # TODO 2019-04-10: add support for syslog

    def isBlank (s):
        return not (s and s.strip())

    def isNotBlank (s):
        return s and s.strip()
    
    # remap log level string to int
    def level_str_to_int(arg):
        switcher = {
            'NOTSET': 0,
            'DEBUG':  10,
            'INFO':   20,
            'WARNING': 30,
            'WARN': 30,
            'ERROR': 40,
            'CRITICAL': 50,
        }
        return switcher.get(arg, 20) 

    #if debug=='yes':
    #    logger.setLevel(logging.DEBUG)
    
    #os.environ['LOG_LEVEL']='INFO'
    if os.environ.get('LOG_LEVEL'):
        loglevel=level_str_to_int(os.environ.get('LOG_LEVEL'))

    pgmname = os.path.splitext(os.path.basename(sys.argv[0]))[0]
    runid=datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    
    logging.debug(pgmname)
    logging.debug(runid)
    
    # output to stderr
    if isBlank(logdir):
        logfile=None
    else:
    # rnb ( except can't write) create dir for logfiles
    # rnb make sure logdir is a directory
        if logdir == '.':
            logdir = ''
        else:
            logdir = logdir.strip().rstrip('\\/')
            if not os.path.exists(logdir):
                os.mkdir(logdir)
            logdir += '/'
        logfile=logdir + pgmname + '_' + runid + '.log'

    #
    # create logger  ( logger.propagate = False )
    # also add nullhandler to prevent exception on addhandler test
    #
    logging.getLogger(__name__).addHandler(logging.NullHandler())

    logger = logging.getLogger()   # getting root logger
    logger.setLevel(loglevel)

    # create console handler and set level
    ch = logging.StreamHandler(sys.stderr)
    ch.setLevel(loglevel)

    #
    # create file handler and set level if directory provided
    # 
    fhtest=False
    chtest=False
    for handlers in logger.handlers:
        if isinstance(handlers,logging.FileHandler): 
            fhtest=True
            logger.removeHandler(handlers)
        if isinstance(handlers,logging.StreamHandler): chtest=True
    
    if logfile != None:
        fh = logging.FileHandler(logfile)
        fh.setLevel(loglevel)
        fh_formatter = logging.Formatter('%(asctime)s %(levelname)s' + ' [' + pgmname + '] ' + '[%(funcName)s] %(message)s', datefmt='%Y-%m-%dT%I:%M:%S.%06d%z')
        fh.setFormatter(fh_formatter)
        logger.addHandler(fh)

    if not chtest:
        # create console formatter (sys.stderr)           
        # formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch_formatter = logging.Formatter('%(levelname)s: %(message)s')
        # add formatter to ch
        ch.setFormatter(ch_formatter)
        # add ch to logger   not sure about multiple
        logger.addHandler(ch)

    # logging framework debug info
    logging.debug('logging_pp setup complete')
    logging.debug('loglevel [{}]'.format(loglevel))
    logging.debug('logfilename [{}]'.format(logfile))
# end of init

if __name__ == '__main__':
    #sys.path.append('.')
    import logging_pp
    """Illustrate usage of logging_pp."""

    # issue a couple of logging messages using root logger w/defaults
    logging.critical('root logger example1')
    logging.warning('root logger example2')

    # log messages to stderr, messages to console, defaults to INFO
    #logging_pp.init()
    init()
    # Generate some log messages. ( debug should not appear )
    logging.critical('*1* This function illustrates how to use the ops_logging package.')
    logging.warn('All messages are sent to both the console and either to STDERR or a logfil')
    logging.warn('The logfile\'s name encodes the time when the program was started as a runid.')
    logging.debug('This is a sample debug message')
    logging.info('This is a sample info with %s parm','string')

    # log messages to local file and messages to console
    logging_pp.init(logdir='.')
    logging.critical('*2* This function illustrates how to use the ops_logging package.')
    logging.info('Default loglevel is 20 (INFO)')
    logging.warn('All messages are sent to both the console and either to STDERR or a logfil')
    logging.warn('The logfile\'s name encodes the time when the program was started as a runid.')
    logging.debug('This is a sample debug message')
    logging.info('This is a sample info message')

    # log messages to file in directory [logs] and messages to console
    # each call creates a new file
    logging_pp.init(logdir='logs',loglevel=10)
    logging.critical('*3* This function illustrates how to use the ops_logging package.')
    logging.info('loglevel 10 (Debug) file should have 3 DEBUG messages from setup')
    logging.warn('All messages are sent to both the console and either to STDERR or a logfil')
    logging.warn('The logfile\'s name encodes the time when the program was started as a runid.')
    logging.debug('This is a sample debug message')
    logging.info('This is a sample info message')
    logging.getLogger().setLevel(logging.WARNING)
    logging.warn('Resetting logger level to warning, next info message should NOT appear')
    logging.info('Info should not be recorded')

    # log messages to file in directory [logs] and messages to console
    logging_pp.init(logdir='logs',loglevel=30)
    logging.critical('*4* This function illustrates how to use the ops_logging package.')
    logging.info('loglevel 10 (Debug) file should have 3 DEBUG messages from setup')
    logging.warn('All messages are sent to both the console and either to STDERR or a logfil')
    logging.warn('The logfile\'s name encodes the time when the program was started as a runid.')
    logging.debug('This is a sample debug message')

    # end of main
