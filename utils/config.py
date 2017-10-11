'''------------------------------------------------------------------------------------------------
Program:    config
Version:    0.0.4
Py Ver:     2.7
Purpose:    Small helper program designed to load a program's config
            file.

Dependents: os
            sys
            json

Developer:  J. Berendt
Email:      support@73rdstreetdevelopment.co.uk

Use:        >>> import utils.config
            >>> CONFIG = config.loadconfig()

---------------------------------------------------------------------------------------------------
UPDATE LOG:
Date        Programmer      Version     Update
02.10.16    J. Berendt      0.0.1       Written
29.11.16    J. Berendt      0.0.2       New loadconfig parameters:
                                        - filename  (default=config.json)
                                        - devmode   (default=False)
                                        Added docstring to program.
                                        Added error handling if the config file does not exist.
                                        Cleaned code to confirm to PEP8. pylint (10/10)
                                        - WARNING: This will break programs currently using
                                          this module!
22.03.17    J. Berendt      0.0.3       Added a test to determine if the filename is a path,
                                        or filename only.  If full path, the devmode / path
                                        deciphering is bypassed.
                                        This allows a calling program to pass in a full path to
                                        the config file, without it being altered.
14.05.17    J. Berendt      0.0.4       Updated to sit within the utils library.
                                        Incomplete code warning: added filename parameter to
                                        the os.path.dirname check.
                                        Simplified __fromjson function. pylint (10/10)
                                        Renamed function/method names to replace double leading
                                        underscore with single underscore.
------------------------------------------------------------------------------------------------'''

import os
import sys
import json
from _version_config import __version__

#-----------------------------------------------------------------------
#METHOD FOR GENERAL SETUP
def loadconfig(filename='config.json', devmode=False):

    '''
    DESIGN:
    Function designed to load and return a program's JSON config file
    as a dictionary.

    The devmode parameter can be used if you are programming through an
    IDE which defaults the sys.argv[0] value to the cwd of the IDE,
    rather than from where the program is actually being run.
    It just makes design and debugging easier.

    PREREQUESITES / ASSUMPTIONS:
    - The config file is a JSON file
    - The config file lives in the program directory

    USE:
    > import utils.config as config
    > c = config.loadconfig()

    > param_value = c['someparam_name']
    '''

    #TEST IF FULL PATH OR ONLY FILENAME WAS PASSED
    if os.path.dirname(filename) == '':

        #TEST PROGRAM MODE
        if devmode:

            #STORE PROGRAM DIRECTORY
            path_base = os.getcwd()

        else:

            #ASSIGN DIRECTORIES
            progdir = os.path.dirname(os.path.realpath(sys.argv[0]))
            curdir = os.getcwd()

            #TEST AND STORE PROGRAM DIRECTORY
            path_base = progdir if sys.argv[0] != '' else curdir

        #CONSOLIDATE PATH AND FILENAME
        fullpath = os.path.join(path_base, filename)

    else:

        #ASSIGN PASSED PATH/FILENAME TO TESTED VARIABLE
        fullpath = filename


    #TEST IF THE FILE EXISTS
    if os.path.exists(fullpath):

        #LOAD CONFIG FILE
        return _fromjson(filepath=fullpath)

    else:

        #USER NOTIFICATION
        raise UserWarning('The config file (%s) could not be found.' % (fullpath))
        return None


#-----------------------------------------------------------------------
#FUNCTION FOR READING THE CONFIG FILE INTO A DICTIONARY
def _fromjson(filepath):

    #OPEN AND READ CONFIG FILE >> RETURN AS DICT
    with open(filepath, 'r') as config: return json.load(config)
