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

import git
from _logging._logging import logged, mkLogger, DEBUG, INFO, WARN, ERROR
logger = mkLogger(__name__, DEBUG)

# test

def main():
    remote = "https://github.com/TDC-bob/bobgit.git"
    local = r"C:\Documents and Settings\owner\My Documents\BORIS\TDC\tests8.git"
    p = git.GSP()
    p.clone(remote, local)
    p.pull(local)
    print("Press ENTER to close this window")
    input()

if __name__ == '__main__':
    main()


