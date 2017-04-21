'''------------------------------------------------------------------------------------------------
Program:    regtest.py
Version:    0.0.1
Py Ver:     2.7
Purpose:    This is a regression testing program for utils; to ensure backwards compatability
            for each upgrade.

Dependents: _version
            utils
            pandas

Developer:  J. Berendt
Email:      support@73rdstreetdevelopment.co.uk

Comments:   This program is intended for internal testing only and should not be added to
            setup.py for distribution / installation.

Use:        > python regtest.py

---------------------------------------------------------------------------------------------------
UPDATE LOG:
Date        Programmer      Version     Update
04.04.17    J. Berendt      0.0.1       Written
------------------------------------------------------------------------------------------------'''

from _version import __version__
import utils.utils as u
import pandas as pd


#------------------------------------------------------------------------------
def setup():

    global itested
    global ipassed
    global ifailed

    itested = 0
    ipassed = 0
    ifailed = 0


#------------------------------------------------------------------------------
def results():

    print ''
    print '-'*50
    print 'RESULTS'
    print '-'*50
    print 'Number tested: %s' % itested
    print 'Number passed: %s' % ipassed
    print 'Number failed: %s' % ifailed
    print '-'*50


#------------------------------------------------------------------------------
def gen(method, name):

    global itested
    global ipassed
    global ifailed

    itested += 1

    try:
        print '-'*50
        print 'TEST: %s' % name
        print 'RESULT: PASS\n'
        ipassed += 1
    except Exception as err:
        print 'RESULT: FAIL'
        print 'ERR: %s\n' % err
        ifailed += 1


#-------------------------------------------------------------------------------
#MAIN PROGRAM CONTROLLER
def main():

    '''
    METHODS TESTED:
    ------------------
    ArgvParse
    CleanDF
    DirExists
    FileExists
    GetColourMap
    GetConfig
    GetDriverName
    Unidecode
    clean_df
    colours_addRGB
    colours_addRGBA
    x- dbConn_Oracle  #DB CONN(S) REMOVED DUE TO DB CONN COMPLICATIONS
    x- dbConn_SQL
    x- dbconn_oracle
    x- dbconn_sql
    direxists
    fileexists
    format_exifDate
    format_exif_date
    getcolormap
    getdrivername
    jsonRead
    jsonWrite
    json_read
    json_write
    testimport
    unidecode
    ------------------
    '''

    setup()

    gen(u.ArgvParse(), u.ArgvParse.func_name)
    gen(u.CleanDF(pd.DataFrame()), u.CleanDF.func_name)
    gen(u.clean_df(pd.DataFrame()), u.clean_df.func_name)
    gen(u.colours_addRGB(), u.colours_addRGB.func_name)
    gen(u.colours_addRGBA(), u.colours_addRGBA.func_name)
#    gen(u.dbConn_Oracle('x', 'x', 'x'), u.dbConn_Oracle.finc_name)
#    gen(u.dbconn_oracle('x', 'x', 'x'), u.dbConn_oracle.func_name)
#    gen(u.dbConn_SQL('x', 'x', 'x', 'x'), u.dbConn_SQL.func_name)
#    gen(u.dbConn_sql('x', 'x', 'x', 'x'), u.dbConn_sql.func_name)
    gen(u.DirExists('c:/temp'), u.DirExists.func_name)
    gen(u.direxists('c:/temp'), u.direxists.func_name)
    gen(u.FileExists('c:/temp'), u.FileExists.func_name)
    gen(u.fileexists('c:/temp'), u.fileexists.func_name)
    gen(u.format_exif_date('2017:04:05 23:22:21'), u.format_exif_date.func_name)
    gen(u.format_exifDate('2017:04:05 23:22:21'), u.format_exifDate.func_name)
    gen(u.GetColourMap(), u.GetColourMap.func_name)
    gen(u.getcolormap(), u.getcolormap.func_name)
    gen(u.GetConfig(), u.GetConfig.func_name)
    gen(u.GetDriverName('Ora'), u.GetDriverName.func_name)
    gen(u.getdrivername('Ora'), u.getdrivername.func_name)
    gen(u.json_read('c:/temp/test.json'), u.json_read.func_name)
    gen(u.json_write({'a':'b'}, 'c:/temp/test.json'), u.json_write.func_name)
    gen(u.jsonRead('c:/temp/test.json'), u.jsonRead.func_name)
    gen(u.jsonWrite({'a':'b'}, 'c:/temp/test.json'), u.jsonWrite.func_name)
    gen(u.testimport('pyodbc'), u.testimport.func_name)
    gen(u.Unidecode('some text'), u.Unidecode.func_name)
    gen(u.unidecode('some text'), u.unidecode.func_name)

    results()


#------------------------------------------------------------------------------
#RUN PROGRAM
if __name__ == '__main__': main()

