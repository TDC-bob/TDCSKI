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

import bobgit.git as git
import _logging
logger = _logging.mkLogger(__name__, _logging.DEBUG)

def main():
##    git._run(["clone","https://github.com/caolan/async","test1"])
    p = git.GSP()
    p._run(["merge","master"])
    print("Press ENTER to close this window")
    input()

if __name__ == '__main__':
    main()


