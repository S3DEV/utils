'''------------------------------------------------------------------------------------------------
Program:    setup.py
Version:    0.1.0
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
-------------------------------------------------------------------------------------------------'''

import sys
import os
from setuptools import setup, find_packages
from utils._version import __version__

#SETUP CONSTANTS
PACKAGE         = 'utils'
VERSION         = __version__
PLATFORMS       = 'Python 2.7'
DESC            = 'Bespoke general utilities package for Python 2.7.'
AUTHOR          = 'J. Berendt'
AUTHOR_EMAIL    = 'support@73rdstreetdevelopment.co.uk'
URL             = 'https://github.com/s3dev/utils_x.x.x'
LICENSE         = 'MIT'

#GET SYS.PREFIX PATH >> MODIFY TO INCLUDE PACKAGE DIR (FOR DATA_FILES)
# INST_RAW    = 'c:/anaconda2/lib/site-packages/' + PACKAGE
# PREFIX      = os.path.realpath(sys.prefix).lower()
# INST_ROOT   = os.path.realpath(INST_RAW).lower().replace(PREFIX, '.')

#DEFINE PARAMETERS (LIST PROGRAM DEPENDENCIES IN INSTALL_REQUIRES PARAMETER)
params = dict(name=PACKAGE,
              version=VERSION,
              platforms=PLATFORMS,
              description=DESC,
              author=AUTHOR,
              author_email=AUTHOR_EMAIL,
              url=URL,
              license=LICENSE,
              packages=find_packages(),
              install_requires=['numpy', 'cx_Oracle', 'unidecode', 'matplotlib', 'pyodbc', 'plotly',
                                'mysql-connector==2.1.4', 'colorama'],
              package_data={'utils':['*.json']},
              data_files=[('', ['LICENSE', 'README.md', 'README.html'])])

#SETUP PARAMETERS
setup(name=params['name'],
      version=params['version'],
      platforms=params['platforms'],
      description=params['description'],
      author=params['author'],
      author_email=params['author_email'],
      maintainer=params['author'],
      maintainer_email=params['author_email'],
      url=params['url'],
      license=params['license'],
      packages=params['packages'],
      install_requires=params['install_requires'],
      package_data=params['package_data'],
      data_files=params['data_files']
      )
