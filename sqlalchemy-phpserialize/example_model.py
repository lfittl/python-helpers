#!/usr/bin/env python2.5
# vim: encoding=utf-8:ft=python:et:sw=4:ts=8:sts=4:
#
# Released under the GNU General Public License, version 2 or later.
#
# Author: Lukas Fittl <lukas@fittl.com>

from REPLACE_THIS_PATH import php_serialization_pickler

example_table = Table('example', metadata,
    Column('data', PickleType(pickler=php_serialization_pickler)))

class Example(object):
    pass

mapper(Example, example_table)
