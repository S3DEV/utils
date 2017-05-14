'''------------------------------------------------------------------------------------------------
Program:    reporterror
Version:    0.0.1
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

Use:        >
            >

---------------------------------------------------------------------------------------------------
UPDATE LOG:
Date        Programmer      Version     Update
01.01.17    J. Berendt      0.0.1       Written. pylint (10/10)
------------------------------------------------------------------------------------------------'''

from _version_reporterror import __version__

#-----------------------------------------------------------------------
#METHOD USED TO REPORT AN ERROR
def reporterror(error):

    '''
    DESIGN:
    Module designed to handle error reporting and logging.

    PARAMETERS:
        - error
        Exception from the error handler; refer to the USE section.

    USE:
    > try:
    >     stuff here ...
    > except Exception as err:
    >     #REPORT / LOG ERROR
    >     reporterror(err)
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
    #w2l(CONFIG['file_log'], 'ERROR: %s; METHOD: %s; LINE: %s' % (error, func_name, line_num))

    #CLEANUP
    del (exc_type, exc_obj, exc_tb)
