'''------------------------------------------------------------------------------------------------
Program:    utils.py
Version:    4.3.0
Py Ver:     2.7
Purpose:    Central library standard s3dev utilities.

Comments:

Use:        > import utils.utils as u
            > help(u)

---------------------------------------------------------------------------------------------------
UPDATE LOG:
Date        Programmer      Version     Update
26.04.16    J. Berendt      1.0.0       colours_addRGB:
                                        written
27.04.16    J. Berendt      1.1.0       colours_addRGBA:
                                        written
                                        format_exifDate:
                                        written
03.05.16    J. Berendt      1.2.0       colours_addRGB:
                                        Replaced brewer2mpl with palettable library.
                                        colours_addRGBA:
                                        Replaced brewer2mpl with palettable library.
11.05.16    J. Berendt      1.3.0       Added function for Oracle database connections.
                                        Added function to clean dataframe headers and content.
14.05.16    J. Berendt      1.4.0       Added a function to write a JSON file.
                                        Added a function to read a JSON file.
                                        Added a function to check if a file exists; using os.
17.05.16    J. Berendt      1.5.0       Added a function for loading a config file.
                                        Added version attribute.
20.05.16    J. Berendt      2.0.0       Added function to test for a directory, and create if
                                        required.
                                        Added deployment testing method.
                                        Added versioning.
                                        Reorganised utils.py code into utils package.
                                            - CAUTION: THIS WILL BREAK PROGRAMS USING THIS PACKAGE.
23.05.16    J. Berendt      2.1.0       Added a function to parse argv arguments for help and
                                        versioning of command line programs.
                                        Updated use instructions to fit v2.0.0 upgrade.
28.05.16    J. Berendt      2.1.1       Added function for decoding unicode characters;
                                        using unidecode.
12.10.16    J. Berendt      2.1.2       Updated dbConn_Oracle():
                                            - to prompt the user only for the login parameters
                                            that are missing. Method used to prompt for all if
                                            only one parameter was missing.
                                            - Added 'db' string to the prompts, to clarify these
                                            are database credentials.
10.11.16    J. Berendt      2.2.0       Added dbConn_SQL method for connecting to a SQL Server
                                        database.
                                        Added GetDriverName helper function which returns the
                                        ODBC driver name for a passed regex search string;
                                        as driver names can vary across PCs.
                                        Updated dbConn_Oracle login prompts to include 'oracle',
                                        to differenciate this login request from sql server.
14.11.16    J. Berendt      2.3.0       Added a utility to extract the hex (or specified dtype)
                                        color values from a matplotlib colour map.
                                        This is useful when creating a color gradient for plotly
                                        graphs (e.g.: bar charts).
28.11.16    J. Berendt      2.3.1       Updated setup.py to grab / install dependencies.
                                        Updated _version code to be more concise.
29.11.16    J. Berendt      2.3.2       No functional changes.
                                        Cleaned code with pylint.
                                        Fixed year in v2.3.0 and 2.3.1 update comments.
04.04.17    J. Berendt      3.0.0       Added a method to test if a library exists before
                                        importing it: testimport()
                                        ----------------------------------
                                        CODE OVERHAUL AND STANDARDISATION:
                                        ----------------------------------
                                        - Revised all code and docstrings to conform to the PEP-8
                                        line wrap standard. (Aside from this header).
                                        - Updated the format_exif_date() function to use datetime
                                        rather than the s.replace() function.
                                        - Added feature to getcolormap() which provides a preview
                                        for the chosen color map.
                                        REMOVED METHODS:
                                        - ArgvParse()
                                        - GetConfig()
                                        - colours_addRGB()
                                        - colours_addRGBA()
                                        RENAMED METHODS:
                                        - All methods/functions and parameters have
                                        been renamed to use all lower case, per PEP-8.
                                            - Original method/function names still exist,
                                            but warning messages have been added advising source
                                            updates.
29.05.17    J. Berendt      3.0.1       BUG01: utils.__version__ shows the package version rather
                                        than the module version.
                                        FIX01: Updated the _version call to use _version_utils.
05.06.17    J. Berendt      3.0.2       BUG02: The clean_df() function returns an updated version
                                        of the original dataframe.  A cleaned COPY should be
                                        returned.
                                        FIX02: Updated function so that a COPY of the df is
                                        updated and returned, rather than the original.
21.06.17    J. Berendt      3.1.0       Known low pylint score due to 'Invalid ... name' convention
                                        warnings.  These modules will be removed on next major
                                        update. (7.96/10)
                                        Updated dbconn_sql and dbconn_oracle to remove None type
                                        return after connection failure, due to pylint
                                        'unreachable code' warning.
                                        Added dbconn_sqlite function.
                                        Replaced leading double underscores with single underscore.
                                        Updated clean_df function to test for number or datetime
                                        data types before performing column value cleaning.
07.07.17    J. Berendt      3.1.1       Updated the dbconn_sqlite() function so the db file is
                                        created if it doesn't exist.
25.07.17    J. Berendt      3.2.0       Added the rgb2hex function.
09.10.17    J. Berendt      3.3.0       Added dbconn_mysql() function.
                                        Minor docstring revisions.
10.10.17    J. Berendt      4.0.0       Updated to remove depreciated methods and functions.
                                        - This update aligns with the utils v5 update.
                                        Updated variables in fileexists() and direxists()  to
                                        lower case.  pylint (10/10)
16.10.17    J. Berendt      4.1.0       Overhaul / re-structure for the dbconn_* functions.
                                        - split each connection function into sub/reusable
                                        functions
                                        - enhanced error trapping / handling
                                        - updated dbconn_oracle() and dbconn_sql() functions to
                                        accept a JSON config file for db credentials.
                                        - added user parameter (in parallel to existing userid
                                        parameter), to the oracle and sql db connection functions.
                                        pylint (10/10)
20.10.17    J. Berendt      4.2.0       Added the getsitepackages() function.  pylint (10/10)
11.12.17    J. Berendt      4.3.0       Updated getcolormap() function to include a colorscale
                                        boolean parameter, which transforms a colour map into a
                                        colorscale list for use with the Plotly colorscale
                                        parameter.
                                        Added a listcolormaps() method which prints the available
                                        colour maps in matplotlib.
                                        Added the _convert_to_colorscale() helper function for use
                                        with the getcolormap() function.
                                        Updated the format_exif_date() function to accept caller
                                        specified input and output formats.  pylint (10/10)
------------------------------------------------------------------------------------------------'''

