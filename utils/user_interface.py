'''------------------------------------------------------------------------------------------------
Program:    user_interface.py

Version:    0.1.0

Security:   NONE

Purpose:    This module provides an interface to the Windows Command Line Interpreter (CLI).
            It contains a UserInterface class whose methods provide a standard way of getting data
            and reporting normal, alternative and abnormal behaviour. The following formats are
            provided:
                - heading
                  white text, cyan background
                  white text, green background
                - user input expected
                  white text, black backgroud
                - normal behaviour
                  green text, black background
                - alternative behaviour (e.g. a warning)
                  yellow text, black background
                - abnormal or erroneous behaviour
                  red text, black background

Developer:  M. Critchard

Email:      mark.critchard@rolls-royce.com

---------------------------------------------------------------------------------------------------
UPDATE LOG:
Date        Programmer      Version     Update
09.10.17    M. Critchard    0.0.1       Written
10.10.17    J. Berendt      0.0.2       Updated config file reader to use utils.config module.
                                        Updated 'import utils.reporterror' statement to
                                        'import reporterror', as reporterror is now a local module.
                                        Extended header line length to 100 characters.
                                        Added version file and import.
                                        pylint (10/10)
11.10.17    J. Berendt      0.0.3       BUG01: Config file could not be found on module import.
                                        FIX01: Added explicit config file location.
11.10.17    J. Berendt      0.0.4       Removed the class instantiation shortcut.
                                        BUG02: Config file install was setup for Windows, and
                                        failed on Linux.
                                        FIX02: Updated the path to locate the config file to use
                                        'utils.__file__' as the starting location.
                                        BUG03: When analysing EHM.enviro with pylint, this error
                                        was caught:
                                        '_Client._set_type: No value for argument 'text' in method
                                        call'
                                        On inspection, the utils.user_interface.print_error_enviro
                                        method requires a 'text' argument.
                                        FIX03: The text argument is old/residual code and have been
                                        removed as the text for this error is pulled form the
                                        config file.  pylint (10/10)
16.10.17    J. Berendt      0.1.0       Added a print_alert() method which prints console text in
                                        red.
                                        Updated config file location to use __file__ rather than
                                        utils.__file__, and wrapped in the realpath() function.
                                        pylint (10/10)
------------------------------------------------------------------------------------------------'''

import os
import inspect
import reporterror
import config

from _version_ui import __version__
from colorama import init as colourinit
from colorama import Fore, Back, Style

#IGNORE AS METHODS ARE USED TO PRINT TO CONSOLE
#pylint: disable=no-self-use
#IGNORE SHORTCUT TO CLASS INSTANTIATION
#pylint: disable=invalid-name

class UserInterface(object):
    '''
    PURPOSE:
    This class encapsulates the Windows / Linux Command Line Interpreter
    (CLI). Its methods provide a standard way of getting data
    and reporting normal, alternative and abnormal behaviour.

    USE:
    import utils.user_interface as ui
    _ui = ui.UserInterface()
    _ui.print_heading_green(text='MY HEADER')
    '''

    def __init__(self):
        '''
        PURPOSE:
        This constructor initialises colorama, which colours output to
        the CLI. It also reads the config file, which is used
        throughout the class.
        '''
        colourinit()

        #SET LOCATION OF THE UI CONFIG FILE EXPLICITLY (SHOULD WORK FOR WIN AND LINUX)
        ui_config_file = os.path.join(os.path.realpath(os.path.dirname(__file__)),
                                      'user_interface_config.json')

        self._cfg = config.loadconfig(filename=ui_config_file)

    def get_input(self, prompt):
        '''
        PURPOSE:
        This method prompts the user for input and then returns the
        user's input to the caller.
        '''
        user_input = raw_input(prompt)
        return user_input

    def print_heading_cyan(self, text):
        '''
        PURPOSE:
        This method prints white text on a cyan background.
        '''
        print(Back.CYAN + Fore.LIGHTWHITE_EX +
              text +
              Style.RESET_ALL)

    def print_heading_green(self, text):
        '''
        PURPOSE:
        This method prints white text on a green background.
        '''
        print(Back.GREEN + Fore.LIGHTWHITE_EX +
              text +
              Style.RESET_ALL)

    def print_normal(self, text):
        '''
        PURPOSE:
        This method prints green text on a black background.
        '''
        print(Fore.LIGHTGREEN_EX +
              text +
              Style.RESET_ALL)

    def print_warning(self, text):
        '''
        PURPOSE:
        This method prints yellow text on a black background.
        '''
        print(Fore.LIGHTYELLOW_EX +
              text +
              Style.RESET_ALL)

    def print_alert(self, text):
        '''
        PURPOSE:
        This method prints red text on a black background.
        '''
        print(Fore.LIGHTRED_EX +
              text +
              Style.RESET_ALL)

    def print_error(self, text):
        '''
        PURPOSE:
        This method prints red text on a black background.
        '''
        print(Fore.LIGHTRED_EX)
        reporterror.reporterror(text)
        print(Style.RESET_ALL)

    def print_error_enviro(self):
        '''
        PURPOSE:
        This method prints red text on a black background. It uses the
        stack and the config file to print a message for environment
        errors.
        '''
        stack = inspect.stack()
        mtd = inspect.currentframe().f_back.f_code.co_name
        cls = stack[1][0].f_locals['self'].__class__
        text = self._cfg['enviro'].format(mtd, cls)
        self.print_error(text)

    def print_error_notimp(self):
        '''
        PURPOSE:
        This method prints red text on a black background. It uses the
        stack and the config file to print a message for not
        implemented errors.
        '''
        stack = inspect.stack()
        mtd = inspect.currentframe().f_back.f_code.co_name
        cls = stack[1][0].f_locals['self'].__class__
        text = self._cfg['notimp'].format(mtd, cls)
        self.print_error(text)

    def print_error_unexpd(self):
        '''
        PURPOSE:
        This method prints red text on a black background. It uses the
        stack and the config file to print a message for unexpected
        errors.
        '''
        stack = inspect.stack()
        mtd = inspect.currentframe().f_back.f_code.co_name
        cls = stack[1][0].f_locals['self'].__class__
        text = self._cfg['unexpd'].format(mtd, cls)
        self.print_error(text)

    def print_error_windws(self):
        '''
        PURPOSE:
        This method prints red text on a black background. It uses the
        stack and the config file to print a message for Windows
        errors.
        '''
        stack = inspect.stack()
        mtd = inspect.currentframe().f_back.f_code.co_name
        cls = stack[1][0].f_locals['self'].__class__
        text = self._cfg['windws'].format(mtd, cls)
        self.print_error(text)
