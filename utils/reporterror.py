"""------------------------------------------------------------------------------------------------
Program:    reporterror
Platform:   Windows / Linux
Py Ver:     2.7
Purpose:    Module designed to report program errors to the console
            and/or a log file, using the utils.log Log() class.

Dependents: log
            sys
            traceback

Developer:  J. Berendt
Email:      support@73rdstreetdevelopment.co.uk

Comments:

Use:        > import utils.reporterror as reporterror
            >
            > try:
            >   stuff here ...
            > except Exception as err:
            >   # SEND ERROR TO REPORTERROR METHOD
            >   reporterror.reporterror(err)

---------------------------------------------------------------------------------------------------
UPDATE LOG:
Date        Programmer      Version     Update
01.01.17    J. Berendt      0.0.1       Written. pylint (10/10)
29.05.17    J. Berendt      0.0.2       Updated to fit within the installed utils module.
                                        Added the CMD to log file output.  pylint (10/10)
11.10.17    J. Berendt      0.0.3       BUG01: The 'ImportError: cannot import name write2log'
                                        error is thrown on reporterror() use; as the write2log
                                        has been deleted from utils v5.
                                        FIX01: Replaced the write2log method call with the new
                                        Log() class.
21.12.17    J. Berendt      0.0.4       **FORMATTING CHANGES**
                                        Cleaned docstring text and formatting IAW PEP 257.
                                        Changed docstrings to use triple-double quotes (PEP 257).
                                        Changed block comments to add a space after '#' (PEP 8).
                                        Moved the summary block comment from above each
                                        method/function into the docstring.  pylint (10/10)
23.02.18    M. Critchard    0.0.5       Changed print statements for compatibility with Python 3.
05.03.18    J. Berendt      0.0.6       Added __future__ import to support Python 2/3.
------------------------------------------------------------------------------------------------"""

from __future__ import absolute_import, print_function

# ----------------------------------------------------------------------
def reporterror(error, logevent=False,
                logfilepath='c:/temp/reporterror.log'):
    """
    Report an error, using the Exception object.

    DESIGN:
    Module designed to handle error reporting and logging.

    PARAMETERS:
        - error
        Exception from the error handler; refer to the USE section.
        - logevent (default=False)
        Send the error to a log file.
        Note: use of this command assumes the log file is already
        created, and the header is already written.
        - logfilename (default='c:/temp/reporterror.log')
        File path to the log file.

    USE:
    > try:
    >     stuff here ...
    > except Exception as err:
    >     # REPORT / LOG ERROR
    >     reporterror.reporterror(err)
    """

    import sys
    import traceback
    import log

    # GET TRACEBACK OBJECTS
    exc_type, exc_obj, exc_tb = sys.exc_info()
    filename, line_num, func_name, text = traceback.extract_tb(exc_tb)[-1]

    # USER NOTIFICATION
    print('')
    print('ERROR:\t%s'  % error)
    print('TYPE:\t%s'   % exc_type)
    print('FUNC:\t%s'   % func_name)
    print('LINE:\t%s'   % line_num)
    print('CMD:\t%s'    % text)

    # LOG ERROR
    if logevent:
        # SETUP THE LOGGER
        _log = log.Log(filepath=logfilepath)
        # LOG ERROR
        _log.write(text='ERROR: %s; CMD: %s; METHOD: %s; LINE: %s' %
                   (error, text, func_name, line_num))

    # CLEANUP
    del (exc_type, exc_obj, exc_tb)
