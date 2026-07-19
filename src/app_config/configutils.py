#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Copyright 2024 cswaim <cswaim@tpginc.net>

class ConfigUtils():
    """ a class of utilities for the config module """

    def __init__(self, config):
        """ on init, load the directory paths, if autorun read the cfg file"""
        self.cfg = config


    # @staticmethod
    def print_config_vars(self, heading=None, comments=True, fileobj=None ):
        print("", file=fileobj)
        if heading is not None:
            print(f"--- {heading} ---", file=fileobj)

        print(f"    wkdir: {self.cfg.wkdir}", file=fileobj)
        print(f"  wk path: {self.cfg.wkdir_path}", file=fileobj)
        print(f"  src dir: {self.cfg.srcdir}", file=fileobj)
        print(f" data dir: {self.cfg.datadir}", file=fileobj)
        print(f"file name: {self.cfg.cfg_flnm}", file=fileobj)
        print("", file=fileobj)

        print(f"sections: {self.cfg.config.sections()}", file=fileobj)

        # print config variables
        for sec, vars in self.cfg.config.items():
            if comments:
                self.print_cfg_var_comments(sec, sec=True, fileobj=fileobj)
            print(self.cfg.config[sec], file=fileobj)
            for var, val in vars.items():
                if comments:
                    self.print_cfg_var_comments(var, fileobj=fileobj)
                print(f"   {var}: {val}", file=fileobj)

    # @staticmethod
    def print_cfg_var_comments(self, var, sec=False, fileobj=None):
        """look for comments for the var (sec or var)"""
        if var in self.cfg.cfg_comments.keys():
                for c in self.cfg.cfg_comments[var]:
                    if sec:
                        print(f"# {c}", file=fileobj)
                    else:
                        print(f"   # {c}", file=fileobj)
