#!/usr/bin/env python
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

from lib.configobj import ConfigObj
from tdcski._logging import mkLogger, logged, DEBUG
import os
from tdcski.file import File
logger = mkLogger(__name__, DEBUG)

git_exe = None
DCS_path = None
SaveGames_path = None
update = False
update_list_only = False

server_interface = "127.0.0.1"
server_port = "10307"

class ConfigFileDoesNotExist(Exception):
    def __init__(self, path_to_file):
        logger.error("le fichier n'existe pas ({})".format(path_to_file))

class Config():
    def __init__(self, file='../tdcski.cfg', must_exists=True):
        if must_exists and not os.path.exists(file):
            raise ConfigFileDoesNotExist(file)
            #~ logger.error("impossible de trouver le fichier de configuration sur le chemin suivant: {}".format(os.path.abspath(file)))
            #~ input()
            #~ exit(1)
        self.__file = File(file, must_exists)
        self.__config = ConfigObj(infile=self.__file.path)

    @property
    def file(self):
        return self.__file

    def reload(self):
        self.__config.reload()

    def get(self, *args):
        if not args:
            return ''
        base = self.__config
        try:
            while len(args) > 1:
                base = base[args[0]]
                args = args [1:]
            if base[args[0]] in ["True","true","oui","yes", "o", "y"]:
                return True
            if base[args[0]] in ["False","false","non","no", "n"]:
                return False
            return base[args[0]]
        except KeyError:
            return None

    def set_or_create(self, *args):
        if not self.set(*args):
            if not self.create(*args):
                return None
        return True

    def create(self, *args):
        if self.get(*args[0:-1]):
            return None
        base = self.__config
        while len(args) > 2:
            try:
                base[args[0]]
            except KeyError:
                base[args[0]] = {}
            base = base[args[0]]
            args = args[1:]
        if type(args[1]) == bool:
            if args[1]:
                base[args[0]] = "True"
            else:
                base[args[0]] = "False"
        else:
            base[args[0]] = args[1]
        self.__config.write()
        return True

    def set(self, *args):
        if self.get(*args[0:-1]) == None:
            return None
        base = self.__config
        while len(args) > 2:
            base = base[args[0]]
            args = args[1:]
        if type(args[1]) == bool:
            if args[1]:
                base[args[0]] = "True"
            else:
                base[args[0]] = "False"
        else:
            base[args[0]] = args[1]
        self.__config.write()
        return True

