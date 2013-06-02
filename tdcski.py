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
from lib.configobj import ConfigObj
import mod
from config import Config
import ui_server
from bobgit.git import Repo
from _logging._logging import mkLogger, DEBUG

logger = mkLogger(__name__, DEBUG)


def main():
    config = Config()
    print(config.values)
    print(config.keys)
    print(config.items)
    # print(config.get("general", "python_path"))
    # config.create("test", "test2", "test3", "test43")
    # print(config.get("test", "test2", "test3"))
    # print(config.set("test", "test2", "test3", "test55"))
    # config.config["test"] = {}
    # config.config["test"]["test2"] = {}
    # config.config["test"]["test2"] = {}
    # config.config["test"]["test2"]["test3"] = {}
    # config.config["test"]["test2"]["test3"]["test43"] = "caribou"
    # config.config.write()
    exit(0)
    saved_games_path = os.path.normpath(os.path.expanduser("~/saved games/dcs"))
    print(os.path.exists(saved_games_path))
    print(saved_games_path)
    exit(0)
    ui = ui_server.UIServer()
    ui.start()
    exit(0)
    # os.environ["GIT_SSL_NO_VERIFY"] = "1"
    DCS_path, _type = winreg.QueryValueEx (winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Eagle Dynamics\DCS World"), "Path")

    if not os.path.exists("../mods"):
        os.makedirs("../mods")

    Repo("../mods/modlist", "https://github.com/TDC-bob/modlist.git").pull()

    sys.path.append(os.path.abspath("../modlist/"))
    # noinspection PyUnresolvedReferences
    import modlist
    for m in modlist.mods:
        test = mod.Mod(m, modlist.mods[m])
        test.pull_repo()
        # print(test)
        # for file in test.files:
            # print(file)
    print("Press ENTER to close this window")
    # input()

if __name__ == '__main__':
    main()


