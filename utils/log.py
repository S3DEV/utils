'''------------------------------------------------------------------------------------------------
Program:    log
Version:    0.1.1
Py Ver:     2.7
Purpose:    Small program designed to be a central log file creator.
            Updated to be part of the utils package, and installed into site-packages.

            The calling program is responsible for passing the proper arguments to create the
            log file header.  (i.e.: PrintHeader=True, HeaderText='some, header, text, here')

            It is suggested to call w2l at program startup, with the printheader parameter
            set to True.  If the log file already exists, the header will not be written.

Dependents: os
            datetime
            socket
            getpass

Developer:  J. Berendt
Email:      support@73rdstreetdevelopment.co.uk

Comments:

Use:        >>> from utils.log import write2log as w2l
            >>> w2l(filepath, text, [printheader=False], [headertext=''])

---------------------------------------------------------------------------------------------------
UPDATE LOG:
Date        Programmer      Version     Update
02.10.16    J. Berendt      0.0.1       Written
22.10.16    J. Berendt      0.0.2       Updated to add optional PrintHeader argument.
                                        Removed Header argument test.  Header will now be
                                        populated by the calling program.
                                        Header argument renamed HeaderText.
                                        Added header and log validation checks.
                                        Added error handling.
06.12.16    J. Berendt      0.0.3       Updated dependencies in header.
                                        Revised import structure to improve readability and clarify
                                        to which module the methods belong.
                                        Cleaned code with pylint. (10/10)
29.05.17    J. Berendt      0.1.0       Updated to fit within the utils package.
                                        Code revised / cleaned to meet PEP-8 style standards.
                                        pylint (10/10)
29.05.17    J. Berendt      0.1.1       Updated to add new line before UserWarning errors.
------------------------------------------------------------------------------------------------'''

from _version_log import __version__

#-----------------------------------------------------------------------
def write2log(filepath, text, autofill=True, printheader=False,
              headertext=''):

    '''
    DESIGN:
    Designed as a small external logging program.

    The calling program is responsible for passing the proper arguments
    to create the log file header.
    (i.e.: PrintHeader=True, HeaderText='some, header, text, here')

    It is suggested to call write2log() at program startup, with the
    printheader argument set to True, and a header string passed.
    If the log file already exists, the header will not be written.

    PARAMETERS:
        - filepath
        Path to the log file.
        - text
        Entry text to be written to the log.  The format should follow
        the  format of the header.
        - autofill (default=True)
        Auto-fill the log entry with datetime(now), host and username
        values.
        - printheader (default=False)
        Flag to print the text passed to the headertext parameter as
        the log file header.  This is typically only writte on file
        creation.
        - headertext (default='')
        [Comma separated] values to be written as the log file header.

    FILE VALIDATION:
    Tests are performed to ensure the log file is being populated
    correctly.
    1) If printheader is False, and the log file does not yet exist,
    the user is notified.
    2) If printheader is True, yet headertext is blank, the user is
    instructed to pass header text.
    3) If printheader is True, yet the log file already exists,
    the header will not be written.

    USE:
    > from utils.log import write2log as w2l
    > log(filepath, text, [autofill=True], [printheader=False],
          [headertext=''])
    '''

    from datetime import datetime as dt
    import os
    import socket
    import getpass


    try:

        #VALIDATION
        #TEST THE LOG FILE EXISTS (IF HEADER IS NOT REQUESTED)
        if printheader is False and os.path.exists(filepath) is False:
            #NOTIFY USER
            raise UserWarning('The log file does not exist, however a header was not requested. '
                              'A header must be written at the time of log file creation.\n')


        #VALIDATION
        #TEST PRINTHEADER ARGUMENT, TO ENSURE A HEADER STRING IS BEING PASSED >> RAISE ERROR
        if printheader is True and headertext == '':
            #NOTIFY USER
            raise UserWarning('The printheader argument is True, however the headertext string is '
                              'blank. A headertext string must also be supplied.\n')


        #HEADER
        #TEST PRINTHEADER ARGUMENT, TO ENSURE A HEADER STRING IS BEING PASSED >> PRINT HEADER
        if printheader is True and headertext != '' and os.path.exists(filepath) is False:
            #CREATE FILE
            with open(filepath, 'a') as f:
                #WRITE HEADER
                f.write(headertext)
                #ADD NEW LING CHARACTER
                f.write('\n')


        #LOG TEXT
        #TEST THAT TEXT IS PASSED >> WRITE TEXT TO LOG
        if text != '':

            #TEST FOR AUTOFILL >> BUILD AUTOFILL STRING
            autotext = '%s,%s,%s,' % (dt.now(), socket.gethostname(), getpass.getuser()) \
                       if autofill is True else ''

            #APPEND TEXT TO LOG FILE
            with open(filepath, 'a') as f:
                #WRITE TEXT
                f.write(autotext)
                f.write(text)
                #ADD NEW LINE CHARACTER
                f.write('\n')


    except Exception as err:

        #NOTIFY USER OF EXCEPTION
        print '\nERR: %s' % err
