'''------------------------------------------------------------------------------------------------
Program:    user_interface.py

Security:   NONE

Purpose:    This module provides an interface to the Win / Linux Command Line Interpreter (CLI).
            It contains a UserInterface class whose methods provide a standard way of getting data
            and reporting normal, alternative and abnormal behaviour. The following formats are
            provided:
                - fully customisable messages and headers via the print_() method
                - heading
                  black text, cyan background
                  black text, green background
                  black text, white background
                  black text, yellow background
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
            jeremy.berendt@rolls-royce.com
            support@73rdstreetdevelopment.co.uk

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
19.10.17    M. Critchard    0.1.1       Added print_error_intoor() to allow integer out of range
                                        errors to be printed to the Windows CLI. pylint (10/10)
30.10.17    M. Critchard    0.2.0       Changed formats with coloured backgrounds to have black
                                        text instead of white because the white text appeared
                                        washed-out when using certain CLI tools.
                                        Added black text on white background and black text on
                                        yellow background.
                                        Added a 'padto' optional argument for formats with
                                        backgrounds to allow the user to specify the width of the
                                        colour across the screen.
                                        Added print_blank_lines().  pylint (10/10)
29.11.17    J. Berendt      0.3.0       Added the print_() method which extends functionality of
                                        the built-in print command, allowing user-defined
                                        colouring and padding.
                                        Updated the get_input() function to include appearance
                                        configuration; i.e. text colouring and prompt control.
                                        Updated the _pad() function to use the built-in
                                        str.format() function for padding.
                                        Converted all methods like print_normal() into simple /
                                        standard wrappers for the new print_() method.
                                        Addressed pylint error 'Method could be a function' by
                                        removing the 'self' parameter and adding a @staticmethod
                                        decorator; as no class parameters are changed by the
                                        methods/functions.
30.11.17    J. Berendt      0.3.1       BUG04: When padding text which included tabs, the back
                                        colour padding extended past the surrounding h_pads.
                                        FIX04: Updated the _pad() function to use
                                        str.expandtabs(4) with the text string.
                                        BUG05: User prompts do not act as expected with tiger.
                                        FIX05: Updated default values for the print_() method's
                                        ending_char and add_space parameters to '\n' and False,
                                        respectively.
                                        Added a sleep parameter to the print_() method to enable
                                        pausing after a message / banner is printed.
                                        pylint (10/10)
------------------------------------------------------------------------------------------------'''

#ALLOW OUR IMPORT GROUPING
#pylint: disable=ungrouped-imports

import os
import inspect
import time

