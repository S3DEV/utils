'''------------------------------------------------------------------------------------------------
Program:    test_log
Version:    0.1.0
Py Ver:     2.7
Purpose:    Unit test for utils.log

Dependents: utils.log

Developer:  J. Berendt
Email:      support@73rdstreetdevelopment.co.uk

Comments:   Pylint knowingly flags the following:
                - C0413: utils.log import should be at top of module

Use:        > cd /package_root/test
            > python test_log.py

---------------------------------------------------------------------------------------------------
UPDATE LOG:
Date        Programmer      Version     Update
29.05.17    J. Berendt      0.0.1       Written
20.07.17    J. Berendt      0.1.0       Updated to test the write() method of the Log class rather
                                        than write2log().
------------------------------------------------------------------------------------------------'''

import os
import sys
import unittest

#ADD DIR PATH TO IMPORT UTILS.LOG
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from utils.log import Log


class TestLog(unittest.TestCase):

    def test_log(self):

        import re

        #VARIABLES
        log_path       = 'c:/temp/utils_log_unittest.log'
        header         = 'datetime,host,user,text'
        entry          = 'this is a test'
        pattern_entry  = r'([0-9]{4}-[0-9]{2}-[0-9]{2}\s[0-9]{2}:[0-9]{2}:[0-9]{2}.[0-9]{6},' \
                          '[0-9a-zA-Z].*,' \
                          '[0-9a-zA-Z].*,' + entry + ')'
        exp            = re.compile(pattern_entry)

        #INSTANTIATE LOG CLASS
        _log = Log(filepath=log_path, autofill=True, printheader=True,
                   headertext=header)

        #WRITE LOG FILE
        _log.write(text=entry)
        _log.write_blank_line()

        #READ IN LOG FILE
        text = [line.strip() for line in open(log_path, 'r').readlines()]

        #TEST HEADER
        self.assertTrue(text[0] == header)

        #TEST LOG ENTRY AGAINST REGEX
        self.assertTrue(len(exp.findall(text[1])) == 1)

        #TEST FOR BLANK LINE (WRITTEN BY write_blank_line() METHOD)
        self.assertTrue(text[2] == '')

        #DELETE THE LOG FILE
        if os.path.exists(log_path): os.remove(log_path)


#-----------------------------------------------------------------------
#MAIN PROGRAM CONTROLLER
def main():

    #RUN UNIT TESTS
    unittest.main()


#RUN PROGRAM
if __name__ == '__main__': main()