import site
import platform
import config
import reporterror
import user_interface
from _version_utils import __version__


#GLOBAL CONSTANTS / CLASS INSTANTIATIONS
_UI = user_interface.UserInterface()

#-----------------------------------------------------------------------
#METHOD USED FOR DEPLOYMENT TESTING
def __test():

    '''
    DESIGN:
    Method used for testing only.
    '''
    print 'This is only a test.'


#-----------------------------------------------------------------------
#FUNCTION USED TO RETURN THE SITE PACKAGES DIRECTORY, BASED ON PLATFORM
def getsitepackages():

    '''
    PURPOSE:
    This function returns the directory path to site-packages based on
    the platform.

    DESIGN:
    The function first uses the platform.system() function to get the
    platform's base OS.  The OS is then tested and the site-packages
    location is returned using the OS appropriate element from the
    site.getsitepackages() list.

    If the OS is not accounted for, or fails the test, a value of
    'unknown' is returned.

    RATIONALE:
    The need for this function comes out of the observation there are
    many (many!) different ways on stackoverflow (and other sites) to
    get the location to which pip will install a package, and most of
    the answers contradict each other.  Also, the site.getsitepackages()
    function returns a list of two options (in all tested cases); and
    the Linux / Windows paths are in different locations in this list.

    So this function was written to help simplify matters ... hopefully.
    '''

    #GET PLATFORM
    my_os = platform.system().lower()

    #TEST PLATFORM >> GET SITE-PACKAGES DIRECTORY
    if 'win' in my_os:
        sitepkgs_dir = site.getsitepackages()[1]

    elif 'lin' in my_os:
        sitepkgs_dir = site.getsitepackages()[0]

    else:
        sitepkgs_dir= 'unknown'

    return sitepkgs_dir


#-----------------------------------------------------------------------
#FUNCTION USED TO CONVERT AN RGB STRING TO A HEX VALUE
def rgb2hex(rgb_string, drop_alpha=False):

    '''
    DESIGN:
    This function is designed to convert an rgb (or rgba) string to a
    hex string.

    For example: 'rgb(195, 0, 0)' returns #c00000
                 'rgba(65, 125, 50, 0.25)' returns #40417d32

    This is useful as some colour functions return an rgb or rgba
    string, and matplotlib.pyplot only accepts hex strings.

    Regex is used to extract the colour channels from the string.
    Therefore, the 'rgb' or 'rgba' prefix is not required; although
    accepted for standard use.

    The extracted integer values (or float value in the case of alpha),
    are converted to hex and returned as a compiled hex string.

    If an alpha value is present, the alpha value is moved to the first
    byte of the hex string; making the hex string read as #argb.

    PARAMETERS:
        - rgb_string
          This is the rgb or rgba string to convert.
        - drop_alpha (default=False)
          'True' will drop the alpha value from the hex string.
          This is useful for colour maps that automatically return an
          alpha channel, yet the [plotting program] does not accept
          alpha values.

    DEPENDENCIES:
    - re

    USE:
    > import utils.utils as u
    > clr = u.rgb2hex('rgb(195, 0, 0)')
    '''

    import re

    try:
        #MATCH RGB CHANNELS, AND SEVERAL VARIATIONS OF (INCL OPTIONAL) ALPHA
        #CASE WILL BE IGNORED
        pattern = r'([0-9]{1,3},\s*[0-9]{1,3},\s*[0-9]{1,3}(,\s[0,1]{0,}\.*[0-9]{0,})?)'
        exp = re.compile(pattern, flags=re.IGNORECASE)

        #EXTRACT COLOUR CHANNEL VALUES FROM PASSED STRING
        vals = exp.search(rgb_string).groups()[0].split(',')
        #REMOVE COMMAS FROM EACH STRING & TRIM WHITESPACE
        vals = [val.replace(',', '').strip() for val in vals]

        #TEST IF ALPHA SHOULD BE STRIPPED
        if drop_alpha is True and len(vals) == 4: vals = vals[:3]

        #TEST IF ALPHA CHANNEL PROVIDED
        if len(vals) == 4:
            #TEST IF ALPHA CHANNEL IN FLOAT >> CONVERT TO INTEGER (BETWEEN 0 AND 255)
            vals[3] = int(round(float(vals[3]) * 255, 0)) if 0 <= float(vals[3]) <= 1 else vals[3]

        #CONVERT VALUES FROM STRING TO INT
        ints = [int(i) for i in vals]

        #TEST IF ALPHA CHANNEL PROVIDED
        if len(ints) == 4:
            #MOVE ALPHA CHANNEL TO BEGINNING OF LIST
            ints.insert(0, ints[3])
            #SPLIT CHANELS
            r, g, b, a = [i for i in ints[:4]]
            #CONVERT TO HEX STRING
            xhex = '#{:02x}{:02x}{:02x}{:02x}'.format(r,g,b,a)

        #NO ALPHA CHANNEL
        elif len(ints) == 3:
            #SPLIT CHANELS
            r, g, b = [i for i in ints]
            #CONVERT TO HEX STRING
            xhex = '#{:02x}{:02x}{:02x}'.format(r,g,b)

        else:
            #NOTIFY USER OF INCORRECT FORMAT
            raise ValueError('The quantity of integer values to convert must be 3 or 4 values.\n\n'\
                             'The colour channel list musts be in this format: ' \
                             '(r, g, b) or (r, g, b, a) to include the alpha channel.')

        #RETURN CONVERTED HEX VALUE AS STRING
        return str(xhex)

    except Exception as err:
        #NOTIFICATION
        reporterror.reporterror(err)


