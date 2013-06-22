#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  untitled.py
#
#  Copyright 2013 bob <bob@tinybou>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
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

import unittest
import os
import file

from _logging._logging import mkLogger, logged, DEBUG
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





def main():

    return 0

if __name__ == '__main__':
    unittest.main(verbosity=9)

