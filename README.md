
# utils_5.2.0
---
The **utils** package is a centralised location for commonly used utilities; such as database connections, colourmaps, JSON (config file) loading, program event logging, error reporting, etc.

Change log information is included in each module's header.


## PACKAGE CONFIGURATION
---
With package version 5, the **depreciated methods and functions from version 4, have been deleted**.  Version 5 includes the addition of Windows registry access (via the `_winreg` package), enabling easy manipulation querying of the registry and environment variables.

As of program version 4, a number of other standalone modules have been added to the utils package.  Outlined below is the current package configuration.

- utils
   + config
      + loadconfig()
   + log
      + **Log()**
         + write()
         + write_blank_line()
   + progressbar
       + **ProgressBar()**
          + update_progress()
   + registry
      + **Registry()**
         + various registry access methods and functions
   + reporterror
      + reporterror()
   + user_interface()
      + **UserInterface()**
         + various console and error printing methods
   + utils
      + clean_df()
      + dbconn_oracle()
      + dbconn_sql()
      + dbconn_sqlite()
      + dbconn_mysql()
      + direxists()
      + fileexists()
      + format_exif_date()
      + getcolormap
      + getdrivername()
      + json_read()
      + json_write()
      + rgb2hex()
      + testimport()
      + unidecode()


## INSTALLATION
---
### LINUX
Any of the following options will get you there ...

- **GitHub**
```bash
sudo pip install git+https://github.com/s3dev/utils_x.x.x/
```

- **Local / Remote Git Repo**
```bash
sudo pip install git+file:///<repo/location>/utils
```

- **Local Install**
```bash
cd <utils_project_directory>
sudo pip install .
```


### WINDOWS INSTALLATION
Any of the following options will get you there ...

- **GitHub**
```bash
pip install git+https://github.com/s3dev/utils_x.x.x/
```

- **Local / Remote Git Repo**
```bash
pip install git+file:///<repo/location>/utils
```

- **Local Install**
```bash
cd <utils_project_directory>
pip install .
```


### UPGRADING A CURRENT INSTALLATION
To upgrade a current installation to the latest version, use an install command as listed above, and append the `--upgrade` argument to the command.  
For example:

```bash
sudo pip install git+https://github.com/s3dev/utils_x.x.x/ --upgrade
```


## PACKAGE HELP
---
```python
import utils.utils as utils
help(utils)
```  
```python
import utils.config as config
help(config)
```  
```python
import utils.log as log
help(log)
```  
```python
import utils.progressbar as progressbar
help(progressbar.ProgressBar)
```  
```python
import utils.reporterror as reporterror
help(reporterror)
```  


## TROUBLESHOOTING
---
If the Linux (or Windows) installation is giving you trouble with **cx_Oracle**, use the `--no-deps` argument for **pip**.  This argument will ignore the dependencies, and allow you to install each dependency yourself, *if* you require it.  

```bash
sudo pip install git+https://github.com/s3dev/utils_x.x.x/ --no-deps
```
