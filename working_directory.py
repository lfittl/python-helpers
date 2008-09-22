#!/usr/bin/env python2.5
# vim: encoding=utf-8:ft=python:et:sw=4:ts=8:sts=4:
#
# Released under the Public Domain.
#
# Author: Lukas Fittl <lukas@fittl.com>

import os

class working_directory(object):
    def __init__(self, new_cwd):
        self.new_cwd = new_cwd
    
    def __enter__(self):
        self.old_cwd = os.getcwd()
        
        os.chdir(self.new_cwd)
    
    def __exit__(self, type, value, traceback):
        os.chdir(self.old_cwd)