#-----------------------------------------------------------------------
#FUNCTION RETURNS A LIST OF CONVERTED VALUES FROM A MATPLOTLIB COLORMAP
def getcolormap(colormap='Blues', n=5, colorscale=False, dtype='hex',
                preview=False, preview_in='mpl'):

    '''
    DESIGN:
    Function designed to return a list of colour values from a
    matplotlib colormap.  The number of returned colour values can
    range from 1 to 256.

    This is useful when creating a graph which requires gradient
    colour map. (e.g.: a plotly bar chart)

    To print a list of available colour maps:
    > import utils.utils as u
    > u.listcolormaps()

    PARAMETERS:
        - colormap (default='Blues')
          name of the matplotlib color map
        - n (default=1)
          number of colors to return
        - colorscale (default=False)
          converts the retured colour map into a list of colour scale
          values.  this is useful with Plotly's colorscale parameter.
          returned format: [(0.00, u'#f7fbff'), (0.33, u'#abd0e6'),
                            (0.66, u'#3787c0'), (1.00, u'#08306b')]
        - dtype (default='hex')
          data type to return
        - preview (default=False)
          this option creates a plotly or matplotlib graph displaying
          the colormap.
        - preview_in (default='mpl')
          display method for previewing the graph.
          'mpl' = matplotlib (used for inline preview)
          'plotly' = plotly (use for html display in a web browser)

    DEPENDENCIES:
    - matplotlib

    USE:
    > import utils.utils as u
    > cmap = u.getcolourmap(colormap='winter',
                            n=50,
                            dtype='hex',
                            preview=True,
                            preview_in='plotly')
    '''

    from matplotlib import cm
    from matplotlib.colors import rgb2hex

    #CREATE A COLOR MAP OBJECT (MAP, NUMBER OF VALUES)
    cmap = cm.get_cmap(colormap, n)

    #CONVERT COLORMAP OBJECT INTO LIST OF COLORS
    if dtype.lower() == 'hex':
        #RETURN A LIST OF RGB2HEX CONVERTED COLORS
        colors = [rgb2hex(cmap(i)[:3]) for i in range(cmap.N)]
    else:
        colors = None

    #TEST FOR PREVIEW:
    if colors is not None and preview:
        #MATPLOTLIB
        if preview_in == 'mpl': _prev_mpl(cmap=colors, cmap_name=colormap)
        #PLOTLY
        if preview_in == 'plotly': _prev_plotly(cmap=colors, cmap_name=colormap)


    #TEST FOR COLORSCALE >> RETURN COLOUR MAP OR COLOUR SCALE
    return colors if colorscale is False else _convert_to_colorscale(cmap=colors)


#-----------------------------------------------------------------------
#HELPER FUNCTION TO CONVERT A COLOUR MAP TO A COLOUR SCALE LIST
def _convert_to_colorscale(cmap):

    '''
    PURPOSE:
    This is a helper function used to convert a colour map into a
    colour scale list, as used by the Plotly colorscale parameter.

    DESIGN:
    Returned format: [(0.00, u'#f7fbff'), (0.33, u'#abd0e6'),
                      (0.66, u'#3787c0'), (1.00, u'#08306b')]

    DEPENDENCIES:
    - numpy
    '''

    import numpy as np

    return [i for i in zip(np.linspace(0, 1, num=len(cmap)), cmap)]


#-----------------------------------------------------------------------
#METHOD USED TO PRINT A LIST OF AVAILABLE MATPLOTLIB COLOUR MAPS
def listcolormaps():

    '''
    PURPOSE:
    A very simple method used to print a list of colour maps available
    in matplotlib.

    DEPENDENCIES:
    - matplotlib

    USE:
    > import utils.utils as u
    > u.listcolormaps()
    '''

    from matplotlib.pyplot import colormaps

    print colormaps()


#-----------------------------------------------------------------------
#HELPFER METHOD USED TO PREVIEW A COLOUR MAP USING MATPLOTLIB
def _prev_mpl(cmap, cmap_name):

    '''
    DESIGN:
    This method is designed to be called form the getcolormap()
    function, as a means of displaying / previewing the colour map
    chosen, using the matplotlib plotting library.

    ADVANTAGE:
    This method displays the colour map preview directly within the
    [Sypder] IDE, Jupyter Notebook.

    PARAMETERS:
    - cmap
      The colour map you want to preview.  This must be a python list of
      rgb/rgba/hex values.
    - cmap_name
      The name of the matplotlib colour map.  (e.g.: OrRd, winter, etc.)
      This name is only used to display the colour map name in the
      graph title.

    DEPENDENCIES:
    - matplotlib
    '''

    import matplotlib.pyplot as plt

    #CREATE GRAPH DATA
    n = len(cmap)
    x = range(0, n)
    y = [10]*n

    #CREATE IMAGE
    plt.figure(facecolor='black')
    plt.bar(x, y, width=15, linewidth=0, color=cmap)
    plt.title('COLOUR MAP NAME: %s' % cmap_name, color='w', size=12)
    plt.xlim(0, n)
    plt.ylim(0, 10)
    plt.tick_params(top='off', bottom='off', left='off', right='off', labelleft='off')
    plt.xticks(color='w', size=12)
    #TURN OFF BORDER
    for spine in plt.gca().spines.values(): spine.set_visible(False)
    #DISPLAY GRAPH
    plt.show()


