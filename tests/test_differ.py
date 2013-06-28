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

__author__ = 'TDC-Bob'

import unittest
import os

from ..lib._logging._logging import mkLogger, logged, DEBUG
from ..tdcski.differ import three_way_merge
#logger = mkLogger(__name__, DEBUG)

class testDiffer(unittest.TestCase):

    def setUp(self):
        lines_orig = [
            "orig: first line",
            "orig: second line",
            "orig: third line"
        ]
        with open("original", mode="w") as orig:
            orig.writelines(lines_orig)

        lines_merger1 = [
            "1: first line",
            "1: second line",
            "1: third line"
        ]
        with open("first_merger", mode="w") as orig:
            orig.writelines(lines_merger1)

        lines_merger2 = [
            "2: first line",
            "2: second line",
            "2: third line"
        ]
        with open("second_merger", mode="w") as orig:
            orig.writelines(lines_merger2)
    def tearDown(self):
        os.remove("original")
        os.remove("first_merger")
        os.remove("second_merger")

    def test_one(self):
        three_way_merge("original", "first_merger", "first_merger")



def main():

    return 0

if __name__ == '__main__':
    unittest.main(verbosity=9)

