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

from tdcski import ui_server
import tdcski
import os
import sys

def main():
    tdcski.MY_FULLNAME = os.path.normpath(os.path.abspath(os.path.join(os.getcwd(), "tdcski.exe")))
    tdcski.MY_NAME = os.path.basename(tdcski.MY_FULLNAME)
    tdcski.PROG_DIR = os.path.dirname(tdcski.MY_FULLNAME)
    tdcski.DATA_DIR = tdcski.PROG_DIR
    tdcski.MY_ARGS = sys.argv[1:]
    tdcski.CREATEPID = False
    tdcski.DAEMON = False


    ui_server.main()

if __name__ == "__main__":
    main()