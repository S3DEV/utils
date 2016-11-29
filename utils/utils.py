'''------------------------------------------------------------------------------------------------
Program:    utils.py
Version:    2.3.1
Py Ver:     2.7
Purpose:    Centralised location for reusable utilities.

Dependents: _version
            palettable
            numpy
            cx_Oracle
            json
            unidecode
            matplotlib
            pyodbc

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
14.11.06    J. Berendt      2.3.0       Added a utility to extract the hex (or specified dtype)
                                        color values from a matplotlib colour map.
                                        This is useful when creating a color gradient for plotly
                                        graphs (e.g.: bar charts).
28.11.06    J. Berendt      2.3.1       Updated setup.py to grab / install dependencies.
                                        Updated _version code to be more concise.
------------------------------------------------------------------------------------------------'''

#--------------------------------------------------------------------------------------------------
#SET VERSION NUMBER       
from _version import __version__ as __version__

    
#--------------------------------------------------------------------------------------------------
#METHOD USED FOR DEPLOYMENT TESTING
def Test():
    print 'This is only a test.'

    
#--------------------------------------------------------------------------------------------------
#FUNCTION DESIGNED TO GET AND UPDATE A COLOUR MAP FROM BREWER2MPL FOR USE IN PLOTLY
def colours_addRGB(colorset, category, count):
    
    '''
    DESIGN:
    Function designed to get a colour map from palettable.colorbrewer library.
    Colourmap list is then updated to include 'N, rgb' prior to each colour in the list.
    
    This is useful when automating colour maps for Plot.ly, as the number and 'rgb' is 
    required before each colour.
    
    USE:
    > from utils.utils import colours_addRGB as _addRGB
    > cmap = _addRGB('Blues', 'sequential', 3)
    > 
    > for x in cmap: print x
    >   [0.0, 'rgb(222, 235, 247)']
    >   [0.5, 'rgb(158, 202, 225)']
    >   [1.0, 'rgb(49, 130, 189)']
    '''
        
    import palettable.colorbrewer as cb
    import numpy as np

    #INITIALISE VARIABLES
    colors = list()
    indx = 0

    #SETUP COLOUR MAP
    cmap = cb.get_map(colorset, category, count)
    #SETUP INTERVAL FOR LIST[0] NUMBER    
    i = np.linspace(0, 1, len(cmap.colors))
    
    #ITERATE THROUGH COLOUR MAP    
    for x in cmap.colors:
        
        #COMPILE THE PARSED / UPDATED COLOUR AND ADD TO THE LIST
        colors.append([i[indx], 'rgb(%d, %d, %d)' % (x[0], x[1], x[2])])

        #INCREMENT THE INDEX COUNTER
        indx = indx + 1
        
    #RETURN FUNCTION VALUES AS A LIST
    return colors


#--------------------------------------------------------------------------------------------------
#FUNCTION DESIGNED TO GET AND UPDATE A COLOUR MAP FROM BREWER2MPL FOR USE IN PLOTLY
def colours_addRGBA(colorset, category, count, alpha):
    
    '''
    DESIGN:
    Function designed to get a colour map from palettable.colorbrewer library; and include the alpha parameter.
    Colourmap list is then updated to include 'N, rgba' prior to each colour in the list.
    
    This is useful when automating colour maps for Plot.ly, as the number, 'rgba' and the
    alpha value are required before each colour.
    
    USE:
    > from utils.utils import colours_addRGBA as _addRGBA
    > cmap = _addRGBA('Blues', 'sequential', 3, 0.75)
    > 
    > for x in cmap: print x
    >   [0.0, 'rgba(222, 235, 247, 0.75)']
    >   [0.5, 'rgba(158, 202, 225, 0.75)']
    >   [1.0, 'rgba(49, 130, 189, 0.75)']
    '''
        
    import palettable.colorbrewer as cb
    import numpy as np

    #INITIALISE VARIABLES
    colors = list()
    indx = 0
    
    #SETUP COLOUR MAP
    cmap = cb.get_map(colorset, category, count)
    #SETUP INTERVAL FOR LIST[0] NUMBER    
    i = np.linspace(0, 1, len(cmap.colors))
    
    #ITERATE THROUGH COLOUR MAP    
    for x in cmap.colors:
        
        #COMPILE THE PARSED / UPDATED COLOUR AND ADD TO THE LIST
        colors.append([i[indx], 'rgba(%d, %d, %d, %f)' % (x[0], x[1], x[2], alpha)])

        #INCREMENT THE INDEX COUNTER
        indx = indx + 1
        
    #RETURN FUNCTION VALUES AS A LIST
    return colors


