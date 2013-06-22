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

import os
from _logging._logging import mkLogger, logged, DEBUG
import shutil
from hashlib import md5 as MD5

logger = mkLogger(__name__)

class FileException(Exception):
    def __init__(self, msg):
        logger.error(msg)
        super(FileException, self).__init__(msg)

class FileDoesNotExist(FileException):
    def __init__(self, file):
        msg = "le fichier suivant n'existe pas: {}".format(file.path)
        super(FileDoesNotExist, self).__init__(msg)

class FileRemoveError(FileException):
    def __init__(self, file):
        msg = "erreur pendant la suppression du fichier: {}".format(file.path)
        super(FileRemoveError, self).__init__(msg)

class FileCopyError(FileException):
    def __init__(self, file, dest, msg):
        msg = "erreur pendant la copie de {} -> {}\n{}".format(file.path, dest, msg)
        super(FileCopyError, self).__init__(msg)

class File():
    def __init__(self, path, must_exist=True):
        self.path = path
        self.__md5 = None
        if must_exist and not self.exists:
            raise FileDoesNotExist(self)

    @property
    def exists(self):
        return os.path.exists(self.path)

    @property
    def md5(self):
        if not self.__md5:
            self.__md5 = self.__hash(self.path)
        return self.__md5

    @staticmethod
    def __hash(path):
        hasher = MD5()
        with open(path,'rb') as f:
            for chunk in iter(lambda: f.read(128), b''):
                 hasher.update(chunk)
        return hasher.digest()

    def remove(self):
        os.remove(self.path)
        if self.exists:
            raise FileRemoveError(self)

    def copy(self, dest, overwrite=False):
        logger.debug("copie: {} -> {}".format(self.path, dest))
        if os.path.exists(dest) and not overwrite:
            raise FileCopyError(self, dest, "la destination existe déjà")
        shutil.copy2(self.path, dest)
        if not os.path.exists(dest):
            raise FileCopyError(self, dest,
             "il y a eu une erreur pendant la copie, la destination n'existe pas")
        return File(dest)

    def compare(self, other, force_reload=False):
        if type(other) == str:
            other = File(other)
        logger.debug("comparaison: {} <-> {}".format(self.path, other.path))
        if force_reload:
            logger.debug("calcul forcé des hash md5")
            self.__md5 = self.__hash(self.path)
            other.__md5 = self.__hash(other.path)
        result = self.md5 == other.md5
        logger.debug("résultat de la comparaison: {}".format(result))
        return result

    def backup(self, prefix="", suffix=".tdcski"):
        logger.debug("back up du fichier: {}".format(self.path))
        dest = "{}{}{}".format(
                    prefix,
                    os.path.abspath(self.path),
                    suffix)
        logger.debug("chemin du backup: {}".format(dest))
        if os.path.exists(dest):
            logger.debug("le backup existe déjà")
        else:
            self.copy(dest)
        return File(dest)

