#!/usr/bin/python3
# ######################################################################
#
# Program:  logging_subsystem.py
# Language: Python ver 3
# Author:   Bob
#
# Purpose:  logging_subsystem setups and initializes pythons logging subsystem
#           supports console and logfile recording
#           formats logfile message records according to group standard
#           datetime is ISO8601 enhanced
#           creates a runid to uniquely track each job, includes runid in log msg
#
# History:  15Nov2019 Initial creation                               RNB
#
# Notes:    Created a logging_subsystem_tester.py program to exercise class
#
# ######################################################################

"""
Example:
    >>> import logging_subsystem
    >>> import logging
    >>> loggerpp = logging_subsystem.LoggerPlus(logdir='logs')
    >>> logging.info('Test message')
"""

# Import required standard libraries.
import _env
import os
import sys
import logging
import datetime

try:
    import colorlog
    HAVE_COLORLOG = True
except ImportError:
    HAVE_COLORLOG = False

class LoggerPlus:

    # Loglevels range from 0 to 50 with 0-NOTSET to 50-Critical
    DEFAULT_LOGLEVEL = 'logging.INFO'
    DEFAULT_LOGDIR = 'logs'

    def __init__(self, logdir = None, loglevel = None):

        if logdir is None:
            self.loglevel = self.level_str_to_int(LoggerPlus.DEFAULT_LOGDIR)
        else:
            self.logdir = logdir

        if loglevel is None:
            self.loglevel = self.level_str_to_int(LoggerPlus.DEFAULT_LOGLEVEL)
        else:
            self.loglevel = self.level_str_to_int(loglevel)
        print('(init) Level >>[{}]'.format(self.loglevel))
        print('(init) Level >>[{}]'.format(self.logdir))
        """ Set up logging (console and logfile).

        When the logger class is initialized, it creates a logfile name, runid and the target logs direction, 
        if missing. The logfile name encodes creation date, time, and runid. For example "20181115-153559.txt". 
        All messages with a log level of at least "warn" are also forwarded to the console.

        Args:
            logdir (str): path of the directory where to store the log files. Both a relative or an absolute path may be 
            specified. If a relative path is specified, it is interpreted relative to the working directory.
            If no directory is given, the logs are written to a folder called "logs" in the working directory. 
        """
        # TODO 2019-04-10: add native support for syslog

        #if debug=='yes':
        #    logger.setLevel(logging.DEBUG)
        #os.environ['LOG_LEVEL']='INFO'

        # TODO add check for LOG_LEVEL in _env.vars dictionary
        #if os.environ.get('LOG_LEVEL'):
        #    loglevel=self.level_str_to_int(os.environ.get('LOG_LEVEL'))

        self.runid=datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        
        logging.debug(_env.vars['pgmname'])
        logging.debug(self.runid)
        
        if self.logdir is not None:
            self.logfile=self.logDir(self.logdir) + '/' + _env.vars['pgmname'] + '_' + self.runid + '.log'

        logging.debug(self.logfile)

        #
        # create logger  ( logger.propagate = False )
        # also add nullhandler to prevent exception on addhandler test
        #
        logging.getLogger(__name__).addHandler(logging.NullHandler())

        self.logger = logging.getLogger()   # getting root logger
        self.logger.setLevel(self.loglevel)

    def logDir(self, logdir=None):
        if logdir is not None:
            self.logdir = logdir
        # output to stderr only
        if self.isNotBlank(self.logdir):
        # TODO rnb ( except can't write) create dir for logfiles
        # TODO rnb make sure logdir is a directory
            if self.logdir == '.':
                self.logdir = ''
            else:
                self.logdir = logdir.strip().rstrip('\\/')
                if not os.path.exists(logdir):
                    try:
                        os.mkdir(logdir)
                    except OSError as exc:
                        if exc.errno != errno.EEXIST:
                            raise OSError("Can't create destinataion directory ($s)!" % (logdir))
                        pass
                #self.logdir += '/'
            print('(logdir) logdir >>{}'.format(self.logdir))
        return logdir
    
    def setLogger(self, logdir=None, loglevel=None):
        print(type(loglevel))
        print('(setter) logdir >>{}'.format(logdir))
        print('(setter) loglevel >>{}'.format(loglevel))
        # testing to see if setter called with logdir or loglevel changes
        if loglevel is not None:
            self.loglevel = self.level_str_to_int(loglevel)
        if logdir is not None:
            self.logdir = logdir
            self.logfile = self.logDir(self.logdir) + '/' + _env.vars['pgmname'] + '_' + self.runid + '.log'
        print('(setter) loglevel >>{}'.format(self.loglevel))
        # creating console handler and set level
        #
        ch = logging.StreamHandler(sys.stderr)
        ch.setLevel(self.loglevel)

        # creating file handler and set level if directory provided
        #
        fhtest=False
        chtest=False
        for handlers in self.logger.handlers:
            if isinstance(handlers,logging.FileHandler): 
                fhtest=True
                self.logger.removeHandler(handlers)
            if isinstance(handlers,logging.StreamHandler): chtest=True

        if self.logfile != None:
            fh = logging.FileHandler(self.logfile)
            fh.setLevel(self.loglevel)
            fh_formatter = logging.Formatter('%(asctime)s %(levelname)s' + ' [' + _env.vars['pgmname'] + ']' +
                    ' [' + self.runid + ']' + ' [%(module)s] %(lineno)s %(message)s', datefmt='%Y-%m-%dT%H:%M:%S%z')
            fh_formatter.default_msec_format = '%s.%03d'
            fh.setFormatter(fh_formatter)
            self.logger.addHandler(fh)
        if not chtest:

            # creating console formatter (sys.stderr)
            # formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            ch_formatter = logging.Formatter('%(levelname)s: %(message)s')

            """ TODO, add color support for log message level
            format_str = '%(asctime)s - %(levelname)-8s - %(message)s'
            date_format = '%Y-%m-%d %H:%M:%S
            if HAVE_COLORLOG:
                cformat = '%(log_color)s' + format_str
                colors = {'DEBUG': 'reset',
                        'INFO': 'reset',
                        'WARNING': 'bold_yellow',
                        'ERROR': 'bold_red',
                        'CRITICAL': 'bold_red'}
                ch_formatter = ColoredFormatter(cformat, date_format,log_colors=colors)
            """
            # add formatter to ch
            ch.setFormatter(ch_formatter)
            # add ch to logger, not sure about multiple
            self.logger.addHandler(ch)
        # debug info for the logging framework itself
        logging.debug('logging_pp setup complete')
        logging.debug('loglevel [{}]'.format(loglevel))
        logging.debug('logfilename [{}]'.format(self.logfile))

        return

    # remap log level string to int
    def level_str_to_int(self, arg):
        print('(level_str_to_int) {}'.format(arg))
        print('(level_str_to_int) {}'.for)
        """
        remapping logging.<level> into level as per logging package requirements
        TODO validate range, may be a simpler way
        """
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

    def isBlank(self, s):
        return not (s and s.strip())

    def isNotBlank(self, s):
        return s and s.strip()

def main():
    # creating loggerplus instance
    loggerpp = LoggerPlus()

    # end of main()

if __name__ == '__main__':
    
    import _env
    _env.init()
    pgmname = _env.vars['pgmname']
    print('Program Name {}'.format(_env.vars['pgmname']))
    
    main()
    # end of main
