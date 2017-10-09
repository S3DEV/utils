
# utils_4.5.1
---
The **utils** package is a centralised location for commonly used utilities; such as database connections, colourmaps, JSON (config file) loading, program event logging, error reporting, etc.

Change log information is included in each module's header.


## PACKAGE CONFIGURATION
---
As of program version 4, a number of other standalone modules have been added to the utils package.  Outlined below is the current package configuration.

- utils
   + config
      + loadconfig()
   + log
      + **Log**
         + write()
         + write_blank_line()
   + progressbar
       + **ProgressBar**
          + update_progress()
   + reporterror
      + reporterror()
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
> sudo pip install git+https://github.com/s3dev/utils_4.x.x/
```

- **Local / Remote Git Repo**
```bash
> sudo pip install git+file:///<repo/location>/utils
```

- **Python Setup File**
```bash
> sudo python <path>/utils/setup.py install
```


### WINDOWS INSTALLATION
Any of the following options will get you there ...

- **GitHub**
```bash
> pip install git+https://github.com/s3dev/utils_4.x.x/
```

- **Local / Remote Git Repo**
```bash
> pip install git+file:///<repo/location>/utils
```

- **Python Setup File**
```bash
> python <path>/utils/setup.py install
```


### UPGRADING A CURRENT INSTALLATION
To upgrade a current installation to the latest version, use an install command as listed above, and append the `--upgrade` argument to the command.  
For example:

```bash
> sudo pip install git+https://github.com/s3dev/utils_4.x.x/ --upgrade
```


## PACKAGE HELP
---
```python
> import utils.utils as utils
> help(utils)
```  
```python
> import utils.config as config
> help(config)
```  
```python
> import utils.log as log
> help(log)
```  
```python
> import utils.progressbar as progressbar
> help(progressbar.ProgressBar)
```  
```python
> import utils.reporterror as reporterror
> help(reporterror)
```  


## TROUBLESHOOTING
---
If the Linux (or Windows) installation is giving you trouble with **cx_Oracle**, use the `--no-deps` argument for **pip**.  This argument will ignore the dependencies, and allow you to install each dependency yourself, *if* you require it.  

```bash
> sudo pip install git+https://github.com/s3dev/utils_4.x.x/ --no-deps
```