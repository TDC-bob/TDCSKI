##!/usr/bin/env python
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

import unittest
import os
from ..tdcski import file

from ..lib._logging._logging import mkLogger, logged, DEBUG
#logger = mkLogger(__name__, DEBUG)

class testFile(unittest.TestCase):
    file_list = ["test{}".format(x) for x in range(1, 10)]

    def setUp(self):
        for f in self.file_list:
            with open(f, mode="w") as file:
                file.write("caribou")

    def tearDown(self):
        for f in self.file_list:
            if os.path.exists(f):
                os.remove(f)
        extra_remove = ["test7_2", "test6.tdcski", "test_write"]
        for x in extra_remove:
            if os.path.exists(x):
                os.remove(x)

    def test_file_init(self):
        file.File("test1")

    def test_file_doesNotExist(self):
        with self.assertRaises(file.FileDoesNotExist):
            file.File("tchoutchou")

    def test_file_remove(self):
        f = file.File("test2")
        self.assertTrue(os.path.exists("test2"))
        f.remove()
        self.assertFalse(os.path.exists("test2"))

    def test_file_compare(self):
        f1 = file.File("test3")
        self.assertTrue(f1.compare("test4"))
        with open("test4", mode="w") as f:
            f.write("pouet")
        self.assertFalse(f1.compare("test4"))
        f2 = file.File("test5")
        self.assertTrue(f1.compare(f2))
        with open(f2.path, mode="w") as f:
            f.write("pouet")
        self.assertFalse(f1.compare(f2, True))

    def test_file_backup(self):
        f = file.File("test6")
        backup = f.backup()
        f.backup()
        self.assertTrue(os.path.exists("test6.tdcski"))
        self.assertTrue(f.compare(backup))
        backup.remove()
        self.assertFalse(os.path.exists("test6.tdcski"))

    def test_file_copy(self):
        f = file.File("test7")
        copy = f.copy("test7_2")
        self.assertTrue(os.path.exists("test7_2"))
        self.assertTrue(f.compare(copy))
        with self.assertRaises(file.FileCopyError):
            f.copy("test7_2")
        f.copy("test7_2", overwrite=True)
        self.assertTrue(os.path.exists("test7_2"))
        self.assertTrue(f.compare(copy))
        copy.remove()

    def test_write(self):
        dummy = ["caribou\n", "meuh\n", "tchoutchou\n"]
        f = file.File("test_write", must_exist=False)
        f.write_lines(dummy)
        with open("test_write") as result:
            self.assertEqual(result.readlines(), dummy)
        with open("test_write") as result:
            self.assertEqual(result.readlines(), f.read_lines())

    ## skipped due to buggy function
    #~ def test_is_binary(self):
        #~ f1 = file.File("tdcski.exe")
        #~ f2 = file.File("README.md")
        #~ self.assertTrue(f1.is_binary)
        #~ self.assertFalse(f2.is_binary)




def main():

    return 0

if __name__ == '__main__':
    unittest.main(verbosity=9)

