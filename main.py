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
    import git
from _logging._logging import logged, mkLogger, DEBUG, INFO, WARN, ERROR
logger = mkLogger(__name__, DEBUG)

def main():
    local = r"C:\Documents and Settings\owner\My Documents\BORIS\TDC\TDCMEME.git"
    remote = "https://github.com/TDC-bob/_logging.git"
    repo = git.Repo(local, remote)
##    repo.fetch()
    print(repo)

    print("Press ENTER to close this window")
##    input()
    return
    remote = "https://github.com/TDC-bob/_logging.git"
    local = r"C:\Documents and Settings\owner\My Documents\BORIS\TDC\tests10.git"
    p = git.Git()
    p.clone(remote, local)
    p.pull(local)
    print("Press ENTER to close this window")
    input()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass


