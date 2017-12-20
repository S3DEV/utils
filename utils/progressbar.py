'''---------------------------------------------------------------------
Program:    progressbar
Py Ver:     2.7
Purpose:    This is a class which provides access to a simple console
            progress bar.

Dependents: sys

Developer:  J. Berendt
Email:      support@73rdstreetdevelopment.co.uk

Comments:   This class is to be incorporated into the utils package
            later.

Use:        Refer to USE section of the docstring.

------------------------------------------------------------------------
UPDATE LOG:
Date        Programmer      Version     Update
16.05.17    J. Berendt      0.0.1       Written
31.05.17    J. Berendt      0.0.2       Converted into a class for use
                                        with the utils package.
01.06.17    J. Berendt      0.0.3       Added a user defined color
                                        option.
05.06.17    J. Berendt      0.0.4       Moved version to external file.
                                        Added into utils package.
---------------------------------------------------------------------'''

import sys
import colorama

from _version_progressbar import __version__


class ProgressBar(object):

    '''
    DESIGN:
    This is a simple console progress bar which should be called
    inside a processing loop.

    You can pass in the bar colour, length and symbol parameters if
    you want to configure the appearance a little bit.

    PARAMETERS:
        - bar_len (default=50)
        Length of the progress bar.
        - symbol (default='.')
        The symbol which is used to track progress.
        - color (default='white')
        Color of the progress bar.
            - red, green, yellow, blue, magenta, cyan, white

    USE:
    > import progressbar
    >
    > pb = progressbar.ProgressBar(bar_len=25, symbol='#', color='r')
    >
    > #SOME PROCESS
    > for i range(26):
    >     #UPDATE PROGRESS
    >     pb.update_progress(current=i, total=25)
    >     #SOME PAUSE TO SEE UPDATES
    >     time.sleep(.1)
    '''

    #CONSTANT DECLARATIONS
    RED     = '31'
    GREEN   = '32'
    YELLOW  = '33'
    BLUE    = '34'
    MAGENTA = '35'
    CYAN    = '36'
    WHITE   = '37'


    def __init__(self, bar_len=50, symbol='.', color='w'):

        '''
        PURPOSE:
        Initialisation method.  Create the progress bar object.
        '''

        #MAKE COLORS WORK WITH WINDOWS
        colorama.init()

        #SET CLASS VARIABLES
        self._bar_len = bar_len
        self._symbol = symbol
        self._color = color
        self._reset = '\x1b[0m'

        #GET USER'S COLOUR
        self._clr = self._getcolor()


    def update_progress(self, current, total):

        '''
        PURPOSE:
        Method used to update the progress bar.

        USE:
        Refer to the class docstring: help(progressbar.ProgressBar)
        '''

        #CALCULATE PERCENT COMPLETE
        percent = float(current) / total
        #DETERMINE NUMBER OF 0 PLACEHOLDERS
        vals = len(str(total))
        #NUMBER OF TICKS
        ticks = self._symbol * int(round(percent * self._bar_len))
        #NUMBER OF SPACE PLACEHOLDERS
        spaces = ' ' * (self._bar_len - len(ticks))

        #PRINT OUTPUT
        sys.stdout.write(self._clr + '\rProcessing %s of %s [ %s ] %.0f%% Complete' % \
                         (str(current).zfill(vals),
                          total,
                          ticks + spaces,
                          percent*100) + self._reset)

        #FLUSH BUFFER
        sys.stdout.flush()


    def _getcolor(self):

        '''
        PURPOSE:
        This is a helper function for returning the ANSI color string
        for the user's color option, using the global color constants.
        '''

        color = ''

        #RETURN USER COLOR AN ANSI STRING
        if self._color.lower() == 'r' or self._color.lower() == 'red':
            color = '\x1b[%s;40m' % (self.RED)
        if self._color.lower() == 'g' or self._color.lower() == 'green':
            color = '\x1b[%s;40m' % (self.GREEN)
        if self._color.lower() == 'y' or self._color.lower() == 'yellow':
            color = '\x1b[%s;40m' % (self.YELLOW)
        if self._color.lower() == 'b' or self._color.lower() == 'blue':
            color = '\x1b[%s;40m' % (self.BLUE)
        if self._color.lower() == 'm' or self._color.lower() == 'magenta':
            color = '\x1b[%s;40m' % (self.MAGENTA)
        if self._color.lower() == 'c' or self._color.lower() == 'cyan':
            color = '\x1b[%s;40m' % (self.CYAN)
        if self._color.lower() == 'w' or self._color.lower() == 'white':
            color = '\x1b[%s;40m' % (self.WHITE)

        return color