#FUNCTION DESIGNED TO RETURN A LIST OF CONVERTED VALUES FROM A MATPLOTLIB COLORMAP
def GetColourMap(Map='Blues', N=1, DType='HEX'):
    
    '''
    DESIGN:
    Function designed to return a list of converted values from a matplotlib colormap.
    The number of returned color values can range from 1 to 256.
    
    This is useful when creating a graph which requires gradient colour map.
    (e.g.: a Plotly bar chart)

    To list matplotlib color maps:
    > from matplotlib.pyplot import colormaps
    > colormaps()

    PARAMETERS:
    Map     = Name of the matplotlib color map  (Default = Blues)
    N       = Number of colors to return        (Default = 1)
    DType    = Data type to return              (Default = HEX)

    DEPENDENCIES:
    - matplotlib
    
    USE:
    > from utils.utils import GetColourMap_hex
    > c = GetColourMap(Map='spring', N=50, DType='hex')
    '''
    
    from matplotlib import cm
    from matplotlib.colors import rgb2hex

    #CREATE A COLOR MAP OBJECT (MAP, NUMBER OF VALUES)
    cmap = cm.get_cmap(Map, N)

    #TEST FOR DTYPE >> COMPILE / RETURN A LIST OF RGB2HEX CONVERTED COLORS
    if DType.upper() == 'HEX': return [rgb2hex(cmap(i)[:3]) for i in range(cmap.N)]


#--------------------------------------------------------------------------------------------------
#FUNCTION DESIGNED TO CONVERT EXIF DATE FROM (2010:01:31 12:31:18) TO (20100131123118)
def format_exifDate(value):
    
    '''
    DESIGN:
    Function designed to convert the exif datetime stamp from 2010:01:31 12:31:18 format
    to 20100131123118 format for easy sorting.
    
    This is useful when automating colour maps for Plot.ly, and sorting the colourmap
    based on datetime.
    
    USE:
    > from utils.utils import format_exifDate as _exifDate
    > newdate = _exifDate('2010:01:31 12:31:18')
    '''
    
    #REFORMAT EXIF DATE TO NUMBER
    x = str(value).replace(':', '').replace(' ', '') if value != None else '20000101000000'

    #RETURN VALUE
    return x
    
    