#------------------------------------------------------------------------------
#COLOUR MAP (BAR GRAPH) PREVIEW USING PLOTLY
def _prev_plotly(cmap, cmap_name, out_file='c:/temp/cmap_graph.html'):

    '''
    DESIGN:
    This method is designed to be called form the getcolormap()
    function, as a means of displaying / previewing the colour map
    chosen, using the plotly library.

    ADVANTAGE:
    This method displays the hex/rgb/rgba colour code value for each
    bar as hovertext.

    PARAMETERS:
    - cmap
      The colour map you want to preview.  This must be a python list of
      rgb/rgba/hex values.
    - cmap_name
      The name of the matplotlib colour map.  (e.g.: OrRd, winter, etc.)
      This name is only used to display the colour map name in the
      graph title.
    - out_file (default='c:/temp/cmap_graph.html')
      File path/name for the html graph output; if you wish to save
      the file.

    DEPENDENCIES:
    - plotly >= 2.0.6
    '''

    #TEST IF PLOTLY HAS BEEN INSTALLED
    if testimport('plotly'):

        from plotly.offline import plot
        import plotly.graph_objs as go

        #CREATE GRAPH DATA
        n = len(cmap)
        x = range(1, n+1)
        y = [10]*n
        grey = 'rgb(165, 165, 165)'

        #CREATE LAYOUT
        layout = go.Layout(title='COLOUR MAP NAME: %s' % (cmap_name), titlefont=dict(color=grey, size=20))
        #CREATE BAR GRAPH
        bar1 = go.Bar(x=x, y=y, text=cmap, marker=dict(color=cmap))

        #EDIT AXES
        layout['xaxis'].update(zeroline=False, showgrid=False, tickfont=dict(color=grey))
        layout['yaxis'].update(zeroline=False, showgrid=False, showticklabels=False)

        #COMPILE AND PLOT
        fig = go.Figure(data=[bar1], layout=layout)
        plot(fig, filename=out_file, show_link=False)


#-----------------------------------------------------------------------
#FUNCTION DESIGNED TO CONVERT EXIF DATE
def format_exif_date(datestring, input_format='%Y:%m:%d %H:%M:%S',
                     output_format='%Y%m%d%H%M%S'):

    '''
    DESIGN:
    Function designed to convert the exif date/timestamp
    from 2010:01:31 12:31:18 (or a caller specified) format to a
    format specified by the caller.

    This is useful for storing an exif date as a datetime string.

    PARAMETERS:
    - datestring
    the datetime string to be converted.
    typical exif date format: yyyy:mm:dd hh:mi:ss
    - input_format (default='%Y:%m:%d %H:%M:%S')
    formatting string for the input datetime value.
    - output_format (default='%Y%m%d%H%M%S')
    formatting string for the resulting date time value.

    DEPENDENCIES:
    - datetime

    USE:
    > import utils.utils as u
    > newdate = u.format_exif_date('2010:01:31 12:31:18')
    '''

    from datetime import datetime as dt

    #RETURN FORMATTED STRING
    return dt.strftime(dt.strptime(datestring, input_format), output_format)


#-----------------------------------------------------------------------
#FUNCTION TO VERIFY THE REQUIRED FIELDS ARE PROVIDED IN THE CONFIG FILE
#USER IS PROMPTED FOR ALL VALUES NOT PROVIDED
def _dbconn_fields(dbtype, fields, filename):

    '''
    PURPOSE:
    This is a general-purpose function used to extract database
    credentials from a passed JSON config file.

    DESIGN:
    Using the passed file, the config key/values are loaded into a
    dictionary which is iterated, testing if the expected fields are
    present.  If an expected field is not present, the user is prompted
    for the value.

    The completed credential dictionary is then returned.
    '''

    try:
        #INITIALISE
        creds = dict()

        #LOAD CONNECTION DETAILS FROM CONFIG FILE
        conf = config.loadconfig(filename=filename)

        #LOOP THROUGH EXPECTED KEYS
        for key in fields:
            #TEST KEY EXISTS IN CONFIG FILE
            if conf.has_key(key):
                #ADD EXISTING VALUE TO CREDENTIAL DICT (USED FOR CONNECTION)
                creds[key] = conf[key]
            else:
                #PROMPT FOR VALUE >> ADD TO CREDENTIAL DICT
                creds[key] = raw_input('please enter the %s %s: ' % (dbtype, key))

        #RETURN DICTIONARY OF CREDENTIALS
        return creds

    except Exception as err:
        #USER NOTIFICATION
        _UI.print_alert('\nAn error occurred while checking the database credentials in the '
                        'config file.\nFilename used: %s' % filename)
        _UI.print_error(err)
        return None


