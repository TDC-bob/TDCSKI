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

import os
import sys
import winreg
import tdcski.mod as mod
import bobgit.git as git
from _logging._logging import logged, mkLogger, DEBUG, INFO, WARN, ERROR
logger = mkLogger(__name__, DEBUG)

def main():
    value, type = winreg.QueryValueEx (winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Eagle Dynamics\DCS World"), "Path")
    print(value)

    if not os.path.exists("../mods"):
        os.makedirs("../mods")
    os.environ["GIT_SSL_NO_VERIFY"] = "1"
    modlist_repo = git.Repo("../mods/modlist", "https://github.com/TDC-bob/modlist.git")
    sys.path.append(os.path.abspath("../modlist/"))
    import modlist
    for m in modlist.mods:
        test = mod.Mod(m, modlist.mods[m])
        test.repo.
        print(test)
        for file in test.files:
            print(file)
    print("Press ENTER to close this window")
    input()

if __name__ == '__main__':
    main()


