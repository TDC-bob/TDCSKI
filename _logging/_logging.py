﻿#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Copyright 2013 Bob <TDC-bob@daribouca.net>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#
__version__ = (0, 0, 1)
__author__ = 'bob'

import logging
from os.path import exists
from os import remove
##from msgbox import MsgBox
##from PyQt4 import QtGui
DEBUG = logging.DEBUG
WARNING = logging.WARNING
INFO = logging.INFO
ERROR = logging.ERROR
WARN = WARNING
ERR = ERROR

#~ @decorator
def logged(f):
    """
    Decorator for the __init__ function of a class

    Adds a logger to an instance of that class, named:
    main.module.class.function
    """
    def wrapper(instance, *args, **kw):
        instance.logger = logging.getLogger(".".join(["main", instance.__module__, instance.__class__.__name__, f.__name__]))
        return f(instance, *args, **kw)
    return wrapper


def mkLogger(moduleName, lvl=logging.DEBUG, logFile="python.log"):
    """
    Creates a module-specific logger
    """
    if moduleName == "__main__":
        return __setupLogger("main", lvl, logFile)
    else:
        subLoggerName = ".".join(["main", moduleName])
    return logging.getLogger(subLoggerName)


def __setupLogger(name="main", lvl=logging.DEBUG, logFile="python.log"):
    try:
        if exists(logFile):
            remove(logFile)
    except WindowsError:
        import sys
##        app = QtGui.QApplication(sys.argv)
##        error = MsgBox("Impossible de lancer le TDCMEME !\n\nSoit le TDCMEME est dÃ©jÃ  en cours d'exÃ©cution, ou alors il n'a pas accÃ¨s Ã  son propre rÃ©pertoire.\n\nCela peut arriver si vous l'avez installÃ© dans un rÃ©pertoire dans lequel il n'est pas\
##possible d'Ã©crire sans avoir les droits d'aministrateur (\"Program Files\", rÃ©pertoire Windows, etc...)")
##        error.show()
##        sys.exit(app.exec_())
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler(logFile)
    fh.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    logfileFormatter = logging.Formatter('%(asctime)s: %(levelname)s - %(name)s - %(message)s')
    consoleFormatter = logging.Formatter('%(levelname)s - %(name)s - %(message)s')
    fh.setFormatter(logfileFormatter)
    ch.setFormatter(consoleFormatter)
    logger.addHandler(fh)
    logger.addHandler(ch)
    return logger
