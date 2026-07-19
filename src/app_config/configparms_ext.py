#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  configparms_ext.py
#     read the config file and load the
#     variables in the config.py module
#
#  Copyright 2023 cswaim <cswaim@jcrl.net>
#  Licensed under the Apache License, Version 2.0
#  http://www.apache.org/licenses/LICENSE-2.0

from pathlib import Path
import os
from app_config.configparms import ConfigParms

# ----------------------------------------------------------------
# NOTE:
# In the methods that return True/False, the boolean value controls
# the flow of looping thru sections/variables.
# False - follow the default flow and process the rest of the logic
#         for the loop
# True - Force the next item in the loop, ie a python `continue`
# ----------------------------------------------------------------

class ConfigParmsExt(ConfigParms):
    """ This class extends the ConfigParms class allowing overrides of
        base class
    """
    def __init__(self, config, autorun=False):
        """ on init, load the directory paths,
            if autorun read the cfg file
        """
        super().__init__(config, autorun)

    def set_directories(self,) -> None:
        """ set the working directory paths in cfg
            modify the directory of the .cfg file if not data

            The default code is provided
        """
        # location of .cfg
        _datadir = self.find_dir_path("data", __file__)
        self.cfg.datadir = str(Path(_datadir).resolve()) + os.sep

        self.cfg.wkdir_path = Path(__file__).parent.parent

        self.cfg.srcdir = str(Path(__file__).resolve().parent) + os.sep
        self.cfg.wkdir = str(self.cfg.wkdir_path) + os.sep

        self.cfg.root_path = self.find_file_path("pyproject.toml", __file__)

    def custom_init_routine(self,) -> None:
        """ Run any custom process need during init of the class.
            This is rarely used. """
        pass

    # set custom default values in the config object before writing the config file

    def set_custom_default_sects(self, config, sec, vars) -> bool:
        """ Process any section that needs special handling,
            such as a dictionary that is converted into variables
            within a section in the config file
        """
        #  set to True to skip the rest of the loop
        next_iter = False
        return next_iter

    def set_custom_default_vars(self, config, sec, vars, var) -> bool:
        """ Process any variable that needs special handling """
        #  set to True to skip the rest of the loop
        next_iter = False
        return next_iter

    # verify the values defined in the config module exist
    # in the config parser object or
    # if in the config object, they are loaded to the cfg module

    def verify_config_sects(self, config, sec, vars) -> bool:
        """ verify sect in the cfg module are same as config obj
            if sect missing in config add it
            if sect exists in config, load values to cfg module
        """
        #  set to True to skip the rest of the loop
        next_iter = False
        return next_iter

    def verify_config_vars(self, config, sec, vars, var) -> bool:
        """ verify vars in the cfg module are same as config obj
            if var missing in config add it
            if var exists in config, load values to cfg module
        """
        #  set to True to skip the rest of the loop
        next_iter = False
        return next_iter

    # set the values in the cfg module

    def set_module_sects(self, config, sec, vars) -> bool:
        """ special processing for module sects
            for example: create a dict from a section
        """
        #  set to True to skip the rest of the loop
        next_iter = False
        return next_iter

    def set_module_vars(self, config, sec, vars, var) -> bool:
        """ special processing or editing for module variables
            for example:
                filter a text string to have a specific format
        """
        #  set to True to skip the rest of the loop
        next_iter = False
        return next_iter

    def set_custom_module_vars(self, config) -> None:
        """ set any custiom vars that are not being defined in the config.py module
            These generally are values that are derived from
            values received from the config file

            For example:
                build a list based on the number of items, as set
                in a config file varible
        """
        pass
