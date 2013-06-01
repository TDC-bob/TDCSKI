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

import os
import sys
import winreg
import mod as mod
import bobgit.git as git
from _logging._logging import mkLogger, DEBUG

logger = mkLogger(__name__, DEBUG)

def main():
    os.environ["GIT_SSL_NO_VERIFY"] = "1"

    DCS_path, _type = winreg.QueryValueEx (winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Eagle Dynamics\DCS World"), "Path")

    if not os.path.exists("../mods"):
        os.makedirs("../mods")
    git.Repo("../mods/modlist", "https://github.com/TDC-bob/modlist.git").pull()
    sys.path.append(os.path.abspath("../modlist/"))
    # noinspection PyUnresolvedReferences
    import modlist
    for m in modlist.mods:
        test = mod.Mod(m, modlist.mods[m])
        test.repo.pull()
        print(test)
        for file in test.files:
            print(file)
    print("Press ENTER to close this window")
    input()

if __name__ == '__main__':
    main()