#-----------------------------------------------------------------------
#FUNCTION BUILDS A DICT FROM DB CREDENTIAL PARAMETERS
def _dbconn_params(dbtype, **params):

    '''
    PURPOSE:
    This is a general-purpose function used to test if the provided
    database credential parameters have been populated.

    DESIGN:
    This function iterates over the passed credential fields (passed as
    **kwargs), and tests each field for a None value.  If a None value
    is found, the user is prompted for the credential.

    The completed credential dictionary is then returned.
    '''

    try:
        #LOOP THROUGH KEYS AND GET MISSING VALUES
        for key, value in params.items():
            #TEST VALUE
            if params[key] is None:
                #PROMPT USER FOR VALUE
                params[key] = raw_input('Please enter the %s for the %s connection: ' %
                                        (key, dbtype))

        #RETURN COMPLETED DICTIONARY
        return params

    except Exception as err:
        #USER NOTIFICATION
        _UI.print_alert('\nAn error occurred while checking the passed database credentials.')
        _UI.print_error(err)
        return None


#-----------------------------------------------------------------------
#FUNCTION MAKES AN ORACLE DB CONNECTION AND RETURN THE CONN/CUR OBJECTS
def _dbconn_oracle_conn(creds):

    '''
    PURPOSE:
    This function is used to make a connection to an Oracle database.

    DESIGN:
    Using a passed credential dictionary, an Oracle connection string
    is built and used for connection.

    Upon successful connection, the function returned the db connection
    and cursor objects, wrapped in a dictionary.
    '''

    import cx_Oracle

    try:
        #BUILD CONNECTION STRING
        connstring = '%s/%s@%s' % (creds['user'], creds['password'], creds['host'])

        #MAKE THE CONNECTION >> GET CURSOR OBJECT
        connection = cx_Oracle.connect(connstring)
        cursor = connection.cursor()

        #RETURN THE CONN/CUR OBJECTS IN A DICT
        return dict(conn=connection, cur=cursor)

    except Exception as err:
        #ALERT USER TO CONNECTION ERROR
        _UI.print_alert('\nThe database connection failed for '
                        '(host: %s, user name: %s, pw: xxx...%s)' %
                        (creds['host'], creds['user'], creds['password'][-3:]))
        _UI.print_error(err)


#-----------------------------------------------------------------------
#FUNCTION MAKES AN ORACLE DB CONNECTION AND RETURN THE CONN/CUR OBJECTS
def _dbconn_mysql_conn(creds):

    '''
    PURPOSE:
    This function is used to make a connection to a MySQL database.

    DESIGN:
    The passed credential dictionary is passed directly into the
    mysql.connect function as a set of **kwargs.

    Upon successful connection, the function returned the db connection
    and cursor objects, wrapped in a dictionary.
    '''

    import mysql.connector as sql

    try:
        #CREATE CONNECTION / CURSOR OBJECTS
        connection = sql.connect(**creds)
        cursor = connection.cursor()

        #RETURN THE CONN/CUR OBJECTS IN A DICT
        return dict(conn=connection, cur=cursor)

    except Exception as err:
        #ALERT USER TO CONNECTION ERROR
        _UI.print_alert('\nThe database connection failed for '
                        '(host: %s, user name: %s, pw: xxx...%s)' %
                        (creds['host'], creds['user'], creds['password'][-3:]))
        _UI.print_error(err)


#-----------------------------------------------------------------------
#FUNCTION MAKES AN ORACLE DB CONNECTION AND RETURN THE CONN/CUR OBJECTS
def _dbconn_sql_conn(creds):

    '''
    PURPOSE:
    This function is used to make a connection to a SQL Server database.

    DESIGN:
    The database credentials are passed into the pyodbc library, which
    searches for the SQL Server driver, via the getdrivername()
    function.

    Upon successful connection, the function returned the db connection
    and cursor objects, wrapped in a dictionary.
    '''

    import pyodbc

    try:
        #BUILD CONNECTION STRING >> CONNECT
        connection = pyodbc.connect('Driver={%s};'
                                    'Server=%s;'
                                    'Database=%s;'
                                    'UID=%s;'
                                    'PWD=%s;' %
                                    (getdrivername('SQL Server.*'),
                                     creds['server'],
                                     creds['database'],
                                     creds['user'],
                                     creds['password']))

        #CREATE CURSOR OBJECT
        cursor = connection.cursor()

        #STORE RESULT IN DICTIONARY
        return dict(conn=connection, cur=cursor)

    except Exception as err:
        #ALERT USER TO CONNECTION ERROR
        _UI.print_alert('\nThe database connection failed for '
                        '(host: %s, user name: %s, pw: xxx...%s)' %
                        (creds['host'], creds['user'], creds['password'][-3:]))
        _UI.print_error(err)


#-----------------------------------------------------------------------
#FUNCTION DESIGNED TO RETURN DB OBJECTS FOR A SQLITE DATABASE
def dbconn_sqlite(db_path):

    '''
    DESIGN:
    Function designed to create and return database connection and
    cursor objects for a SQLite database, using the passed database
    filename.

    conn = [the connection object]
    cur  = [the cursor object]

    PARAMETERS:
        - db_path
        Full path to the SQLite database file.

    DEPENDENCIES:
    - sqlite3
    - reporterror

    USE:
    > import utils.utils as u
    > dbo = u.dbconn_sqlite(db_path)
    > conn = dbo['conn']
    > cur = dbo['cur']
    '''

    import sqlite3 as sql

    try:
        #CREATE CONNECTION / CURSOR OBJECTS
        connection = sql.connect(db_path)
        cursor = connection.cursor()

        #STORE RESULT IN DICTIONARY
        return dict(conn=connection, cur=cursor)

    except Exception as err:
        #NOTIFICATION
        reporterror.reporterror(err)



