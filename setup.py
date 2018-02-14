'''------------------------------------------------------------------------------------------------
Program:    setup.py
Py Ver:     2.7
Purpose:    Setup packager for utils.

Dependents: distutils
            setuptools

Comments:

            Installation:
            > cd /path/to/package_x.x.x
            > pip install . --no-deps

---------------------------------------------------------------------------------------------------
UPDATE LOG:
Date        Programmer      Version     Update
22.03.17    J. Berendt      0.0.1       Written
09.10.17    J. Berendt      0.0.2       Utils version 4.5.0 included moving the README files to
                                        the root directory, for GitHub use.
                                        Updated this setup file to use the new README location.
                                        Added mysql-connector==2.1.4 to the required packages.
10.10.17    J. Berendt      0.0.3       Added colorama to the required packages, in support of the
                                        user_interface module.
11.10.17    J. Berendt      0.0.4       BUG01: The user_interface_config.json config file cannot be
                                        found on utils.registry import.
                                        FIX01: Added user_interface_config.json to data_files.
11.10.17    J. Berendt      0.1.0       Overhaul of this setup file IAW:
                                        https://setuptools.readthedocs.io/en/latest/setuptools.html
                                        This file now makes use of the package_data parameter.
17.10.17    J. Berendt      0.1.1       Removed unneeded / commented code.
                                        Minor formatting updates.
                                        Removed sys and os imports.
                                        Removed use of data_files; replaced with MANIFEST.in.
                                        pylint (10/10)
19.10.17    J. Berendt      0.2.0       Updated to use utils.get_datafiles() function for data
                                        file collection.
                                        Updated to re-include README and LICENCE files in install.
20.12.17    J. Berendt      0.2.1       Updated to use new get_datafile() function, which pulls
                                        README and LICENSE files properly.
14.02.18    J. Berendt      0.2.2       Removed the x.x.x version place holder from the URL entry.
------------------------------------------------------------------------------------------------'''

import os
from setuptools import setup, find_packages
from utils.utils import getsitepackages
from utils.get_datafiles import get_datafiles
from utils._version import __version__


#SETUP CONSTANTS
PACKAGE         = 'utils'
VERSION         = __version__
PLATFORMS       = 'Python 2.7'
DESC            = 'Bespoke general utilities package for Python 2.7.'
AUTHOR          = 'J. Berendt'
AUTHOR_EMAIL    = 'support@73rdstreetdevelopment.co.uk'
URL             = 'https://github.com/s3dev/utils'
LICENSE         = 'MIT'
PACKAGE_ROOT    = os.path.join(os.path.realpath(os.path.dirname(__file__)), PACKAGE)
SITE_PKGS       = os.path.join(getsitepackages(), PACKAGE)

#PACKAGE REQUIREMENTS
REQUIRES        = ['numpy', 'cx_Oracle', 'unidecode', 'matplotlib', 'pyodbc', 'plotly',
                   'mysql-connector==2.1.4', 'colorama']

#ADD DATA FILES
DATA_FILES      = get_datafiles(pkg_dir=PACKAGE_ROOT)

#DEFINE PARAMETERS (LIST PROGRAM DEPENDENCIES IN INSTALL_REQUIRES PARAMETER)
PARAMS = dict(name=PACKAGE,
              version=VERSION,
              platforms=PLATFORMS,
              description=DESC,
              author=AUTHOR,
              author_email=AUTHOR_EMAIL,
              url=URL,
              license=LICENSE,
              packages=find_packages(),
              install_requires=REQUIRES,
              data_files=DATA_FILES)

#SETUP PARAMETERS
setup(name=PARAMS['name'],
      version=PARAMS['version'],
      platforms=PARAMS['platforms'],
      description=PARAMS['description'],
      author=PARAMS['author'],
      author_email=PARAMS['author_email'],
      maintainer=PARAMS['author'],
      maintainer_email=PARAMS['author_email'],
      url=PARAMS['url'],
      license=PARAMS['license'],
      packages=PARAMS['packages'],
      install_requires=PARAMS['install_requires'],
      data_files=PARAMS['data_files'])