#--------------------------------------------------------------------------------------------------
#FUNCTION DESIGNED CREATE AN ORACLE DATABASE CONNECTION; PROMPTING THE USER FOR USER DETAILS.
def dbConn_Oracle(host=None, userid=None, password=None):
    
    '''
    DESIGN:
    Function designed to create a connection to an Oracle database using parameters provided by
    the user / calling program.
    
    The connection is tested.  If successful, the connection and cursor objects are returned
    to the calling program, via a dictionary.
    
    conn    = [the connection object]
    cur     = [the cursor object]
    
    DEPENDENCIES:
        - cx_Oracle
    
    USE:
    > from utils.utils import dbConn_Oracle as _Oracle
    > dbo = _Oracle(host, userid, password)     NOTE: To prompt the user, leave the argument(s) blank
    > conn = dbo['conn']
    > cur = dbo['cur']
    '''
    
    import cx_Oracle as o

    #TEST FOR PASSED ARGUMENTS >> PROMPT FOR DATABASE USER CREDENTIALS
    if host == None:     host = raw_input('db oracle host name: ')
    if userid == None:   userid = raw_input('db oracle userid: ')
    if password == None: password = raw_input('db oracle password (for %s): ' % userid)

    #BUILD CONNECTION STRING
    connstring = userid + '/' + password + '@' + host
    
    try:
        #CREATE CONNECTION / CURSOR OBJECTS
        connection = o.connect(connstring)
        cursor = connection.cursor()

        #STORE RESULT IN DICTIONARY
        output = dict(conn=connection, cur=cursor)

    except Exception as e:
        #ALERT USER TO CONNECTION ERROR
        raise ValueError('the database connection failed for (host: %s, userid: %s, pw: %s)' % (host, userid, 'xxx...' + password[-3:]) + '\n' + str(e))
    
        #STORE NULL RESULT
        output =  None
        
    #RETURN CONNECTION / CURSOR OBJECTS TO PROGAM
    return output

#--------------------------------------------------------------------------------------------------
#HELPER FUNCTION DESIGNED TO GET AND RETURN AN ODBC DRIVER NAME, USING REGEX
def GetDriverName(re_DriverName):

    '''
    DESIGN:
    Helper function designed to get and return the name of an ODBC driver.
        
    The argument should be formatted as a regex expression.  If multiple drivers are found, 
    the first driver in the list is returned.
    
    DEPENDENCIES:
        - re
        - pyodbc
    
    USE:
    > driver = GetDriverName('SQL Server.*')
    '''
    
    import re
    import pyodbc
    
    #GET / RETURN THE ODBC DRIVER NAME FOR SQL SERVER
    return [driver for driver in pyodbc.drivers() if re.search(re_DriverName, driver)][0]


#--------------------------------------------------------------------------------------------------
#FUNCTION DESIGNED CREATE AN ORACLE DATABASE CONNECTION; PROMPTING THE USER FOR USER DETAILS.
def dbConn_SQL(server=None, database=None, userid=None, password=None):
    
    '''
    DESIGN:
    Function designed to create a connection to a SQL Server database using parameters provided by
    the user / calling program.
    
    The connection is tested.  If successful, the connection and cursor objects are returned
    to the calling program, via a dictionary.
    
    conn    = [the connection object]
    cur     = [the cursor object]
    
    DEPENDENCIES:
        - pyodbc
    
    USE:
    > from utils.utils import dbConn_SQL as _SQL
    > dbo = _SQL(server, database, userid, password)     NOTE: To prompt the user, leave the argument(s) blank
    > conn = dbo['conn']
    > cur = dbo['cur']
    '''
    
    import pyodbc

    #TEST FOR PASSED ARGUMENTS >> PROMPT FOR DATABASE USER CREDENTIALS
    if server == None:      server = raw_input('db sql server name: ')
    if database == None:    database = raw_input('db sql database name: ')
    if userid == None:      userid = raw_input('db sql userid: ')
    if password == None:    password = raw_input('db sql password (for %s): ' % userid)


    try:
        #BUILD CONNECTION STRING >> CONNECT
        connection = pyodbc.connect('Driver={%s};'
                                    'Server=%s;'
                                    'Database=%s;'
                                    'UID=%s;'
                                    'PWD=%s;' %
                                    (GetDriverName('SQL Server.*'), server, database, userid, password))
    
        #CREATE CURSOR OBJECT
        cursor = connection.cursor()

        #STORE RESULT IN DICTIONARY
        output = dict(conn=connection, cur=cursor)

    except Exception as e:
        #ALERT USER TO CONNECTION ERROR
        raise ValueError('the database connection failed for (server: %s, userid: %s, pw: %s)' % (server, userid, 'xxx...' + password[-3:]) + '\n' + str(e))
    
        #STORE NULL RESULT
        output =  None
        
    #RETURN CONNECTION / CURSOR OBJECTS TO PROGAM
    return output
    
    
