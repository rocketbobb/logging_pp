#!/usr/bin/python3
import sys
import os
import io
import logging
from datetime import datetime 
from contextlib import redirect_stdout

# create opscommon
# make logging and datetime imports from opscommon

def func_name():
    """
    :return: name_of_caller
    """
    return sys._getframe(1).f_code.co_name
    # end of func_name

def ops_globalenv():
    """
    """
    global pgmname, runid
    pgmname = os.path.splitext(os.path.basename(sys.argv[0]))[0]
    runid=datetime.now().strftime("%Y%m%d_%H%M%S")    
    #formatter = logging.Formatter('%(asctime)s')
    #formatter.default_msec_format = '%s.%06d'

    # where is datalake?
    # 
    ## get and print current working directory
    cwd = os.getcwd()

    ## change local directory 
    #os.chdir("/dept/fitforit/bob/spreadsheets")
    #os.listdir('.')
    # end of setupenv

def loadsummary():
    logging.debug('running {}')
    # end of load summary

def main():
    # TODO 2019-04-10: virtual env needs to add root directory, remove
    # need to append sys.path
    
    sys.path.append('.')
    import logging_pp
    # log messages to local file and messages to console
    logging_pp.init(logdir='logs', loglevel=logging.INFO)

    logging.info('Setup logging using ops_logging package.')
    logging.getLogger().setLevel(logging.INFO)
    
    logging.info('Setup')

    loadsummary()
    logging.info('completed')
    # create/set meterdb libref    
    # 
    # end of main

if __name__ == '__main__':
    """
        Sample main with additional functions
    """
    main()
    sys.exit(0)
# end of program