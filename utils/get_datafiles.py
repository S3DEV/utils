'''------------------------------------------------------------------------------------------------
Program:    get_datafiles
Version:    0.0.2
Platform:   Windows / Linux
Py Ver:     2.7
Purpose:    This module is designed to provide a list of data files to the calling setup.py file
            in py2exe format.

Developer:  J. Berendt
            With principal code concept adopted from matplotlib.get_datafiles()
Email:      support@73rdstreetdevelopment.co.uk

Comments:

Use:        > import utils.get_datafiles as gdf
            > data_files = gdf.get_datafiles(top_dir='myprog/package', exts=['.json', '.sql'])

---------------------------------------------------------------------------------------------------
UPDATE LOG:
Date        Programmer      Version     Update
19.10.17    J. Berendt      0.0.1       Adopted and adpated.  pylint (10/10)
20.10.17    J. Berendt      0.0.2       Added the p2e (py2exe) argument and functionality.
------------------------------------------------------------------------------------------------'''

import os
import utils
from _version_gdf import __version__


#-----------------------------------------------------------------------
#FUNCTION RETURNS A PY2EXE LIST OF DATA FILES USED BY THIS PACKAGE
def get_datafiles(pkg_dir, exts=['.json', '.sql', '.txt'], p2e=False):

    '''
    PURPOSE:
    This function is designed to be called by another program's setup.py
    file and will return a list of data files used by that program, in
    py2exe's expected format.

    The concept and principal design were adopted from matplotlib's
    get_py2exe_datafiles() function.

    RESULTS FORMAT:
        return = [('destination_dir', ['/path/to/file.ext', '...'])]

    DESIGN:
    The calling program (setup.py file) will pass it's program's home
    directory and a list of desired file extensions.  The function then
    performs a directory walk and picks out the full path to each
    desired file.

    The results are returned as a list of tuples, which include the
    destination directory and the full path to each file.

    If the p2e (py2exe) flag is False, the platform's site-packages
    directory is prepended to the destination path, so the data files
    are installed to the package's site-package directory.

    PARAMETERS:
    - pkg_dir
    The root directory to begin the search.  Typically your main
    package directory.
    Tip: In your setup.py file, you can use
    os.path.join(os.path.realpath(os.path.dirname(__file__)), 'pkg') to
    get the package's directory path.
    - exts (default=['.json', '.sql', '.txt'])
    A list of file extensions used as a filter when collecting data
    files.
    - p2e (default=False)
    This flag indicates to the function whether this is a py2exe
    installation, or not.
    p2e=True means the destination path is left as derived by the
    function.
    p2e=False means the platform's site-packages directory is prepended
    to the destination path.

    USE:
    > from utils.get_datafiles import get_datafiles
    > data_files = get_datafiles(pkg_dir='myprog/package',
                                 exts=['.json', '.sql'],
                                 p2e=False)
    '''

    #ALLOW DEFAULT LIST OF EXTENSIONS
    #pylint: disable=dangerous-default-value

    #INITIALISE
    result = {}

    #GET TAIL DIRECTORY
    tail = os.path.split(pkg_dir)[1]

    #WALK DIRECTORY TREE AND GET ALL FILES
    for root, _, files in os.walk(pkg_dir):
        #BUILD LIST OF FILES MEETING THE EXTENSION CRITERIA
        files = [os.path.realpath(os.path.join(root, fname)) for fname in files
                 if os.path.splitext(fname)[1] in exts]
        #GET INDEX OF THE TAIL DIRECTORY FROM ROOT STRING
        idx = root.rfind(tail)
        #SLICE TO GET DEST DIR (AND SUB DIRS)
        root = root[idx:]
        #TEST IF PY2EXE INSTALLATION >> IF NOT, PREPEND SITE-PACKAGES DIR
        if p2e is False: root = os.path.join(utils.getsitepackages(), root)
        #TEST IF FILES TO BE ADDED >> ADD FILES TO DICT WITH DEST DIR AS THE KEY
        if len(files) > 0: result[root] = files

    #CONVERT DICT TO LIST OF TUPLES
    return list(result.items())
