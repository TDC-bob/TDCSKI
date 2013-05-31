# coding=utf-8
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

try:
    import bobgit.git as git
except ImportError:
    # noinspection PyUnresolvedReferences
    import git
from _logging._logging import mkLogger, DEBUG

logger = mkLogger(__name__, DEBUG)

def main():
    local = r"C:\Documents and Settings\owner\My Documents\BORIS\TDC\TDCMEME.git"
    remote = "https://github.com/TDC-bob/_logging.git"
    repo = git.Repo(local, remote)
##    repo.fetch()
##    print(repo)
##    print(repo.current_commit)
    repo.checkout("master")

    print("Press ENTER to close this window")
##    input()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass


