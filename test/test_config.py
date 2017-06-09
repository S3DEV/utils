'''------------------------------------------------------------------------------------------------
Program:    test_config
Version:    0.0.1
Py Ver:     2.7
Purpose:    Unit test for utils.config

Dependents: utils.config

Developer:  J. Berendt
Email:      support@73rdstreetdevelopment.co.uk

Comments:   Pylint knowingly flags the following:
                - C0413: utils.utils import should be at top of module
                - C0413: utils.config import should be at top of module

Use:        > cd /package_root/test
            > python test_config.py

---------------------------------------------------------------------------------------------------
UPDATE LOG:
Date        Programmer      Version     Update
09.06.17    J. Berendt      0.0.1       Written
------------------------------------------------------------------------------------------------'''

import os
import sys
import unittest

#ADD DIR PATH TO IMPORT UTILS.LOG
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
import utils.utils as u
import utils.config as config


class TestConfig(unittest.TestCase):

    #CLASS VARIABLES
    _path = 'c:/temp/'
    _file = 'config_test.json'
    _config_dict = {'path':'c:/temp/',
                    'file':'config_test.json'}


    def setUp(self):
        #CREATE JSON FILE IN SPECIFIC LOCATION
        u.json_write(dictionary=self._config_dict, filepath=os.path.join(self._path, self._file))
        #CREATE JSON FILE IN CWD
        u.json_write(dictionary=self._config_dict, filepath=self._file)


    def tearDown(self):
        #DELETE TEST CONFIG FROM LOCATION
        os.remove(os.path.join(self._path, self._file))
        #DELETE TEST CONFIG FROM CWD
        os.remove(self._file)


    #TEST CONFIG FROM DEFINED PATH
    def test_config_fullpath(self):

        #PULL IN CONFIG
        conf = config.loadconfig(filename=os.path.join(self._path, self._file), devmode=True)

        #RUN TESTS
        self.assertTrue(self._test_general(conf))


    #TEST CONFIG FROM CWD
    def test_config_defaults(self):

        #PULL IN CONFIG
        conf = config.loadconfig(filename=self._file, devmode=True)

        #RUN TESTS
        self.assertTrue(self._test_general(conf))


    #GENERAL TESTING FUNCTION
    def _test_general(self, conf):

        results = []

        #TEST: RETURNED OBJECT IS A DICT
        results.append(self.assertTrue(isinstance(conf, dict)))
        #TEST: VALUE
        results.append(self.assertEqual(conf['path'], self._path))
        results.append(self.assertEqual(conf['file'], self._file))

        #TEST IF ANY TESTS FAILED
        passed = True if False not in results else False

        #RETURN RESULTS
        return passed


#-----------------------------------------------------------------------
#MAIN PROGRAM CONTROLLER
def main():

    #RUN UNIT TESTS
    unittest.main()


#RUN PROGRAM
if __name__ == '__main__': main()
