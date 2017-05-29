'''------------------------------------------------------------------------------------------------
Program:    reporterror
Version:    0.0.2
Platform:   Windows / Linux
Py Ver:     2.7
Purpose:    Module designed to report program errors to the console
            and/or a log file, using the utils.log.write2log() method.

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
            >   #SEND ERROR TO REPORTERROR METHOD
            >   reporterror.reporterror(err)

---------------------------------------------------------------------------------------------------
UPDATE LOG:
Date        Programmer      Version     Update
01.01.17    J. Berendt      0.0.1       Written. pylint (10/10)
29.05.17    J. Berendt      0.0.2       Updated to fit within the installed utils module.
                                        Added the CMD to log file output.  pylint (10/10)
------------------------------------------------------------------------------------------------'''

from _version_reporterror import __version__

#-----------------------------------------------------------------------
#METHOD USED TO REPORT AN ERROR
def reporterror(error, logevent=False, logfilepath='c:/temp/reporterror.log'):

    '''
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
    >     #REPORT / LOG ERROR
    >     reporterror.reporterror(err)
    '''

    import sys
    import traceback
    from log import write2log as w2l

    #GET TRACEBACK OBJECTS
    exc_type, exc_obj, exc_tb = sys.exc_info()
    filename, line_num, func_name, text = traceback.extract_tb(exc_tb)[-1]

    #USER NOTIFICATION
    print ''
    print 'ERROR:\t%s'  % error
    print 'TYPE:\t%s'   % exc_type
    print 'FUNC:\t%s'   % func_name
    print 'LINE:\t%s'   % line_num
    print 'CMD:\t%s'    % text

    #LOG ERROR
    if logevent: w2l(filepath=logfilepath,
                     text='ERROR: %s; CMD: %s; METHOD: %s; LINE: %s' % (error, text,
                                                                        func_name,
                                                                        line_num),
                     autofill=True)

    #CLEANUP
    del (exc_type, exc_obj, exc_tb)
