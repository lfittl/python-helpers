#!/usr/bin/env python2.5
# vim: encoding=utf-8:ft=python:et:sw=4:ts=8:sts=4:
#
# Released under the Public Domain.
#
# Author: Lukas Fittl <lukas@fittl.com>

from __future__ import with_statement

import atexit
import os
import pwd
import sys
import traceback
import logging

from signal import signal, SIGTERM, SIGINT

# File mode creation mask of the daemon.
UMASK = 0

# Default working directory for the daemon.
WORKDIR = "/"

# Default maximum for the number of available file descriptors.
MAXFD = 1024

# The standard I/O file descriptors are redirected to /dev/null by default.
if hasattr(os, "devnull"):
    REDIRECT_TO = os.devnull
else:
    REDIRECT_TO = "/dev/null"

log = logging.getLogger('lib.daemon')

def remove_pidfile(pidfile):
    try:
        os.remove(pidfile)
    except OSError:
        log.warn('Couldn\'t remove pidfile, already removed?!')

def exit_signal(signum, frame):
    log.info('Received SIGINT/SIGTERM, exiting.')
    sys.exit(0)

def daemonize(mainfnc, pidfile):
    if os.path.exists(pidfile):
        raise Exception, "Pidfile '%s' already exists!" % pidfile

    try:
        pid = os.fork()
    except OSError, e:
        raise Exception, "%s [%d]" % (e.strerror, e.errno)

    if pid == 0: # The first child.
        os.setsid()  # New session
        try:
            pid = os.fork() # Fork a second child.
        except OSError, e:
            raise Exception, "%s [%d]" % (e.strerror, e.errno)
        if pid == 0:# The second child.
            os.chdir(WORKDIR)
            os.umask(UMASK)
        else:
            os._exit(os.EX_OK) # Exit parent (the first child) of the second child.
    else:
        os._exit(os.EX_OK) # Exit parent of the first child.

    # iterating over possibly open file descriptors (inherited from parent)
    for fd in xrange(0, 3):
        try:
            os.close(fd)
            pass
        except OSError: # ERROR, fd wasn't open to begin with (ignored)
            pass

    os.open(REDIRECT_TO, os.O_RDWR) # standard input (0)
    os.dup2(0, 1) # standard output (1)
    os.dup2(0, 2) # standard error (2)

    # Dummy Signal handler to ensure atexit functions are executed
    signal(SIGTERM, exit_signal)
    signal(SIGINT, exit_signal)

    # Pidfile creation
    atexit.register(remove_pidfile, pidfile)
    with open(pidfile, 'w') as fp:
        fp.write('%s\n' % os.getpid())

    log.debug('Entering main program')

    try:
        mainfnc()
    except Exception:
        log.error('Caught exception:\n%s' % traceback.format_exc())

    log.debug('Main program finished')