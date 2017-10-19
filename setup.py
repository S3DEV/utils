'''------------------------------------------------------------------------------------------------
Program:    setup.py
Version:    0.1.1
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
-------------------------------------------------------------------------------------------------'''

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

#PACKAGE REQUIREMENTS
REQUIRES        = ['numpy', 'cx_Oracle', 'unidecode', 'matplotlib', 'pyodbc', 'plotly',
                   'mysql-connector==2.1.4', 'colorama']
#PACKAGE DATA FILES
PACKAGE_DATA    = {'utils':['*.json']}


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
              install_requires=REQUIRES)
            #   package_data=PACKAGE_DATA)

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
      include_package_data=True)
    #   package_data=PARAMS['package_data']