#-----------------------------------------------------------------------
#FUNCTION DESIGNED CREATE AN ORACLE DB CONN; USER PROMPTED FOR DETAILS.
def dbconn_oracle(host=None, user=None, userid=None, password=None, from_file=False,
                  filename=None):

    '''
    DESIGN:
    Function designed to create a connection to an Oracle database
    using the provided login details, or directly from a config file.
    If a login detail is not provided, the user is prompted; which can
    be used as a security
    feature.

    The connection is tested.  If successful, the connection and
    cursor objects are returned to the calling program, as a
    dictionary.

    conn = [the connection object]
    cur  = [the cursor object]

    NOTE: To prompt for login details, leave the argument(s) blank.

    PARAMETERS:
        - host (default=None)
          database host; or database name
        - user (default=None)
          user name, or schema name
        - userid (default=None)
          same as 'user' parameter (both are not needed)
        - password (default=None)
          just what it says on the tin  :-)
        - from_file (default=False)
          boolean flag instructing the function to use the provided
          config (JSON) file for connection details
          valid keys:
              - host, user, password
        - filename (default=None)
          file path and name of the JSON file containing the connection
          details

    DEPENDENCIES:
    - cx_Oracle

    USE:
    > import utils.utils as u
    > dbo = u.dbconn_oracle(host='myhost', userid='myuser',
                            password='mypass')
    > conn = dbo['conn']
    > cur = dbo['cur']

    USE: CONNECTION DETAILS FROM JSON:
    > import utils.utils as u
    > dbo = u.dbconn_oracle(from_file=True, filename='db_config.json')
    > conn = dbo['conn']
    > cur = dbo['cur']

    '''

    try:
        #INITIALISE
        creds = dict()
        dbtype = 'oracle'

        #TEST IF CONFIG FILE IS USED
        if from_file:
            #CONFIG KEYS TO CHECK
            db_keys = ['host', 'user', 'password']

            #VERIFY REQUIRED FIELD EXIST IN CONFIG FILE
            creds = _dbconn_fields(dbtype=dbtype, fields=db_keys, filename=filename)

        else:
            #COMBINE USER AND USERID
            user = user if user is not None else userid

            #TEST PASSED PARAMETERS >> WRAP IN DICTIONARY
            creds = _dbconn_params(dbtype=dbtype, host=host, user=user, password=password)

        #TEST A VALID CREDENTIAL FILE WAS BUILT
        if creds is not None:
            #MAKE THE CONNECTION >> GET THE CONN/CUR OBJECTS
            return _dbconn_oracle_conn(creds=creds)

    except Exception as err:
        #ALERT USER TO CONNECTION ERROR
        _UI.print_alert('\nAn error occurred while connecting to the Oracle database.')
        _UI.print_error(err)


#-----------------------------------------------------------------------
#FUNCTION DESIGNED CREATE A MYSQL DB CONN; USER PROMPTED FOR DETAILS.
def dbconn_mysql(host=None, user=None, password=None, database=None, port=3306,
                 from_file=False, filename=None):

    '''
    DESIGN:
    Function designed to create a connection to a MySQL database
    using the provided login details, or directly from a config file.
    If a login detail is not provided, the end-user is prompted; which
    can be used as a security feature.

    Once all credentials are gathered, the connection is tested.  If
    successful, the connection and cursor objects are returned to the
    calling program, as a dictionary.

    conn = [the connection object]
    cur  = [the cursor object]

    NOTE: To prompt for login details, leave the argument(s) blank.

    SOURCE:
    The connection argument keys for a MySQL connection using the
    mysql.connection library, are listed here:
    https://dev.mysql.com/doc/connector-python/en/connector-python-connectargs.html

    PARAMETERS:
        - host (default=None)
          IP address or machine name of the host or database server
        - user (default=None)
          user name used to authenticate
        - password (default=None)
          just what it says on the tin  :-)
        - database (default=None)
          name of the database to connect
        - port (default=3306)
          the TCP/IP port of the MySQL server; must be an integer
        - from_file (default=False)
          boolean flag instructing the function to use the provided
          config (JSON) file for connection details
          valid keys:
              - user, password, database, host, port
        - filename (default=None)
          file path and name of the JSON file containing the connection
          details

    DEPENDENCIES:
    - mysql-connector (2.1.4)
      Installation: > pip install mysql-connector==2.1.4

    USE: PASSED CONNECTION DETAILS:
    > import utils.utils as u
    > dbo = u.dbconn_mysql(host, user, password, database)
    > conn = dbo['conn']
    > cur = dbo['cur']

    USE: CONNECTION DETAILS FROM JSON:
    > import utils.utils as u
    > dbo = u.dbconn_mysql(from_file=True, filename='db_config.json')
    > conn = dbo['conn']
    > cur = dbo['cur']
    '''

    try:
        #INITIALISE
        creds = dict()
        dbtype = 'mysql'

        #TEST IF CONFIG FILE IS USED
        if from_file:
            #CONFIG KEYS TO CHECK
            db_keys = ['user', 'password', 'database', 'host', 'port']

            #VERIFY REQUIRED FIELD EXIST IN CONFIG FILE
            creds = _dbconn_fields(dbtype=dbtype, fields=db_keys, filename=filename)

        else:
            #TEST PASSED PARAMETERS >> WRAP IN DICTIONARY
            creds = _dbconn_params(dbtype=dbtype, host=host, user=user, password=password,
                                   database=database, port=port)

        #TEST A VALID CREDENTIAL FILE WAS BUILT
        if creds is not None:
            #MAKE THE CONNECTION >> GET THE CONN/CUR OBJECTS
            return _dbconn_mysql_conn(creds=creds)

    except Exception as err:
        #ALERT USER TO CONNECTION ERROR
        _UI.print_alert('\nAn error occurred while connecting to the MySQL database.')
        _UI.print_error(err)


