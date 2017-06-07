'''---------------------------------------------------------------------
Program:    test_all
Version:    0.0.2
Py Ver:     2.7
Purpose:    Program for running all unit test files.

Dependents: os

Developer:  J. Berendt
Email:      jeremy.berendt@rolls-royce.com

Comments:   This module should be run from the command line, as shown
            below.  Test output will not be shown if run inside IDE.

Use:        >>> cd /path/to/tests
            >>> python test_all.py

------------------------------------------------------------------------
UPDATE LOG:
Date        Programmer      Version     Update
19.05.17    J. Berendt      0.0.1       Written
07.06.07    J. Berendt      0.0.2       Added file path validation for
                                        testlist file.
                                        Added try/except block to main()
---------------------------------------------------------------------'''

import os

#-----------------------------------------------------------------------
#METHOD FOR RUNNING THE TESTS
def runit(module):

    #NOTIFICATION
    print '\nRUNNING TEST(S) FOR: %s' % (module)
    #DO IT!
    os.system('python %s' % module)


#-----------------------------------------------------------------------
#MAIN PROGRAM CONTROLLER
def main():

    #VARIABLES
    testlist = 'testlist.txt'

    try:
        #VERIFY TESTLIST FILE EXISTS
        if os.path.exists(testlist):
            #GET LIST OF TEST MODULES FROM TEXT FILE
            modules = [item.strip() for item in open('testlist.txt', 'r').readlines()
                       if item.strip() != '' and not item.startswith('#')]

            #LOOP THROUGH MODULES >> RUN MODULE
            for module in modules: runit(module=module)

        else:
            #NOTIFICATION
            print 'ERR: The %s file cannot be found.' % testlist

    except Exception as err:
            #NOTIFICATION
        print 'ERR: %s' % err


#RUN PROGRAM
if __name__ == '__main__': main()
