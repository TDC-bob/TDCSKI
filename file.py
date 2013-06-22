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
        if must_exist and not self.exists:
            raise FileDoesNotExist(self)

    @property
    def exists(self):
        return os.path.exists(self.path)

    def remove(self):
        os.remove(self.path)
        if self.exists:
            raise FileRemoveError(self)

    def copy(self, dest, overwrite=False):
        if os.path.exists(dest) and not overwrite:
            raise FileCopyError(self, dest, "la destination existe déjà")


def main():
    test = File("caribou")
    return 0

if __name__ == '__main__':
    main()
