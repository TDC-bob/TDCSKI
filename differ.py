#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      owner
#
# Created:     21/06/2013
# Copyright:   (c) owner 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python

import os
import difflib

#!/usr/bin/env python

# mymerge.py - simple 3-way merge tool for Mercurial
#
# Copyright 2006 Marcos Chaves <marcos.nospam at gmail.com>
#
# This software may be used and distributed according to the terms
# of the GNU General Public License, incorporated herein by reference.

import difflib
import sys

def read_file(filename):
    try:
        f = open(filename, 'rb')
        l = f.readlines()
        f.close()
    except IOError, err:
        print "can't open file '" + filename + "'. aborting."
        sys.exit(-1)
    else:
        return l

def drop_inline_diffs(diff):
    r = []
    for t in diff:
        if not t.startswith('?'):
            r.append(t)
    return r

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

if len(sys.argv) < 4:
    print 'mymerge.py my base other [merged]'
    sys.exit(-1)

a = read_file(sys.argv[1])
x = read_file(sys.argv[2])
b = read_file(sys.argv[3])

had_conflict, m = merge_files(a, x, b)

try:
    if len(sys.argv) == 5:
        f = open(sys.argv[4], 'wb')
    else:
        f = open(sys.argv[1], 'wb')
    for line in m:
        f.write(line)
    f.close()
except IOError, err:
    print "can't write to merged file. aborting."
    sys.exit(-1)

if had_conflict:
    sys.exit(-1)

def is_binary(filename):
    """
    Return true if the given filename appears to be binary.
    File is considered to be binary if it contains a NULL byte.
    FIXME: This approach incorrectly reports UTF-16 as binary.
    """
    with open(filename, 'rb') as f:
        for block in f:
            if '\0' in block:
                return True
    return False

def main():
    p1 = "CHANGELOG"
    p2 = "CHANGELOG.tmp"
    differ = difflib.HtmlDiff()
    with open("results.html", mode="w") as r, open(p1) as f1, open(p2) as f2:
        r.write(differ.make_file(f1.readlines(), f2.readlines(), context=True))
    pass

if __name__ == '__main__':
    main()
