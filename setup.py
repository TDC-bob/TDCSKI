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

# Let's start with some default (for me) imports...

from cx_Freeze import setup, Executable
import traceback
import sys
import os



# Process the includes, excludes and packages first

includes = ["html/", "tdcski/"]
excludes = []
packages = ["tdcski","cherrypy","mako"]
path = sys.path + ['cherrypy', 'mako', "tdcski"]


# This is a place where the user custom code may go. You can do almost
# whatever you want, even modify the data_files, includes and friends
# here as long as they have the same variable name that the setup call
# below is expecting.

# No custom code added

# The setup for cx_Freeze is different from py2exe. Here I am going to
# use the Python class Executable from cx_Freeze


# base = None
# if sys.platform == "win32":
#     base = "Win32GUI"

exe = Executable(
    # what to build
    "tdcski.py",
    initScript = None,
    # base = "Win32GUI",
    targetDir = "dist",
    targetName = "tdcski.exe",
    compress = True,
    copyDependentFiles = True,
    appendScriptToExe = False,
    appendScriptToLibrary = False,
    icon = "resources/tdcski.ico"
    )


# That's serious now: we have all (or almost all) the options cx_Freeze
# supports. I put them all even if some of them are usually defaulted
# and not used. Some of them I didn't even know about.

setup(

    version = "0.0.1",
    description = "description",
    author = "TDC Bob",
    name = "TDCSKI",
    options = {"build_exe": {"include_files": includes,
                             "excludes": excludes,
                             # "path": path,
                             "packages": packages,
                             }
               },

    executables = [exe]
    )

# This is a place where any post-compile code may go.
# You can add as much code as you want, which can be used, for example,
# to clean up your folders or to do some particular post-compilation
# actions.

# No post-compilation code added


# And we are done. That's a setup script :-D

