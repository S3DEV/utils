# utils_2.3.2

The **utils** package is a centralised location for commonly used utilities; such as database connections, colourmaps, JSON (config file) reading, etc.


####LINUX INSTALLATION  
`$ sudo pip install git+https://github.com/73rdStreetDev/utils_2.3.2/`  
or  
`$ sudo python <path>/utils/setup.py install`  

-----  

####WINDOWS INSTALLATION  
`> pip install git+https://github.com/73rdStreetDev/utils_2.3.2/`  
or  
`> python <path>\utils\setup.py install`  

-----  

####PACKAGE HELP
```
> import utils.utils as u
> help(u)
```  
-----  

####TROUBLESHOOTING
If the Linux installation is giving you trouble with **cx_Oracle**, use the `--no-deps` argument for **pip**.  This will ignore the dependencies, and allow you to install them yourself, if you require them.  
`$ sudo pip install git+https://github.com/73rdStreetDev/utils_2.3.2/ --no-deps`  

-----
