
from setuptools import setup, find_packages

#GET THE VERSION FILE
exec(open('utils/_version.py').read())

#DEFINE PARAMETERS (LIST PROGRAM DEPENDENCIES IN INSTALL_REQUIRES PARAMETER)
params = dict(  prog='utils', 
                version=__version__,
                platforms='Python 2.7', 
                description='Bespoke general utilities package for Python 2.7', 
                name='J. Berendt', 
                email='support@73rdstreetdevelopment.co.uk', 
                url='https://73rdstreetdevelopment.wordpress.com',
                license='MIT',
                packages=find_packages(),
                install_requires=['palettable', 'numpy', 'cx_Oracle', 'unidecode', 'matplotlib', 'pyodbc']
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
      install_requires=params['install_requires']
      )