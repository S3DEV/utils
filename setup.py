'''------------------------------------------------------------------------------------------------
Program:    setup.py
Version:    0.0.4
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
-------------------------------------------------------------------------------------------------'''

import sys
import os
from setuptools import setup, find_packages

#GET THE VERSION FILE
exec(open('utils/_version.py').read())

#SETUP CONSTANTS
PACKAGE = 'utils'
#GET SYS.PREFIX PATH >> MODIFY TO INCLUDE PACKAGE DIR (FOR DATA_FILES)
INST_RAW = 'c:/anaconda2/lib/site-packages/' + PACKAGE
PREFIX = os.path.realpath(sys.prefix).lower()
INST_ROOT = os.path.realpath(INST_RAW).lower().replace(PREFIX, '.')

#DEFINE PARAMETERS (LIST PROGRAM DEPENDENCIES IN INSTALL_REQUIRES PARAMETER)
params = dict(prog=PACKAGE,
              version=__version__,
              platforms='Python 2.7',
              description='Bespoke general utilities package for Python 2.7',
              name='J. Berendt',
              email='support@73rdstreetdevelopment.co.uk',
              url='https://73rdstreetdevelopment.wordpress.com',
              license='MIT',
              packages=find_packages(),
              install_requires=['numpy', 'cx_Oracle', 'unidecode', 'matplotlib', 'pyodbc', 'plotly',
                                'mysql-connector==2.1.4', 'colorama'],
              data_files=[(INST_ROOT, ['README.html', 'README.md', 'LICENSE', './utils/user_interface_config.json'])]
              )

#SETUP PARAMETERS
setup(name=params['prog'],
      version=params['version'],
      platforms=params['platforms'],
      description=params['description'],
      author=params['name'],
      author_email=params['email'],
      maintainer=params['name'],
      maintainer_email=params['email'],
      url=params['url'],
      license=params['license'],
      packages=params['packages'],
      install_requires=params['install_requires'],
      data_files=params['data_files']
      )
