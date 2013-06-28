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
import difflib

# mymerge.py - simple 3-way merge tool for Mercurial
#
# Copyright 2006 Marcos Chaves <marcos.nospam at gmail.com>
#
# This software may be used and distributed according to the terms
# of the GNU General Public License, incorporated herein by reference.

import difflib
import sys
from .file import File
from ..lib._logging._logging import mkLogger, DEBUG
logger = mkLogger(__name__, DEBUG)

class DifferException(Exception):
    def __init__(self, msg):
        logger.error(msg)
        super(DifferException, self).__init__(msg)

class MergeConflict(DifferException):
    def __init__(self, base, f1, f2):
        msg = "conflit pendant la fusion des fichiers:\n"
        "\tBase: {}\n\tFichier1: {}\n\tFichier2: {}\n"
        "Voyez le fichier \"base\" pour plus de détails"
        " sur le conflit".format(base.path, f1.path, f2.path)
        super(MergeConflict, self).__init__(msg)

def _drop_inline_diffs(diff):
    r = []
    for t in diff:
        if not t.startswith('?'):
            r.append(t)
    return r

def three_way_merge(original_file, file_1, file_2, dest=None):
    """
    Tries to perform a merge of file_1 & file_2 into base

    Unless "dest" is explicitely given, the result of the merge
    is stored into "file_1"
    """
    base = File(original_file)
    f1 = File(file_1)
    f2 = File(file_2)
    if dest:
        dest = File(dest)
    else:
        dest = File(file_1)

    a = f1.read_lines()
    b = f2.read_lines()
    x = base.read_lines()

    dxa = difflib.Differ()
    dxb = difflib.Differ()
    xa = _drop_inline_diffs(dxa.compare(x, a))
    xb = _drop_inline_diffs(dxb.compare(x, b))

    m = [] # m is the result of the merge
    index_a = 0
    index_b = 0
    had_conflict = 0

    while (index_a < len(xa)) and (index_b < len(xb)):
        # no changes or adds on both sides
        if (xa[index_a] == xb[index_b] and
            (xa[index_a].startswith('  ') or xa[index_a].startswith('+ '))):
            m.append(xa[index_a][2:])
            index_a += 1
            index_b += 1
            continue

        # removing matching lines from one or both sides
        if ((xa[index_a][2:] == xb[index_b][2:])
            and (xa[index_a].startswith('- ') or xb[index_b].startswith('- '))):
            index_a += 1
            index_b += 1
            continue

        # adding lines in A
        if xa[index_a].startswith('+ ') and xb[index_b].startswith('  '):
            m.append(xa[index_a][2:])
            index_a += 1
            continue

        # adding line in B
        if xb[index_b].startswith('+ ') and xa[index_a].startswith('  '):
            m.append(xb[index_b][2:])
            index_b += 1
            continue

        # conflict - list both A and B, similar to GNU's diff3
        m.append("<<<<<<< A\n")
        while (index_a < len(xa)) and not xa[index_a].startswith('  '):
            m.append(xa[index_a][2:])
            index_a += 1
        m.append("=======\n")
        while (index_b < len(xb)) and not xb[index_b].startswith('  '):
            m.append(xb[index_b][2:])
            index_b += 1
        m.append(">>>>>>> B\n")
        had_conflict = 1

    # append remining lines - there will be only either A or B
    for i in range(len(xa) - index_a):
        m.append(xa[index_a + i][2:])
    for i in range(len(xb) - index_b):
        m.append(xb[index_b + i][2:])

    if had_conflict:
        raise MergeConflict(base, f1, f2)
    return had_conflict, m



