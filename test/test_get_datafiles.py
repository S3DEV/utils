'''------------------------------------------------------------------------------------------------
Program:    test_get_datafiles
Version:    0.0.1
Py Ver:     2.7
Purpose:    Unit test for get_datafiles.py

Developer:  J. Berendt
Email:      support@73rdstreetdevelopment.co.uk

Comments:   Pylint knowingly flags the following:
                - C0413: utils.log import should be at top of module

Use:        > cd /package_root/test
            > python test_log.py

---------------------------------------------------------------------------------------------------
UPDATE LOG:
Date        Programmer      Version     Update
19.10.17    J. Berendt      0.0.1       Written
------------------------------------------------------------------------------------------------'''

#ALLOW LATE IMPORT
#pylint: disable=wrong-import-position

import os
import sys
import unittest

#ADD DIR PATH TO IMPORT UTILS.LOG
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
import utils.get_datafiles as gdf


class TestGetDataFiles(unittest.TestCase):

    def test_get_datafiles(self):

        #BUILD STRING FOR ROOT
        search_root = os.path.realpath(os.path.dirname(__file__))

        #GET LIST OF FILES
        files = gdf.get_datafiles(pkg_dir=search_root, exts=['.test'])

        #EXTRACT UI CONFIG FILE FROM LIST
        ui_cfg = [os.path.split(fname[1][0])[1] for fname in files
                  if os.path.split(fname[1][0])[1] == 'user_interface_config.test']

        #TEST FOR EXPECTED FILE
        self.assertEqual(ui_cfg[0], 'user_interface_config.test')


#-----------------------------------------------------------------------
#MAIN PROGRAM CONTROLLER
def main():

    #RUN UNIT TESTS
    unittest.main()


#RUN PROGRAM
if __name__ == '__main__': main()
