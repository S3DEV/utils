
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
params = dict(  prog=PACKAGE,
                version=__version__,
                platforms='Python 2.7',
                description='Bespoke general utilities package for Python 2.7',
                name='J. Berendt',
                email='support@73rdstreetdevelopment.co.uk',
                url='https://73rdstreetdevelopment.wordpress.com',
                license='MIT',
                packages=find_packages(),
                install_requires=['numpy', 'cx_Oracle', 'unidecode', 'matplotlib', 'pyodbc', 'plotly'],
                data_files=[(INST_ROOT, ['README.html', 'README.md', 'LICENSE'])]
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