#-----------------------------------------------------------------------
#FUNCTION DESIGNED CREATE A SQL SERVER DB CONN; USER PROMPTED FOR
#DETAILS.
def dbconn_sql(server=None, database=None, userid=None, user=None, password=None,
               from_file=False, filename=None):

    '''
    DESIGN:
    Function designed to create a connection to a SQL Server database
    using the provided login parameters, or directly froma config file.
    If a login detail is not provided, the user is prompted; which can
    be used as a security
    feature.

    The connection is tested.  If successful, the connection and cursor
    objects are returned to the calling program, as a dictionary.

    conn = [the connection object]
    cur  = [the cursor object]

    NOTE: To prompt for login details, leave the argument(s) blank.

    PARAMETERS:
        - server (default=None)
          name of the server on which the database lives
        - database (default=None)
          name of the database to which you're connecting
        - user (default=None)
          just what it says on the tin
        - userid (default=None)
          same as 'user' parameter (both are not needed)
        - password (default=None)
          again, just what it says on the tin  :-)
        - from_file (default=False)
          boolean flag instructing the function to use the provided
          config (JSON) file for connection details
          valid keys:
              - server, database, user, password
        - filename (default=None)
          file path and name of the JSON file containing the connection
          details

    DEPENDENCIES:
    - pyodbc

    USE:
    > import utils.utils as u
    > dbo = u.dbconn_sql(server, database, user, password)
    > conn = dbo['conn']
    > cur = dbo['cur']

    USE: CONNECTION DETAILS FROM JSON:
    > import utils.utils as u
    > dbo = u.dbconn_sql(from_file=True, filename='db_config.json')
    > conn = dbo['conn']
    > cur = dbo['cur']
    '''

    try:
        #INITIALISE
        creds = dict()
        dbtype = 'sql_server'

        #COMBINE USER AND USERID
        user = user if user is not None else userid

        #TEST IF CONFIG FILE IS USED
        if from_file:
            #CONFIG KEYS TO CHECK
            db_keys = ['server', 'database', 'user', 'password']

            #VERIFY REQUIRED FIELD EXIST IN CONFIG FILE
            creds = _dbconn_fields(dbtype=dbtype, fields=db_keys, filename=filename)

        else:
            #TEST PASSED PARAMETERS >> WRAP IN DICTIONARY
            creds = _dbconn_params(dbtype=dbtype, server=server, database=database,
                                   user=user, password=password)

        #TEST A VALID CREDENTIAL FILE WAS BUILT
        if creds is not None:
            #MAKE THE CONNECTION >> GET THE CONN/CUR OBJECTS
            return _dbconn_sql_conn(creds=creds)

    except Exception as err:
        #ALERT USER TO CONNECTION ERROR
        _UI.print_alert('\nAn error occurred while connecting to the SQL Server database.')
        _UI.print_error(err)


#-----------------------------------------------------------------------
#HELPER FUNCTION DESIGNED TO GET AND RETURN AN ODBC DRIVER NAME,
#USING REGEX
def getdrivername(drivername, returnall=False):

    '''
    DESIGN:
    Helper function designed to get and return the name of an ODBC
    driver.

    The argument can be formatted as a regex expression.  If multiple
    drivers are found, by default, only the first driver in the list is
    returned.
    However, the returnall parameter toggles this action.

    This function has a dependency on pyodbc. Therefore,
    the utils.testimport() function is called before pyodbc it is
    imported. If the pyodbc library is not installed, the user is
    notified.

    PARAMETERS:
        - drivername
          the name of the driver you're looking for. should be
          formatted as regex.
        - returnall (default=False)
          return all drivers found.

    DEPENDENCIES:
    - re
    - pyodbc

    USE:
    > driver = getdrivername(drivername='SQL Server.*')
    '''

    import re

    #TEST FOR LIBRARY BEFORE TRYING TO IMPORT
    if testimport('pyodbc'):

        import pyodbc

        #TEST IF USER WANTS ALL DRIVERS RETURNED
        if returnall:
            #RETURN ALL
            return [driver for driver in pyodbc.drivers() if re.search(drivername, driver)]
        else:
            #GET / RETURN THE ODBC DRIVER NAME FOR SQL SERVER
            return [driver for driver in pyodbc.drivers() if re.search(drivername, driver)][0]


#-----------------------------------------------------------------------
#FUNCTION USED TO TEST IF A LIBRARY IS INSTALLED.
#USED BEFORE IMPORTING AN 'OBSCURE' LIBRARY.
def testimport(module_name):

    '''
    DESIGN:
    This is a small helper function designed to test if a
    module/library is installed before trying to import it.

    This can be useful when a method requires an 'obscure' library, and
    importing on a deployment environment where the library is not
    installed, could have adverse effects.

    If the library is not intalled, the user is notified.

    PARAMETERS:
        - module_name
          the name of the module you're testing is installed.

    DEPENDENCIES:
    - imp

    USE:
    > import utils.utils as u
    > if u.testimport('mymodule'): import mymodule
    '''

    import imp

    found = False

    try:
        imp.find_module(module_name)
        found = True
    except ImportError:
        found = False
        print '\nSorry ... the (%s) library/module is not installed.' % (module_name)

    return found


