# app_config
[![image](https://img.shields.io/pypi/v/app_config.svg)](https://python.org/pypi/app_config)
[![image](https://img.shields.io/pypi/l/app_config.svg)](https://python.org/pypi/app_config)
[![image](https://img.shields.io/pypi/pyversions/app_config.svg)](https://python.org/pypi/app_config)

[![image](https://img.shields.io/pypi/dm/app_config?style=flat-square)](https://pypistats.org/packages/app_config)
![Pipeline](https://gitlab.com/tpgllc/app_config/badges/main/pipeline.svg)
![Coverage](https://gitlab.com/tpgllc/app_config/badges/main/coverage.svg)

> **IMPORTANT**
>
> Release 3.0.0 is a breaking release.  It is not backward compatible with release 2.1.1.
>
> For legacy applications set the requirements to app_config==2.1.1
>
> See [history](#history) for more details


## Table of Contents
- [Overview](#overview)
- [Requirements](#requirements)
- [Project Structure](#project-structure)
- [Setup](#setup)
- [Implementation](#implementation)
 - <a href="https://gitlab.com/tpgllc/app_config/-/blob/main/doc/customizing.md" target="_blank">Customization</a>

## Overview

This is a utility module which reads a configuration file and builds a config namespace module which can be passed throughout an application.  If the configuration file does not exist, a file is created with default values from the config module.  The values in the confiuration module are updated from the variables in the config file.  The config module can be imported into each python application program which permits the passing of varibles between programs. Reading and writing of the config file is based upon the standard library configparser module.

  The variables can be references as `cfg.varname` as shown in the example below.

myapp.py

```
    from src import config as cfg

    print(cfg.var1)

    # list variables updated from config file
    for s, v in cfg.cfg_values.items():
        print(f"{s}: {v}")
        for var in v:
            print(f"   {var[0]}: {getattr(cfg, var[0])}")

    print(f"version: {cfg.sys_cfg_version}")
```

### Features

* Allow values to be changed in a config file and passed into the system - no changing of source code
* Manage the config file, reading parameters into the application, creating the initial file with defaults, updating existing config file if parameters are added or names change in the config module.  Pre-defined comments and config file values are preserved.
* Creates a config module that can be used to pass paramters to other modules.  The values in this module are updated from the values in the config file and can be modified by the application.
* Internal variables/objects can be added to the config module and passed to each module in application.

## Requirements

This module requires python 3.10 due to use of case statement.

Standard Python packages are utilized and no special packages are needed.

## Project structure

The package has been tested with three structures: root, nested, src (nomenclature will vary)

### Root Structure
```
proj_name/
    data/
    src/
        __init__.py
        config.py
        configparms_ext.py
    tests/
    proj_main.py
```

### Nested Structure
```
proj_name/
    data/
    scripts/ (or proj_name, codes)
        src/
            __init__.py
            config.py
            configparms_ext.py
        proj_main.py
    tests/
```

### SRC Structure
```
proj_name/
    data/
    src/
        proj_name/
            src/
                __init__.py
                config.py
                configparms_ext.py
            proj_main.py
    tests/
```

If you have a different project structure, then the configparms_ext.py method ```set_directrories``` can be modified to set the path to the data folder and src folder of your project.

## Setup

> all examples assume a root structure
>
> the config file is in a data directory

The configparms_ext.py method set_directories assumes a 'data' directory is where the config file will be stored.  This can be changed by modifying the code that sets self.cfg.datadir.

From a terminal window:

1. Install the package in your environment:

    ```
    pip install app_config

    or

    uv pip install app_config
    ```

1. Change directories to your src folder:

    ```cd src```

1. Copy the config file into the src directory.

    - create an empty `__init__.py` file in the source directory with your favorite editor

    - enter the following command:

        ```app_config-init```

    This command copies two file into the current directory: config.py and configparms_ext.py

    Rerunning ```app_config-init``` will not overwrite existing files, but will receate a file if it is missing.

1. Modify the config file to meet your application needs. Be sure to change the value of the variable *cfg_flnm* to the name of your config file.

1. In each module, add the import for the config.  This should be the first application import, after the standard python module imports,
    ```
    import os
    import sys
    from src import config as cfg
    from src import my_other_application_modules
    ```
1. In ```config.py``` set the autorun flag or call the run method `cfg.run()` in your application.  See the comments at the bottom of the config file.

1. The first time you run a program with the config import, it will look for a config file in the data directory and if does not exist, it will create one.  If a config file is found, the values from the config file will update the values in the config module

All set!

### Verify your paths

the following code will print the paths and any variables managed by the config file.

```
from pathlib import Path
import os

from src import config as cfg

if __name__ == '__main__':
    # get the config parameters
    cfg.run()
    cfg.cu.print_config_vars()
```


## Implementation

In each of your application programs, the ```src.config``` module should be imported as the first application import in each application module.

*`import src.config as cfg`*

The first import reads the config file (`data/xxxxx.cfg`) and loads the runtime values.  If the cfg file, as named in the variable *cfg.cfg_flnm*, does not exist, it is created with the default values.

The config module creates a module as a namespace so variables can be referenced as cfg.var.  Each variable is defined with its default value in the namespace, unless overridden by the config file.  A config file, *`xxxxx.cfg`* is created on the first import of config if it does not exist, where *xxxxx* is name as set in the variable `cfg.cfg_flnm`.

Any changes to the cfg file in the data folder are local and override the defaults.

### Version (`sys_cfg_version`)

If a new variable is added in the *`src.config`* module or if the variable name changes in the config module, then the version number (`sys_cfg_version`) should be updated in the config module (not the config file).  When the cfg module version and the config file version differ, a rewrite the local cfg file will be triggered with the new changes, perserving any values previously set in the file.

### Modifying for your application

Two programs from this package are provided for use by your application:
* scr/config.py
* src/configparms_ext.py   (for customization)

#### config.py

Two classes of variables are in the config.py module: variables that are updated from the xxx.cfg file and those that are defined in the config.py module and set by the application.

It is intended for the *`config.py`* file to be modified for the application.  Parameters modified by the xxx.cfg file are defined with their defaults and added to the cfg_values dictionary (see Variables below).  Replace the *var1-3* and *m1-2* variables with the variables needed by the application.  Also set the cfg filename (*cfg_flnm*).

The *`sys_cfg_version`* variable must not be deleted, it will be updated as new parameters are added to the config file and the change in this value triggers the rewrite of the file.

##### Variables

The *`cfg_values`* is a dictionary that defines the sections and variables to be written to the config file.  The key to the dictionary is the section and the value is a list of lists with variable name and variable type (see sample in config.py).

Be sure all variables to be in the config file are defined in the *`cfg_values`* dictionary.

Valid types supported are
- integer
- float
- boolean
- string
- list

##### Comments

**As of Python 3.14, comments cannot contain delimters = or :. These are seperators for key/value pairs and will throw an error when writing out the comment. **

The variable *`cfg_comments`* contains any comment to be written to the config file to explain a variable or section.

Section comments are written after the section label and variable comments are written before the variable in the config file.

The *`cfg_comments`* variable is a dictionary and the key is the variable or section name and the value is a list with each item in the list being written as a seperate comment line.

#### configparms_ext.py

To override setting of path variables or to provide special processing logic, the *`configparm_ext.py`* module is provided.

##### Set path variables

Modify the method *`set_directories`* to support the structure of your project.

##### Special processing

Sometimes, special processing is needed to covert a section to dictionary in the config module, or special handling of a variable is needed.  This can be accomplished by modifying the `configparms_ext.py` module.  See the <a href="https://gitlab.com/tpgllc/app_config/-/blob/main/doc/customizing.md" target="_blank">customization documentation</a> to modify standard processing.

### Summary of set up
* Install the package
* Run app_config-init to extract the config.py and configparms_ext.py and place in your project src directory
* Modify these modules for your application (set the config file name and set the variables)
* import the module into your application

## History

This package began as a module to read a config file and to pass run-time variables to the application.  This simple module was handy as it allowed variables to be passed into the application without code changes and it was used in several applications.

The original applications were simple and utilized a root structure.  Eventually, this simple module was converted to a package and then the restrictions of the design became clear.

Release 3.0.0 adds the ability to use the package with different project layouts, but at the cost of not being backward compatibile.

### Known Compatibility issues with 3.0.0

- In the config.py module:
  - the run_init method has changed

- In configparms_ext.py:
  - the config module is passed with dependency injection
  - all refereces to cfg.xxx are changed to self.cfg.xxx
  - the __init__ method has changed
  - the set_directories method has changed

Depending on the amount of customization in configparms_ext, the migration can be easy or involved.
