#!/usr/bin/env python2.5
# vim: encoding=utf-8:ft=python:et:sw=4:ts=8:sts=4:
#
# Released under the GNU General Public License, version 2 or later.
#
# Author: Lukas Fittl <lukas@fittl.com>

from REPLACE_THIS_PATH import PHPSerialize
from REPLACE_THIS_PATH import PHPUnserialize

def dumps(data, protocol=None):
    return PHPSerialize().serialize(data)

def loads(data):
    return PHPUnserialize().unserialize(data)