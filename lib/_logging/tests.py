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

import unittest, logging

try:
    import _logging
except ImportError:
    from . import _logging

# noinspection PyUnresolvedReferences
class TestLoggingPackage(unittest.TestCase):

    def SetUp(self):
        pass

    def TearDown(self):
        pass

    def test_main_logger_init(self):
        logger = _logging.mkLogger("main")
        self.assertTrue(type(logger) == logging.Logger)


if __name__ == '__main__':
    unittest.main(verbosity=9)