#--------------------------------------------------------------------------------------------------
#FUNCTION USED TO CLEAR HEADERS AND DATA IN A DATAFRAME
def CleanDF(dfData):
    
    '''
    DESIGN:
    Function designed to clean dataframe content.
        - column names: replace a space with an underscore
        - column names: convert to lower case
        - values:       strip whitespace
        
    The function will return a 'cleaned' dataframe to the program.
    
    USE:
    > from utils.utils import CleanDF as _CleanDF
    > dfCleaned = _CleanDF(dfData)
    '''
    
    #CLEAN HEADERS (REPLACE, STRIP WHITESPACE, LOWER CASE)
    dfData.rename(columns=lambda col: col.strip().replace(' ', '_').lower(), inplace=True)
    
    #STRIP WHITESPACE FROM VALUES
    for x in dfData.columns:
        #TEST FOR FLOAT TYPE
        if 'float' not in str(dfData[x].dtype) and 'int' not in str(dfData[x].dtype):
            #STRIP WHITESPACE
            dfData[x] = dfData[x].str.strip()

    #RETURN CLEANED DATAFRAME
    return dfData


#--------------------------------------------------------------------------------------------------
#FUNCTION USED TO TEST IF A FILE EXISTS AND NOTIFY THE USER IF IT DOESN'T EXIST.
def FileExists(FilePath):
    
    '''
    DESIGN:
    Function designed check if a file exists.  A boolean value is returned to the calling 
    program.
    
    If the file does not exist, the user is notified.
            
    USE:
    > from util.utils import FileExists as _FileExists
    > if _FileExists(FilePath=path\\file.ext): do stuff ...
    '''

    import os
    
    #INITIALISE VARIABLE
    bValue = False    
    
    #TEST IF FILE EXISTS
    if os.path.isfile(FilePath):
        #SET FLAG
        bValue = True
    else:
        #NOTIFY USER
        print 'the requested file cannot be found: (%s)' % FilePath
        #SET FLAG        
        bValue = False
    
    #RETURN BOOLEAN TO PROGRAM
    return bValue
    

#--------------------------------------------------------------------------------------------------
#FUNCTION USED TEST IF A DIRECTORY PATH EXISTS > DEFAULT IS TO CREATE THE DIRECTORY PATH
def DirExists(FilePath, CreatePath=True):
    
    '''
    DESIGN:
    Function designed to test if a directory path exists.  If the path does not exist, the path
    can be created; determined by passed the value of CreatePath (boolean).
    
    CreatePath default = True    
    
    USE:
    > from utils.utils import DirExists as _DirExists
    > _DirExists(FilePath, CreatePath)
    '''

    import os

    #INITIALISE VARIABLE    
    bFound = False
    
    #LOOP 
    while True:
        #TEST IF PATH EXISTS
        if os.path.exists(FilePath): 
            #FLAG AS FOUND
            bFound = True
            #EXIT LOOP
            break
        else:
            #TEST IF DIRECTORY PATH SHOULD BE CREATED
            if CreatePath == True:
                #CREATE PATH
                os.makedirs(FilePath)
            else:
                #DO NOT CREATE > EXIT LOOP
                break
    
    #RETURN IF DIRECTORY WAS FOUND
    return bFound


#--------------------------------------------------------------------------------------------------
#FUNCTION USED TO READ A JSON FILE, AND RETURN A DICTIONARY
def jsonRead(FilePath):
    
    '''
    DESIGN:
    Function designed to read a JSON file, and return the values as a dictionary.

    This utility is useful when reading a json config file for a Python program.
        
    USE:
    > from utils.utils import jsonRead as _jsonRead
    > dValues = _jsonRead(FilePath)
    '''

    import json

    #TEST IF FILE EXISTS    
    if FileExists(FilePath):
        
        #OPEN JSON FILE / STORE VALUES TO DICTIONARY
        with open(FilePath, 'r') as infile: dValues = json.load(infile)
    
        #RETURN DICTIONARY TO PROGRAM
        return dValues
    

