'''------------------------------------------------------------------------------------------------
Program:    utils.py
Version:    3.1.1
Py Ver:     2.7
Purpose:    Central library standard s3dev utilities.

Dependents: _version
            cx_Oracle
            datetime
            imp
            json
            matplotlib
            numpy
            os
            plotly
            pyodbc
            re
            unidecode

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
------------------------------------------------------------------------------------------------'''

#-----------------------------------------------------------------------
#SET VERSION NUMBER
from _version_utils import __version__


#-----------------------------------------------------------------------
#METHOD USED FOR DEPLOYMENT TESTING
def __test():

    '''
    DESIGN:
    Method used for testing only.
    '''
    print 'This is only a test.'


#-----------------------------------------------------------------------
#FUNCTION RETURNS A LIST OF CONVERTED VALUES FROM A MATPLOTLIB COLORMAP
def getcolormap(colormap='Blues', n=5, dtype='hex', preview=False, preview_in='mpl'):

    '''
    DESIGN:
    Function designed to return a list of colour values from a
    matplotlib colormap.  The number of returned color values can
    range from 1 to 256.

    This is useful when creating a graph which requires gradient
    colour map. (e.g.: a plotly bar chart)

    To list matplotlib color maps:
    > from matplotlib.pyplot import colormaps
    > colormaps()

    PARAMETERS:
        - colormap (default='Blues')
          name of the matplotlib color map
        - n  (default=1)
          number of colors to return
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

    return colors


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
#FROM: (2010:01:31 12:31:18)
#TO:   (20100131123118)
def format_exif_date(datestring):

    '''
    DESIGN:
    Function designed to convert the exif date/timestamp
    from 2010:01:31 12:31:18 format to 20100131123118 format for easy
    sorting.

    This is useful for storing an exif date as a datetime string.

    PARAMETERS:
        - datestring
          the datetime string to be converted
          note: this function is looking for an exif datetime string.
          (yyyy:mm:dd hh:mi:ss)

    DEPENDENCIES:
    - datetime

    USE:
    > import utils.utils as u
    > newdate = u.format_exif_date('2010:01:31 12:31:18')
    '''

    from datetime import datetime as dt

    inmask  = '%Y:%m:%d %H:%M:%S'
    outmask = '%Y%m%d%H%M%S'

    #PARSE DATETIME STRING
    parsed = dt.strptime(datestring, inmask)

    #RETURN FORMATTED STRING
    return dt.strftime(parsed, outmask)


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
    import reporterror

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
def dbconn_oracle(host=None, userid=None, password=None):

    '''
    DESIGN:
    Function designed to create a connection to an Oracle database
    using the provided login details.  If a login detail is not
    provided, the user is prompted.
    This can be used as a security feature,

    The connection is tested.  If successful, the connection and
    cursor objects are returned to the calling program, as a
    dictionary.

    conn = [the connection object]
    cur  = [the cursor object]

    NOTE: To prompt for login details, leave the argument(s) blank.

    PARAMETERS:
        - host (default=None)
          database host; or database name
        - userid (default=None)
          user id; or schema name
        - password (default=None)
          just what it says on the tin  :-)

    DEPENDENCIES:
    - cx_Oracle

    USE:
    > import utils.utils as u
    > dbo = u.dbconn_oracle(host, userid, password)
    > conn = dbo['conn']
    > cur = dbo['cur']
    '''

    import cx_Oracle as o

    #TEST FOR PASSED ARGUMENTS >> PROMPT FOR DATABASE USER CREDENTIALS
    if host is None: host = raw_input('oracle host name: ')
    if userid is None: userid = raw_input('oracle userid: ')
    if password is None: password = raw_input('oracle password (for %s): ' % userid)

    #BUILD CONNECTION STRING
    connstring = '%s/%s@%s' % (userid, password, host)

    try:
        #CREATE CONNECTION / CURSOR OBJECTS
        connection = o.connect(connstring)
        cursor = connection.cursor()

        #STORE RESULT IN DICTIONARY
        output = dict(conn=connection, cur=cursor)

    except Exception as err:
        #ALERT USER TO CONNECTION ERROR
        raise ValueError('the database connection failed for (host: %s, userid: %s, pw: %s)' \
                         % (host, userid, 'xxx...' + password[-3:]) + '\n' + str(err))

    #RETURN CONNECTION / CURSOR OBJECTS TO PROGAM
    return output


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
#FUNCTION DESIGNED CREATE A SQL SERVER DB CONN; USER PROMPTED FOR
#DETAILS.
def dbconn_sql(server=None, database=None, userid=None, password=None):

    '''
    DESIGN:
    Function designed to create a connection to a SQL Server database
    using the provided login parameters.  If a login detail is not
    provided, the user is prompted.
    This can be used as a security feature,

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
        - userid (default=None)
          just what it says on the tin
        - password (default=None)
          again, just what it says on the tin  ;-)

    DEPENDENCIES:
        - pyodbc

    USE:
    > import utils.utils as u
    > dbo = u.dbconn_sql(server, database, userid, password)
    > conn = dbo['conn']
    > cur = dbo['cur']
    '''

    import pyodbc

    #TEST FOR PASSED ARGUMENTS >> PROMPT FOR DATABASE USER CREDENTIALS
    if server is None: server = raw_input('sql server name: ')
    if database is None: database = raw_input('sql database name: ')
    if userid is None: userid = raw_input('sql userid: ')
    if password is None: password = raw_input('sql password (for %s): ' % userid)

    try:
        #BUILD CONNECTION STRING >> CONNECT
        connection = pyodbc.connect('Driver={%s};'
                                    'Server=%s;'
                                    'Database=%s;'
                                    'UID=%s;'
                                    'PWD=%s;' %
                                    (getdrivername('SQL Server.*'), server, \
                                                                    database, \
                                                                    userid, \
                                                                    password))

        #CREATE CURSOR OBJECT
        cursor = connection.cursor()

        #STORE RESULT IN DICTIONARY
        output = dict(conn=connection, cur=cursor)

    except Exception as err:
        #ALERT USER TO CONNECTION ERROR
        raise ValueError('the database connection failed for (server: %s, userid: %s, pw: %s)' \
                         % (server, userid, 'xxx...' + password[-3:]) + '\n' + str(err))

    #RETURN CONNECTION / CURSOR OBJECTS TO PROGAM
    return output


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
    bValue = False

    #TEST IF FILE EXISTS
    if os.path.isfile(filepath):
        #SET FLAG
        bValue = True
    else:
        #NOTIFY USER
        print 'the requested file cannot be found: (%s)\n' % filepath
        #SET FLAG
        bValue = False

    #RETURN BOOLEAN TO PROGRAM
    return bValue


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
    bFound = False

    #LOOP
    while True:
        #TEST IF PATH EXISTS
        if os.path.exists(path):
            #FLAG AS FOUND
            bFound = True
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
    return bFound


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


#-----------------------------------------------------------------------
#-----------------------------------------------------------------------
#               -----     DEPRECIATED / REMOVED    -----
#                 TO BE REMOVED ON NEXT MAJOR REVISION
#-----------------------------------------------------------------------
#-----------------------------------------------------------------------

#METHOD FOR DISPLAYING VERSION AND HELP INFORMATION
#REPLACED WITH: n/a
def ArgvParse(Arguments=None):

    '''
    WARNING:
    This method has been removed as of utils v3.0.0, and is no
    longer accessible.

    RECOMMENDED ALTERNATIVE(S):
    - argparse (standard python library)
    '''

    print ArgvParse.__doc__


#-----------------------------------------------------------------------
#FUNCTION USED TO CLEAR HEADERS AND DATA IN A DATAFRAME
#REPLACED WITH: clean_df()
def CleanDF(dfData):

    '''
    WARNING:
    This function has been depreciated and is no longer in use as of
    utils v3.0.0.

    ACTION:
    Revise your source code to use the 'utils.clean_df()' function.

    FALLBACK:
    In the mean-time, I'll pass your request to the clean_df()
    function; but remember to update your source.
    '''

    print CleanDF.__doc__

    #PASS CODE ON TO NEW FUNCTION
    return clean_df(df=dfData)


#-----------------------------------------------------------------------
#FUNCTION USED TEST IF A DIRECTORY PATH EXISTS
#REPLACED WITH: direxists()
def DirExists(FilePath, CreatePath=True):

    '''
    WARNING:
    This function has been depreciated and is no longer in use as of
    utils v3.0.0.

    ACTION:
    Revise your source code to use the 'utils.direxists()' function.

    FALLBACK:
    In the mean-time, I'll pass your request to the direxists()
    function; but remember to update your source.
    '''

    print DirExists.__doc__

    #PASS CODE ON TO NEW FUNCTION
    return direxists(path=FilePath, create_path=CreatePath)


#-----------------------------------------------------------------------
#FUNCTION USED TO TEST IF A FILE EXISTS AND NOTIFY THE USER IF IT
#DOESNT EXIST
#REPLACED WITH: fileexists()
def FileExists(FilePath):

    '''
    WARNING:
    This function has been depreciated and is no longer in use as of
    utils v3.0.0.

    ACTION:
    Revise your source code to use the 'utils.fileexists()' function.

    FALLBACK:
    In the mean-time, I'll pass your request to the fileexists()
    function; but remember to update your source.
    '''

    print FileExists.__doc__

    #PASS CODE ON TO NEW FUNCTION
    return fileexists(filepath=FilePath)


#-----------------------------------------------------------------------
#FUNCTION RETURNS A LIST OF CONVERTED VALUES FROM A MATPLOTLIB COLORMAP
#REPLACED WITH: getcolormap()
def GetColourMap(Map='Blues', N=1, DType='HEX'):

    '''
    WARNING:
    This function has been depreciated and is no longer in use as of
    utils v3.0.0.

    NOTABLE CHANGES:
    - The spelling of GetColourMap has changed to drop the 'u' for
      standardised spelling.
    - The Map parameter has changed to colormap.

    ACTION:
    Revise your source code to use the 'utils.getcolormap()' function.
    Also, note the change in name and/or case for the passed
    parameters.

    FALLBACK:
    In the mean-time, I'll pass your request to the getcolormap()
    function; but remember to update your source.
    '''

    print GetColourMap.__doc__

    #PASS CODE ON TO NEW FUNCTION
    return getcolormap(colormap=Map, n=N, dtype=DType)


#-----------------------------------------------------------------------
#FUNCTION USED TO GET AND RETURN A CONFIG FILE AS A DICTIONARY
#REPLACED WITH: n/a
def GetConfig(FilePath=None):

    '''
    WARNING:
    This method has been removed as of utils v3.0.0, and is no
    longer accessible.

    RECOMMENDED ALTERNATIVE(S):
    - config.loadconfig() (s3dev config library)
    '''

    print GetConfig.__doc__


#-----------------------------------------------------------------------
#HELPER FUNCTION DESIGNED TO GET AND RETURN AN ODBC DRIVER NAME,
#USING REGEX
#REPLACED WITH: getdrivername()
def GetDriverName(re_DriverName):

    '''
    WARNING:
    This function has been depreciated and is no longer in use as of
    utils v3.0.0.

    NOTABLE CHANGES:
    - The method name has changed to lower case.
    - The re_DriverName parameter has changed to drivername.
    - A returnall parameter has been added.

    ACTION:
    Revise your source code to use the 'utils.getdrivername()'
    function. Also, note the change in name and/or case for the passed
    parameters.

    FALLBACK:
    In the mean-time, I'll pass your request to the getdrivername()
    function; but remember to update your source.
    '''

    print GetDriverName.__doc__

    return getdrivername(drivername=re_DriverName)


#-----------------------------------------------------------------------
#FUNCTION FOR DECODING UNICODE AND RETURNING AS STRING
#REPLACED WITH: unidecode()
def Unidecode(string):

    '''
    WARNING:
    This function has been depreciated and is no longer in use as of
    utils v3.0.0.

    NOTABLE CHANGES:
    - The method name has changed to lower case.

    ACTION:
    Revise your source code to use the 'utils.unidecode()' function.
    Also, note the change in name and/or case for the passed
    parameters.

    FALLBACK:
    In the mean-time, I'll pass your request to the unidecode()
    function; but remember to update your source.
    '''

    print Unidecode.__doc__

    return unidecode(string=string)


#-----------------------------------------------------------------------
#FUNCTION DESIGNED TO GET AND UPDATE A COLOUR MAP FROM BREWER2MPL FOR
#USE IN PLOTLY
#REPLACED WITH: n/a
def colours_addRGB(colorset=None, category=None, count=None):

    '''
    WARNING:
    This method has been removed as of utils v3.0.0, and is no
    longer accessible.

    RECOMMENDED ALTERNATIVE(S):
    - utils.getcolormap()  -  (contained in this module)
    '''

    print colours_addRGB.__doc__


#-----------------------------------------------------------------------
#FUNCTION DESIGNED TO GET AND UPDATE A COLOUR MAP FROM BREWER2MPL FOR
#USE IN PLOTLY
#REPLACED WITH: n/a
def colours_addRGBA(colorset=None, category=None, count=None, alpha=None):

    '''
    WARNING:
    This method has been removed as of utils v3.0.0, and is no
    longer accessible.

    RECOMMENDED ALTERNATIVE(S):
    - utils.getcolormap() (s3dev utils method; using matplotlib colormaps)
    '''

    print colours_addRGBA.__doc__


#-----------------------------------------------------------------------
#FUNCTION USED TO READ A JSON FILE, AND RETURN A DICTIONARY
#REPLACED WITH: json_read()
def jsonRead(FilePath):

    '''
    WARNING:
    This function has been depreciated and is no longer in use as of
    utils v3.0.0.

    NOTABLE CHANGES:
    - The method name has changed format and to lower case.
    - The parameter(s) has changed case.

    ACTION:
    Revise your source code to use the 'utils.json_read()' function.
    Also, note the change in name and/or case for the passed
    parameters.

    FALLBACK:
    In the mean-time, I'll pass your request to the json_read()
    function; but remember to update your source.
    '''

    print jsonRead.__doc__

    return json_read(FilePath)


#-----------------------------------------------------------------------
#FUNCTION USED TO WRITE A JSON FILE, FROM A PASSED DICTIONARY
#REPLACED WITH: json_write()
def jsonWrite(Dictionary, FilePath='c:/temp/tempfile.json'):

    '''
    WARNING:
    This function has been depreciated and is no longer in use as of
    utils v3.0.0.

    NOTABLE CHANGES:
    - The method name has changed format and to lower case.
    - The parameter(s) has changed case.

    ACTION:
    Revise your source code to use the 'utils.json_write()' method.
    Also, note the change in name and/or case for the passed
    parameters.

    FALLBACK:
    In the mean-time, I'll pass your request to the json_write()
    method; but remember to update your source.
    '''

    print jsonWrite.__doc__

    return json_write(Dictionary, FilePath)


#-----------------------------------------------------------------------
#FUNCTION DESIGNED TO CONVERT EXIF DATE
#FROM: (2010:01:31 12:31:18)
#TO:   (20100131123118)
#REPLACED WITH: format_exif_date()
def format_exifDate(value):

    '''
    WARNING:
    This function has been depreciated and is no longer in use as of
    utils v3.0.0.

    NOTABLE CHANGES:
    - The method name has changed format and to lower case.
    - The parameter name has changed to datestring.

    ACTION:
    Revise your source code to use the 'utils.format_exif_date()'
    function. Also, note the change in name and/or case for the passed
    parameters.

    FALLBACK:
    In the mean-time, I'll pass your request to the format_exif_date()
    function; but remember to update your source.
    '''

    print format_exifDate.__doc__

    return format_exif_date(datestring=value)


#-----------------------------------------------------------------------
#FUNCTION DESIGNED CREATE AN ORACLE DB CONN; USER PROMPTED FOR DETAILS.
#REPLACED WITH: dbconn_oracle()
def dbConn_Oracle(host=None, userid=None, password=None):

    '''
    WARNING:
    This function has been depreciated and is no longer in use as of
    utils v3.0.0.

    NOTABLE CHANGES:
    - The method name has changed to lower case.

    ACTION:
    Revise your source code to use the 'utils.dbconn_oracle()'
    function.

    FALLBACK:
    In the mean-time, I'll pass your request to the dbconn_oracle()
    function; but remember to update your source.
    '''

    print dbConn_Oracle.__doc__

    return dbconn_oracle(host=host, userid=userid, password=password)


#-----------------------------------------------------------------------
#FUNCTION DESIGNED CREATE A SQL SERVER DB CONN; USER PROMPTED FOR
#DETAILS.
#REPLACED WITH: dbconn_sql()
def dbConn_SQL(server=None, database=None, userid=None, password=None):

    '''
    WARNING:
    This function has been depreciated and is no longer in use as of
    utils v3.0.0.

    NOTABLE CHANGES:
    - The method name has changed to lower case.

    ACTION:
    Revise your source code to use the 'utils.dbconn_sql()' function.

    FALLBACK:
    In the mean-time, I'll pass your request to the dbconn_sql()
    function; but remember to update your source.
    '''

    print dbConn_SQL.__doc__

    return dbconn_sql(server=server, database=database, userid=userid, password=password)