import config
import reporterror
from colorama import init as colourinit
from colorama import Fore, Back, Style


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
        This constructor initialises colorama, which enables the user
        to print coloured text to the CLI. It also reads the config
        file, which is used throughout the class.

        COLORAMA BACKGROUND:
        Colorama is initialised here to 'strip ANSI characters from
        stdout and convert them into the equivalent win32 calls'; per
        Jonathan Hartley, author of Colorama.

        The Win32 console (excluding *some* versions of Win10) does not
        support ANSI escape sequences, and therefore simply printing
        the escape sequence to the native Win CLI with the text does
        not work.  So we use Colorama for the low-level win32 work.
        '''

        #COLORAMA INITIALISATION
        colourinit()

        #SET LOCATION OF THE UI CONFIG FILE EXPLICITLY (SHOULD WORK FOR WIN AND LINUX)
        ui_config_file = os.path.join(os.path.realpath(os.path.dirname(__file__)),
                                      'user_interface_config.json')
        #LOAD CONFIG FILE
        self._cfg = config.loadconfig(filename=ui_config_file)

        #BUILD REFERENCE DICTS OF COLORAMA FORE / BACK / STYLE
        self._fore  = self._build_color_dict(class_=Fore)
        self._back  = self._build_color_dict(class_=Back)
        self._style = self._build_color_dict(class_=Style)


    def print_(self, text, fore='white', back='black', style='normal',
               h_pad=0, v_pad=0, sleep=0):

        #TODO: ADD SLEEP TIMER

        '''
        PURPOSE:
        This method extends the functionality of the built-in print
        command by adding the options for text colouring and padding.

        DESIGN:
        The user can pass a text string for output text colour,
        background colour and style, along with horizontal and vertical
        padding.

        The colour and style strings are referenced against colorama's
        .Fore() .Back() and .Style() classes (via a dictionary built
        in this class' constructor) - where the ANSI escape sequences
        are extracted and added to the output text string.

        In addition to colour, horizontal and vertical padding are
        available.

        After a message or banner is printed, the sleep timer can be
        called to pause the program for (n) seconds; for the user to
        read the message or banner.  If the v_pad value is > 0, and the
        sleep value is 0, the sleep timer value is overridden with the
        value defined in the config file's v_pad_sleep key.

        For further detail, refer to the PARAMETERS section
        of this docstring, and refer to the ACCEPTED OPTIONS section for
        each string parameter's available options.

        PARAMETERS:
        - text
        The text to be printed to the console.
        - fore (default='white')
        The output text's colour, as a string.
        - back (default='black')
        The output text's background colour, as a string.
        - style (default='normal')
        The 'normal' style selects the 8 original foreground colours
        (SGR 30-37).
        The 'bright' style provides access to the 8 additional
        foreground colours (SGR 90-97).
        - h_pad (default=0)
        The amount of horizontal padding, in characters.
        This option will increase the field size to the value of h_pad
        and add (n) blank characters of background colour after the
        text string.
        If greater than the number of text characters, colour will
        extend past the end of the text.  Note: the h_pad value is a
        *field size* value, *not* the number of spaces past the end of
        the text string.
        - v_pad (default=0)
        The amount of vertical padding, in lines.
        This option will add (n) blank lines of backgound colour above
        and below the text string - acting like a banner.  The banner
        will extend to the number of spaces specified in the h_pad
        parameter.
        - sleep (default=0)
        Number of seconds to pause the program after a message or
        banner is printed.
        Although the default sleep value is 0 seconds, the default
        changes to (n) second, if the v_pad parameter is > 0.  This
        provides a default pause for the user to read the banner.
        The default v_pad sleep time can be updated in the config file.

        ACCEPTED OPTIONS:
        - fore / back
        black, blue, cyan, green, magenta, red, white, yellow
        - style
        bright, dim, normal
        '''

        #DECODE COLOR FROM STRING TO ANSI SEQUENCE
        _fore   = self._fore[fore.lower()]
        _back   = self._back[back.lower()]
        _style  = self._style[style.lower()]

        #TEST FOR HORIZONTAL PADDING
        if h_pad > 0:
            #PAD TEXT
            text = self._pad(text=text, padto=h_pad)
            #CREATE SPACES FOR V-PADDING
            spaces = self._pad(text='', padto=h_pad)
        else:
            #CREATE SPACES FOR V-PADDING
            spaces = self._pad(text='', padto=len(text))

        #TEST FOR UPPER AND LOWER PADDING
        if v_pad > 0:
            #ADD BLANK LINE ABOVE BANNER
            print ''
            for i in range(v_pad):
                #PRINT UPPER PAD (N) TIMES
                print('%s%s%s %s%s' % (_fore, _back, _style, spaces, Style.RESET_ALL))
            #PRINT MESSAGE & ADD SPACE BEFORE TEXT TO BRING OFF CONSOLE WALL
            print('%s%s%s %s%s' % (_fore, _back, _style, text, Style.RESET_ALL))
            for i in range(v_pad):
                #PRINT LOWER PAD (N) TIMES
                print('%s%s%s %s%s' % (_fore, _back, _style, spaces, Style.RESET_ALL))
            #ADD BLANK LINE BELOW BANNER
            print ''
            #UPDATE SLEEP TIMER FOR BANNER IF SLEEP=0
            sleep = self._cfg['v_pad_sleep'] if sleep == 0 else sleep
        else:
            #PRINT MESSAGE
            print('%s%s%s%s%s' % (_fore, _back, _style, text, Style.RESET_ALL))

        #PAUSE FOR USER TO READ OUTPUT
        time.sleep(sleep)


    def get_input(self, prompt, fore='white', back='black', style='normal',
                  ending_char='\n', add_space=False):

        '''
        PURPOSE:
        This method extends the built-in raw_input() user prompt by
        adding appearance control and text colouring through colorama.

        Like the raw_input() function, the user's input is returned to
        the caller.

        PARAMETERS:
        - prompt
        The user prompt text to be displayed.
        - fore (default='white')
        The output text's colour, as a string.
        - back (default='black')
        The output text's background colour, as a string.
        - style (default='normal')
        The 'normal' style selects the 8 original foreground colours
        (SGR 30-37).
        The 'bright' style provides access to the 8 additional
        foreground colours (SGR 90-97).
        - ending_char (default='\n')
        Character to be added to the end of the prompt.
        - add_space (default=False)
        Add a space separator between the prompt and the user's
        input.

        ACCEPTED OPTIONS:
        - fore / back
        black, blue, cyan, green, magenta, red, white, yellow
        - style
        bright, dim, normal
        '''

        #DECODE COLOR FROM STRING TO ANSI SEQUENCE
        _fore   = self._fore[fore.lower()]
        _back   = self._back[back.lower()]
        _style  = self._style[style.lower()]

        #TEST FOR SPACE TO BE ADDED TO THE END OF THE PROMPT
        space = ' ' if add_space is True else ''

        #RESET COLOURS BEFORE PRINTING A NEW LINE ENDING CHAR
        if ending_char == '\n': ending_char = '%s%s' % (Style.RESET_ALL, '\n')

        #BUILD THE PROMPT STRING
        prompt = '%s%s%s%s%s%s%s' % (_fore, _back, _style, prompt, ending_char,
                                     Style.RESET_ALL, space)

        #PROMPT USER AND RETURN INPUT TO THE CALLER
        return raw_input(prompt)


    def print_heading_cyan(self, text, padto=0):
        '''
        PURPOSE:
        This method prints black text on a cyan background.
        '''
        self.print_(text=text, fore='black', back='cyan', h_pad=padto)

    def print_heading_green(self, text, padto=0):
        '''
        PURPOSE:
        This method prints black text on a green background.
        '''
        self.print_(text=text, fore='black', back='green', h_pad=padto)

    def print_heading_white(self, text, padto=0):
        '''
        PURPOSE:
        This method prints black text on a white background.
        '''
        self.print_(text=text, fore='black', back='white', h_pad=padto)

    def print_heading_yellow(self, text, padto=0):
        '''
        PURPOSE:
        This method prints black text on a yellow background.
        '''
        self.print_(text=text, fore='black', back='yellow', h_pad=padto)

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

    def print_error_intoor(self):
        '''
        PURPOSE:
        This method prints red text on a black background. It uses the
        stack and the config file to print a message for integer out
        of range errors.
        '''
        stack = inspect.stack()
        mtd = inspect.currentframe().f_back.f_code.co_name
        cls = stack[1][0].f_locals['self'].__class__
        text = self._cfg['intoor'].format(mtd, cls)
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

    def print_normal(self, text):
        '''
        PURPOSE:
        This method prints green text on a black background.
        '''
        self.print_(text=text, fore='green', back='black', style='bright')

    def print_warning(self, text):
        '''
        PURPOSE:
        This method prints yellow text on a black background.
        '''
        self.print_(text=text, fore='yellow', back='black', style='bright')

    def print_alert(self, text):
        '''
        PURPOSE:
        This method prints red text on a black background.
        '''
        self.print_(text=text, fore='red', back='black', style='bright')

    @staticmethod
    def print_blank_lines(quantity=1):
        '''
        PURPOSE:
        This method prints (n) blank lines.
        '''
        for i in range(quantity): print('')

    @staticmethod
    def print_error(text):
        '''
        PURPOSE:
        This method prints red text on a black background, and formats
        the output using reporterror functionality.

        PARAMETERS:
        - text
        This is the error object as generated by the Exception.

        USE:
            try:
                ...
            except Exception as err
                _ui.print_error(text=err)
        '''
        print(Fore.LIGHTRED_EX)
        reporterror.reporterror(text)
        print(Style.RESET_ALL)

    @staticmethod
    def _pad(text, padto):
        '''
        PURPOSE:
        This method is used to pad text to the value provided in the
        padto parameter.

        The padto value is a *field size* value, *not* the number of
        blank characters added to the end of the text string.
        '''
        return '{:{padto}}'.format(text.expandtabs(4), padto=padto)

    @staticmethod
    def _build_color_dict(class_):
        '''
        PURPOSE:
        This function is used to create a dictionary from a class and
        return the class attributes, attribute values as a
        key/value pairs.

        For example, when the colorama.Fore class is passed, the output
        looks like:

            {'black': '\x1b[30m', 'blue': '\x1b[34m', ...,
             'white': '\x1b[37m', 'yellow': '\x1b[33m'}

        DESIGN:
        This function is built to specifically *remove* the LIGHT*_EX
        colours from the output dictionary, as these colours are
        accessed using print_()'s 'style' parameter.
        '''

        #RETURN COMPILED DICTIONARY WITH LIGHT*_EX ITEMS REMOVED
        return {k.lower():v for k, v in vars(class_).items() if not k.lower().startswith('light')}
