# logging_pp
# extensions to python logging package

"""logging_pp

This module contains a function "logging_pp_init()" that sets up file and console logging. All subsequent 
log messages are sent both to the console and to a logfile. Log messages are generated via the "logging" package.

Example:
    >>> import logging_pp
    >>> import logging
    >>> logging_pp.init('mylogs')
    >>> logging.info('Test message')

If run as main, this module illustrates the usage of logging_pp package.
"""