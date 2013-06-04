# coding=utf-8
__author__ = 'bob'

import os
import sys
import winreg
import traceback
from time import strftime, gmtime
from lib.configobj import ConfigObj
from mod import Mod
import config
from config import Config
import ui_server
from bobgit.git import Repo
from _logging._logging import mkLogger, DEBUG, WARN

logger = mkLogger(__name__, DEBUG, "../logs/{} - TDCSKI.log".format(strftime("%Y%m%d - %Hh%Mm%S", gmtime())))


mods = []
skins = []


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
    logger.info("Lecture du fichier de configuration")
    try:
        conf = Config()
    except Exception as e:
        logger.error("Le fichier de configuration est corrompu, supprimez-le et j'en réinstallerai un nouveau")
        logger.debug("Appuyez sur ENTER pour quitter")
        input()
        exit(1)

    logger.info("Recherche du répertoire d'installation de DCS dans la base de registre")
    try:
        dcs_path, caribou = winreg.QueryValueEx (winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Eagle Dynamics\DCS World"), "Path")
    except FileNotFoundError:
        logger.error("Impossible de trouver une installation de DCS")
        logger.debug("Appuyez sur ENTER pour quitter")
        exit(1)
    logger.info("Le répertoire d'installation DCS détecté est: \n\t\t{}".format(dcs_path))
    conf.create("general", "dcs_path", dcs_path)

    try:
        logger.info("Détection du répertoire Saved Games")
        saved_games_path = os.path.normpath(os.path.expanduser("~/saved games/dcs"))
        logger.info("Le répertoire d'installation DCS détecté est: \n\t\t{}".format(saved_games_path))
        conf.create("general", "saved_games_path", saved_games_path)

        config.git_exe = conf.get("general", "git_path")
        config.SaveGames_path = conf.get("general", 'saved_games_path')
        config.DCS_path = conf.get("general", 'dcs_path')

        if not os.path.exists("../repos/skins"):
            os.makedirs("../repos/skins")
        if not os.path.exists("../repos/mods"):
            os.makedirs("../repos/mods")

        logger.info("Création du repository principal")
        Repo("../repos/list", "https://github.com/TDC-bob/modlist.git").pull()

        sys.path.append(os.path.abspath("../repos/list/"))
        # noinspection PyUnresolvedReferences
        import list
        mods = []
        skins = []
        for m in list.mods:
            m = Mod(m, "mod", "../repos/mods", list.mods[m])
            m.pull_repo()
            mods.append(m)

        for s in list.skins:
            s = Mod(s, "skin", "../repos/skins", list.skins[s])
            s.pull_repo()
            skins.append(s)

        logger.info("Fin des mises à jour")
        logger.info("List des mods disponibles: {}".format("\n".join(m.name for m in mods)))
        logger.info("List des skins disponibles: {}".format("\n".join(s.name for s in skins)))
        logger.info("Vérification de ce qu'il faut installer/désinstaller")
        for mod in mods:
            mod.check()
        for skin in skins:
            skin.check()

    except Exception as e:
        logger.error(e.__class__)
        logger.error(e)
        logger.error("Traceback: {}".format("\n".join(traceback.format_tb(e.__traceback__))))
        logger.debug("Appuyez sur ENTER pour quitter")
        input()
        exit(1)
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
    logger.info("tout s'est bien passé !")
    print("Press ENTER to close this window")

if __name__ == '__main__':
    main()