def merge_files(a, x, b):
    dxa = difflib.Differ()
    dxb = difflib.Differ()
    xa = drop_inline_diffs(dxa.compare(x, a))
    xb = drop_inline_diffs(dxb.compare(x, b))

    m = []
    index_a = 0
    index_b = 0
    had_conflict = 0

    while (index_a < len(xa)) and (index_b < len(xb)):
        # no changes or adds on both sides
        if (xa[index_a] == xb[index_b] and
            (xa[index_a].startswith('  ') or xa[index_a].startswith('+ '))):
            m.append(xa[index_a][2:])
            index_a += 1
            index_b += 1
            continue

        # removing matching lines from one or both sides
        if ((xa[index_a][2:] == xb[index_b][2:])
            and (xa[index_a].startswith('- ') or xb[index_b].startswith('- '))):
            index_a += 1
            index_b += 1
            continue

        # adding lines in A
        if xa[index_a].startswith('+ ') and xb[index_b].startswith('  '):
            m.append(xa[index_a][2:])
            index_a += 1
            continue

        # adding line in B
        if xb[index_b].startswith('+ ') and xa[index_a].startswith('  '):
            m.append(xb[index_b][2:])
            index_b += 1
            continue

        # conflict - list both A and B, similar to GNU's diff3
        m.append("<<<<<<< A\n")
        while (index_a < len(xa)) and not xa[index_a].startswith('  '):
            m.append(xa[index_a][2:])
            index_a += 1
        m.append("=======\n")
        while (index_b < len(xb)) and not xb[index_b].startswith('  '):
            m.append(xb[index_b][2:])
            index_b += 1
        m.append(">>>>>>> B\n")
        had_conflict = 1

    # append remining lines - there will be only either A or B
    for i in range(len(xa) - index_a):
        m.append(xa[index_a + i][2:])
    for i in range(len(xb) - index_b):
        m.append(xb[index_b + i][2:])

    return had_conflict, m

#~ if len(sys.argv) < 4:
    #~ print('mymerge.py my base other [merged]')
    #~ sys.exit(-1)

#~ a = read_file(sys.argv[1])
#~ x = read_file(sys.argv[2])
#~ b = read_file(sys.argv[3])

#~ had_conflict, m = merge_files(a, x, b)

#~ try:
    #~ if len(sys.argv) == 5:
        #~ f = open(sys.argv[4], 'wb')
    #~ else:
        #~ f = open(sys.argv[1], 'wb')
    #~ for line in m:
        #~ f.write(line)
    #~ f.close()
#~ except IOError as err:
    #~ print("can't write to merged file. aborting.")
    #~ sys.exit(-1)
#~
#~ if had_conflict:
    #~ sys.exit(-1)

#~ def is_binary(filename):
    #~ """
    #~ Return true if the given filename appears to be binary.
    #~ File is considered to be binary if it contains a NULL byte.
    #~ FIXME: This approach incorrectly reports UTF-16 as binary.
    #~ """
    #~ with open(filename, 'rb') as f:
        #~ for block in f:
            #~ if '\0' in block:
                #~ return True
    #~ return False

def main():
    p1 = "CHANGELOG"
    p2 = "CHANGELOG.tmp"
    differ = difflib.HtmlDiff()
    with open("results.html", mode="w") as r, open(p1) as f1, open(p2) as f2:
        r.write(differ.make_file(f1.readlines(), f2.readlines(), context=True))
    pass

if __name__ == '__main__':
    main()


# another example from the Python help file:
import sys, os, time, difflib, optparse

def main():
     # Configure the option parser
    usage = "usage: %prog [options] fromfile tofile"
    parser = optparse.OptionParser(usage)
    parser.add_option("-c", action="store_true", default=False,
                      help='Produce a context format diff (default)')
    parser.add_option("-u", action="store_true", default=False,
                      help='Produce a unified format diff')
    hlp = 'Produce HTML side by side diff (can use -c and -l in conjunction)'
    parser.add_option("-m", action="store_true", default=False, help=hlp)
    parser.add_option("-n", action="store_true", default=False,
                      help='Produce a ndiff format diff')
    parser.add_option("-l", "--lines", type="int", default=3,
                      help='Set number of context lines (default 3)')
    (options, args) = parser.parse_args()

    if len(args) == 0:
        parser.print_help()
        sys.exit(1)
    if len(args) != 2:
        parser.error("need to specify both a fromfile and tofile")

    n = options.lines
    fromfile, tofile = args # as specified in the usage string

    # we're passing these as arguments to the diff function
    fromdate = time.ctime(os.stat(fromfile).st_mtime)
    todate = time.ctime(os.stat(tofile).st_mtime)
    with open(fromfile) as fromf, open(tofile) as tof:
        fromlines, tolines = list(fromf), list(tof)

    if options.u:
        diff = difflib.unified_diff(fromlines, tolines, fromfile, tofile,
                                    fromdate, todate, n=n)
    elif options.n:
        diff = difflib.ndiff(fromlines, tolines)
    elif options.m:
        diff = difflib.HtmlDiff().make_file(fromlines, tolines, fromfile,
                                            tofile, context=options.c,
                                            numlines=n)
    else:
        diff = difflib.context_diff(fromlines, tolines, fromfile, tofile,
                                    fromdate, todate, n=n)

    # we're using writelines because diff is a generator
    sys.stdout.writelines(diff)

if __name__ == '__main__':
    main()
