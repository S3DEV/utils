
# utils_3.0.1
---
The **utils** package is a centralised location for commonly used utilities; such as database connections, colourmaps, JSON (config file) reading, etc.


### LINUX INSTALLATION
---
Any of the following options will get you there ...

- **GitHub**
```bash
> sudo pip install git+https://github.com/s3dev/utils_3.x.x/
```

- **Local / Remote Git Repo**
```bash
> sudo pip install git+file://<repo/location>/utils_3.x.x/
```

- **Python Setup File**
```bash
> sudo python <path>/utils/setup.py install
```


### WINDOWS INSTALLATION
---
Any of the following options will get you there ...

- **GitHub**
```bash
> pip install git+https://github.com/s3dev/utils_3.x.x/
```

- **Local / Remote Git Repo**
```bash
> pip install git+file://<repo/location>/utils_3.x.x/
```

- **Python Setup File**
```bash
> python <path>/utils/setup.py install
```


### UPGRADING A CURRENT INSTALLATION
---
To upgrade a current installation to the latest version, use an install command as listed above, and append the `--upgrade` argument to the command.  
For example:

```bash
> sudo pip install git+https://github.com/s3dev/utils_3.x.x/ --upgrade
```


### PACKAGE HELP
---
```python
> import utils.utils as u
> help(u)
```  


### TROUBLESHOOTING
---
If the Linux (or Windows) installation is giving you trouble with **cx_Oracle**, use the `--no-deps` argument for **pip**.  This will ignore the dependencies, and allow you to install each one yourself, *if* you require them.  

```bash
> sudo pip install git+https://github.com/s3dev/utils_3.x.x/ --no-deps
```
