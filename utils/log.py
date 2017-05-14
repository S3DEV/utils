'''------------------------------------------------------------------------------------------------
Program:    log
Version:    0.0.3
Py Ver:     2.7
Purpose:    Small program designed to be a central log file creator.
            Designed to be called from another program to handle its simple logging requirements.

            The calling program is responsible for passing the proper arguments to create the
            log file header.  (i.e.: PrintHeader=True, HeaderText='some, header, text, here')

            It is suggested to call W2L at program startup, with PrintHeader set to True.
            If the log file already exists, the header will not be written.

Dependents: os
            datetime
            socket
            getpass

Developer:  J. Berendt
Email:      support@73rdstreetdevelopment.co.uk

Comments:

Use:        >>> from log import Write2Log as w2l
            >>> w2l(FilePath, Text, [PrintHeader=False], [HeaderText=''])

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
------------------------------------------------------------------------------------------------'''

def Write2Log(FilePath, Text, AutoFill=True, PrintHeader=False, HeaderText=''):

    '''
    DESIGN:
    Designed as a small logging program, to be called by another program.

    The calling program is responsible for passing the proper arguments to create the
    log file header.  (i.e.: PrintHeader=True, HeaderText='some, header, text, here')

    It is suggested to call Write2Log at program startup, with PrintHeader set to True,
    and a header string passed.  If the log file already exists, the header will not be written.

    AUTOFILL:
    The AutoFill option (default=True) autofills the log file with:
        - datetime (now)
        - host
        - username

    FILE VALIDATION:
    Tests are performed to ensure the log file is being populated correctly.
    1) If PrintHeader is False, and the log file does not yet exist, the user is notified.
    2) If PrintHeader is True, yet HeaderText is blank, the user is instructed to pass header
       text.
    3) If PrintHeader is True, yet the log file already exists, the header will not be written.

    USE:
    > from log import Write2Log as w2l
    > log(FilePath, Text, [AutoFill=True], [PrintHeader=False], [HeaderText=''])
    '''

    from datetime import datetime as dt
    import os
    import socket
    import getpass


    try:

        #VALIDATION
        #TEST THE FILE EXISTS (IF HEADER IS NOT REQUESTED)
        if PrintHeader is False and os.path.exists(FilePath) is False:
            #NOTIFY USER
            raise IOError('The log file does not yet exist, however a header was not requested.\n'
                          'Perhaps the header should be written to the log file first?\n')


        #VALIDATION
        #TEST PRINTHEADER ARGUMENT, TO ENSURE A HEADER STRING IS BEING PASSED >> RAISE ERROR
        if PrintHeader is True and HeaderText == '':
            #NOTIFY USER
            raise IOError('PrintHeader is requested, however the HeaderText string is blank.\n'
                          'If the PrintHeader argument is True, the HeaderText string must also be passed.\n')


        #HEADER
        #TEST PRINTHEADER ARGUMENT, TO ENSURE A HEADER STRING IS BEING PASSED >> PRINT HEADER
        if PrintHeader is True and HeaderText != '' and os.path.exists(FilePath) is False:
            #CREATE FILE
            with open(FilePath, 'a') as f:
                #WRITE HEADER
                f.write(HeaderText)
                #ADD NEW LING CHARACTER
                f.write('\n')


        #LOG TEXT
        #TEST THAT TEXT IS PASSED >> WRITE TEXT TO LOG
        if Text != '':

            #TEST FOR AUTOFILL
            if AutoFill:

                #BUILD AUTOTEXT STRING
                autotext = '%s,%s,%s,' % (dt.now(), socket.gethostname(), getpass.getuser())

                #APPEND TEXT TO LOG FILE
                with open(FilePath, 'a') as f:
                    #WRITE TEXT
                    f.write(autotext)
                    f.write(Text)
                    #ADD NEW LINE CHARACTER
                    f.write('\n')


    except Exception as err:

        #NOTIFY USER OF EXCEPTION
        print 'log.Write2Log ERROR: %s' % err
