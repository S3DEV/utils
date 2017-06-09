'''------------------------------------------------------------------------------------------------
Program:    test_log
Version:    0.0.1
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
------------------------------------------------------------------------------------------------'''

import os
import sys
import unittest

#ADD DIR PATH TO IMPORT UTILS.LOG
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
import utils.log as log


class TestLog(unittest.TestCase):

    def test_log(self):

        import re

        #VARIABLES
        _log_path       = 'c:/temp/utils_log_unittest.log'
        _header         = 'datetime,host,user,text'
        _entry          = 'this is a test'
        _pattern_entry  = r'([0-9]{4}-[0-9]{2}-[0-9]{2}\s[0-9]{2}:[0-9]{2}:[0-9]{2}.[0-9]{6},' \
                          '[0-9a-zA-Z].*,' \
                          '[0-9a-zA-Z].*,' + _entry + ')'
        _exp            = re.compile(_pattern_entry)
        _match          = []

        #WRITE LOG FILE
        log.write2log(filepath=_log_path, text=_entry,
                      autofill=True, printheader=True,
                      headertext=_header)

        #READ IN LOG FILE
        text = [line.strip() for line in open(_log_path, 'r').readlines()]

        #TEST HEADER
        self.assertTrue(text[0] == _header)

        #LOOP OVER LOG TEXT AND MATCH PATTERN USING REGEX (SKIP HEADER)
        for line in text[1:]:
            #ADD TEST RESULT TO LIST
            _match.append(True if len(_exp.findall(line)) > 0 else False)

        #TEST LIST FOR ANY FALSE VALUES (INDICATING A LINE FAILED THE TEST)
        self.assertTrue(False not in _match)

        #DELETE THE LOG FILE
        if os.path.exists(_log_path): os.remove(_log_path)


#-----------------------------------------------------------------------
#MAIN PROGRAM CONTROLLER
def main():

    #RUN UNIT TESTS
    unittest.main()


#RUN PROGRAM
if __name__ == '__main__': main()