#-----------------------------------------------------------------------
#FUNCTION USED TO CLEAN HEADERS AND DATAFRAME VALUES
def clean_df(df):

    '''
    DESIGN:
    Function designed to clean dataframe content.
        - column names: replace a space with an underscore
        - column names: convert to lower case
        - values:       strip whitespace

    Function returns a 'cleaned' copy of the dataframe.

    PARAMETERS:
        - df
          The pandas dataframe for cleaning.

    DEPENDENTS:
        - numpy

    USE:
    > import utils.utils as u
    > df = u.clean_df(df)
    '''

    import numpy as np

    #CREATE A COPY OF THE DATAFRAME
    df_c = df.copy()

    #CLEAN HEADERS (REPLACE, STRIP WHITESPACE, UPPER CASE)
    df_c.rename(columns=lambda col: col.strip().replace(' ', '_').lower(), inplace=True)

    #STRIP WHITESPACE FROM VALUES
    for col in df_c.columns:
        #TEST FOR NUMBER AND DATETIME TYPES
        if not np.issubdtype(df_c[col], np.datetime64) and not np.issubdtype(df_c[col], np.number):
            #STRIP WHITESPACE
            df_c[col] = df_c[col].str.strip()

    #RETURN CLEANED DATAFRAME
    return df_c


#-----------------------------------------------------------------------
#FUNCTION USED TO TEST IF A FILE EXISTS AND NOTIFY THE USER IF IT
#DOESN'T EXIST
def fileexists(filepath):

    '''
    DESIGN:
    Function designed check if a file exists.  A boolean value is
    returned to the calling program.

    This function expands in the standard os.path.isfile() function in
    that the user is automatically notified if the path does not exist.

    PARAMETERS:
        - filepath
          the file path you are testing

    DEPENDENCIES:
    - os

    USE:
    > import util.utils as u
    > if u.fileexists(filepath='/path/to/file.ext'): do stuff ...
    '''

    import os

    #INITIALISE VARIABLE
    found = False

    #TEST IF FILE EXISTS
    if os.path.isfile(filepath):
        #SET FLAG
        found = True
    else:
        #NOTIFY USER
        print 'the requested file cannot be found: (%s)\n' % filepath
        #SET FLAG
        found = False

    #RETURN BOOLEAN TO PROGRAM
    return found


#-----------------------------------------------------------------------
#FUNCTION USED TO TEST IF A DIRECTORY PATH EXISTS
#DEFAULT ACTION IS TO CREATE THE PATH, IF IT DOESN'T EXIST
def direxists(path, create_path=True):

    '''
    DESIGN:
    Function designed to test if a directory path exists.  If the path
    does not exist, the path can be created; determined by passed the
    value of create_path(boolean).

    This function expands in the standard os.path.exists() function in
    that the path can be created, if it doesn't already exist, by
    passing the create_path parameter as True; which is the default
    action.

    PARAMETERS:
        - path
          the directory you are testing
        - create_path (default=True)

    DEPENDENCIES:
    - os

    USE:
    > import utils.utils as u
    > u.direxists(path[, create_path])
    '''

    import os

    #INITIALISE VARIABLE
    found = False

    #LOOP
    while True:
        #TEST IF PATH EXISTS
        if os.path.exists(path):
            #FLAG AS FOUND
            found = True
            #EXIT LOOP
            break
        else:
            #TEST IF DIRECTORY PATH SHOULD BE CREATED
            if create_path is True:
                #CREATE PATH
                os.makedirs(path)
            else:
                #DO NOT CREATE > EXIT LOOP
                break

    #RETURN IF DIRECTORY WAS FOUND
    return found


#-----------------------------------------------------------------------
#FUNCTION USED TO READ A JSON FILE, AND RETURN A DICTIONARY
def json_read(filepath):

    '''
    DESIGN:
    Function designed to read a JSON file, and return the values as a
    dictionary.

    This utility is useful when reading a json config file for a python
    program.

    PARAMETERS:
        - filepath
          path to the JSON file to read.

    DEPENDENCIES:
    - json

    USE:
    > import utils.utils as u
    > vals = u.json_read(filepath=/path/to/file.json)
    '''

    import json

    #TEST IF FILE EXISTS
    if fileexists(filepath):

        #OPEN JSON FILE / STORE VALUES TO DICTIONARY
        with open(filepath, 'r') as infile:
            vals = json.load(infile)

        #RETURN DICTIONARY TO PROGRAM
        return vals


#-----------------------------------------------------------------------
#METHOD USED TO WRITE A JSON FILE, FROM A PASSED DICTIONARY
def json_write(dictionary, filepath='c:/temp/tempfile.json'):

    '''
    DESIGN:
    Method designed to write a python dictionary to a JSON file in the
    specified file location.

    If a file is not specified, the default file and location is:
    c:/temp/tempfile.json

    This utility is useful when creating a json config file.

    PARAMETERS:
        - dictionary
          the python dictionary you are converting to a json file.
        - filepath
          the path and filename for the output json file.

    DEPENDENCIES:
    - json

    USE:
    > import utils.utils as u
    > u.json_write(dictionary=mypy_dict[,
                   filepath='/path/to/output.json'])
    '''

    import json

    #OPEN / WRITE JSON FILE
    with open(filepath, 'w') as outfile:
        json.dump(dictionary, outfile, sort_keys=True)


#-----------------------------------------------------------------------
#FUNCTION FOR DECODING UNICODE AND RETURNING AS STRING
def unidecode(string):

    '''
    DESIGN:
    Method designed to test a passed string for being unicode type,
    then return a decoded string value.

    If the passed string is not unicode, the original value is
    returned.

    PARAMETERS:
        - string
          the unicode string you wish to test/decode.

    DEPENDENCIES:
    - unidecode

    USE:
    > import utils.utils as u
    > s = u.unidecode(string)
    '''

    from unidecode import unidecode

    #INITIALISE VARIABLE
    decoded = None

    #TEST PASSED VALUE AS BEING UNICODE > STORE DECODED (OR ORIGINAL) VALUE
    decoded = unidecode(string) if isinstance(string, unicode) else string

    #RETURN VALUE
    return decoded
