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
import config
from config import Config
import ui_server
from bobgit.git import Repo
from _logging._logging import mkLogger, DEBUG, WARN

logger = mkLogger(__name__, DEBUG, "tdcski - python.log")


def main():

    # config = Config()
    # print(config.values)
    # print(config.keys)
    # print(config.items)
    # # print(config.get("general", "python_path"))
    # # config.create("test", "test2", "test3", "test43")
    # # print(config.get("test", "test2", "test3"))
    # # print(config.set("test", "test2", "test3", "test55"))
    # # config.config["test"] = {}
    # # config.config["test"]["test2"] = {}
    # # config.config["test"]["test2"] = {}
    # # config.config["test"]["test2"]["test3"] = {}
    # # config.config["test"]["test2"]["test3"]["test43"] = "caribou"
    # # config.config.write()
    # exit(0)

    # saved_games_path = os.path.normpath(os.path.expanduser("~/saved games/dcs"))
    # print(os.path.exists(saved_games_path))
    # print(saved_games_path)
    # exit(0)

    # ui = ui_server.UIServer()
    # ui.start()
    # exit(0)

    # os.environ["GIT_SSL_NO_VERIFY"] = "1"
    conf = Config()
    try:
        dcs_path, caribou = winreg.QueryValueEx (winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Eagle Dynamics\DCS World"), "Path")
    except FileNotFoundError:
        logger.error("impossible de trouver une installation de DCS")
        exit(1)
    conf.create("general", "dcs_path", dcs_path)
    conf.create("general", "saved_games_path", os.path.normpath(os.path.expanduser("~/saved games/dcs")))
    config.git_exe = conf.get("general", "git_path")
    config.SaveGames_path = conf.get("general", 'saved_games_path')
    config.DCS_path = conf.get("general", 'dcs_path')

    if not os.path.exists("../repos/skins"):
        os.makedirs("../repos/skins")
    if not os.path.exists("../repos/mods"):
        os.makedirs("../repos/mods")


    Repo("../repos/list", "https://github.com/TDC-bob/modlist.git").pull()

    sys.path.append(os.path.abspath("../repos/list/"))
    # noinspection PyUnresolvedReferences
    import list
    for m in list.mods:
        test = mod.Mod(m, "mod", "../repos/mods", list.mods[m])
        test.pull_repo()
        test.install()
        # conf.create("mods", m, "path", test.local)
        # conf.create("mods", m, "desc", test.desc)
        # conf.create("mods", m, "installed", False)

    for s in list.skins:
        test = mod.Mod(s, "skin", "../repos/skins", list.skins[s])
        test.pull_repo()
        print(test.should_be_installed)
        if test.should_be_installed:
            test.install()
        # conf.create("skins", s, "path", test.local)
        # conf.create("skins", s, "desc", test.desc)
        # conf.create("skins", s, "installed", False)
        # for file in test.files:
        #     print(file)

        # print(test)
        # for file in test.files:
            # print(file)

    # skins = conf.get("skins")
    # for k in skins:
    #     print(k)
    #     for kk in skins[k]:
    #         print("{}: {}".format(kk, skins[k][kk]))
    # if bool(skins["TDC-Bob-huey"]["install"]):
    #     print('ok')
    #     print(type(bool(skins["TDC-Bob-huey"]["install"])))
    # print()
    print("Press ENTER to close this window")

if __name__ == '__main__':
    main()


