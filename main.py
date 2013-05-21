#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      owner
#
# Created:     19/05/2013
# Copyright:   (c) owner 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python

import lib.git.git as git
import _logging
logger = _logging.mkLogger(__name__, _logging.DEBUG)

def main():
##    git._run(["clone","https://github.com/caolan/async","test1"])
    p = git.GSP()
    p._run(["merge","master"])
    print("Chouk de merde !")
    print("Press ENTER to close this window")
    input()

if __name__ == '__main__':
    main()

'''
#!/usr/bin/python

# This script is a template for writing CLI commands in python.

# Note using "#!/usr/bin/env python" above will
# cause the system to register the name (in ps etc.)
# as "python" rather than the command name
# (as "python" is passed to exec by env).

import sys

# The following exits cleanly on Ctrl-C,
# while treating other exceptions as before.
def cli_exception(type, value, tb):
    if not issubclass(type, KeyboardInterrupt):
        sys.__excepthook__(type, value, tb)
if sys.stdin.isatty():
    sys.excepthook=cli_exception

# The following demonstrates common option argument processing
import os
def Usage():
    print "Usage: %s [OPTION] [PATHS]" % os.path.split(sys.argv[0])[1]
    print "    --name=value    whatever"
    print "    --help          display help"

import getopt
try:
    lOpts, lArgs = getopt.getopt(sys.argv[1:], "", ["help","name="])

    if len(lArgs) == 0:
        lArgs = [os.getcwd()]

    if ("--help","") in lOpts:
        Usage()
        sys.exit(None)

    name=None
    for opt in lOpts:
        if opt[0] == "--name":
            name=opt[1]
            print "name =",name

except getopt.error, msg:
    print msg
    print
    Usage()
    sys.exit(2)

print "processing", lArgs
print "Ctrl-C to exit"
sys.stdin.readline()
'''