#--------------------------------------------------------------------------------------------------
#FUNCTION USED TO WRITE A JSON FILE, FROM A PASSED DICTIONARY
def jsonWrite(Dictionary, FilePath='c:\\tempfile.json'):
    
    '''
    DESIGN:
    Function designed to write a JSON file to the specified file.
    
    If a file is not specified, C:\\tempfile.json is defaulted.
    
    This utility is useful when creating a json config file for a Python program.
        
    USE:
    > from utils.utils import jsonWrite as _jsonWrite
    > _jsonWrite(Dictionary, FilePath)
    '''

    import json

    #OPEN / WRITE JSON FILE
    with open(FilePath, 'w') as outfile: json.dump(Dictionary, outfile, sort_keys=True)
        

#--------------------------------------------------------------------------------------------------
#FUNCTION USED TO GET AND RETURN A CONFIG FILE AS A DICTIONARY
def GetConfig(FilePath):
    
    '''
    DESIGN:
    Function designed to get a return a JSON config file, as a dictionary.
    
    This utility is useful when loading a json config file for a Python program.
        
    USE:
    > from utils.utils import GetConfig as _GetConfig
    > config = _GetConfig(FilePath)
    '''

    #TEST IF FILE EXISTS > RETURN CONFIG FILE DICTIONARY
    if FileExists(FilePath): return jsonRead(FilePath)


#-------------------------------------------------------------------------
#METHOD FOR DISPLAYING VERSION AND HELP INFORMATION
def ArgvParse(Arguments):

    '''
    DESIGN:
    Method designed to provide help and versioning to command line programs.
    
    This method is designed to read the _version.txt and _help.txt files in
    the program's root directory.
        
    USE:
    > import sys
    > from utils.utils import ArgvParse as _ArgvParse
    >
    > def Main():
    >     #TEST NUMBER OF COMMAND LINE ARGUMENTS
    >     if len(sys.argv) > 1: _ArgvParse(sys.argv)
    '''
    
    import os
    import sys

    #PROGRAM PATH
    PATH_BASE = os.path.dirname(os.path.realpath(Arguments[0]))

    #SETUP VERSION AND HELP ARGUMENTS
    lVers = ['-v', '--v', '-version', '--version']
    lHelp = ['-h', '--h', '-help', '--help']

    #ITERATE THROUGH ARGUMENTS
    for arg in Arguments:
        #VERSION
        if arg.lower() in lVers: 
            #OPEN VERSION FILE / PRINT
            with open(PATH_BASE + '\\_version.txt', 'r') as _vers : print _vers.read()

        #HELP 
        if arg.lower() in lHelp: 
            #OPEN HELP FILE / PRINT            
            with open(PATH_BASE + '\\_help.txt', 'r') as _help : print _help.read()

    #EXIT PROGRAM
    sys.exit()


#-------------------------------------------------------------------------
#FUNCTION FOR DECODING UNICODE AND RETURNING AS STRING
def Unidecode(string):

    '''
    DESIGN:
    Method designed test a passed string for being a unicode type, then decode
    using the unidecode package, and return a string value.
    
    If the passed string is not unicode, the original value is returned.
        
    USE:
    > from utils.utils import Unidecode as uni
    >
    > string = uni(unistring)
    '''
    
    from unidecode import unidecode
    
    #INITIALISE VARIABLE
    decoded = None    
    
    #TEST PASSED VALUE AS BEING UNICODE > STORE DECODED (OR ORIGINAL) VALUE
    decoded = unidecode(string) if isinstance(string, unicode) else string

    #RETURN VALUE        
    return decoded        