#!/usr/bin/env python2.5
# vim: encoding=utf-8:ft=python:et:sw=4:ts=8:sts=4:
#
# Released under the Public Domain.
#
# Author: Lukas Fittl <lukas@fittl.com>

import os
import os.path

def chown_recursive(path, user, group):
    for root, dirs, files in os.walk(path, topdown=False):
        for name in files + dirs:
            os.chown(os.path.join(root, name), user, group)