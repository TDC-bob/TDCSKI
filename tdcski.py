# -*- coding: utf-8 -*-
__author__ = 'bob'

import os
import sys
import winreg
import traceback
from time import strftime, gmtime
from mod import Mod
import config
from config import Config
from bobgit.git import Repo
from optparse import OptionParser
from _logging._logging import mkLogger, DEBUG

logger = mkLogger(__name__, DEBUG, "../logs/{} - TDCSKI.log".format(strftime("%Y%m%d - %Hh%Mm%S", gmtime())))

mods = []
skins = []
offline_mode = False

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
    logger.info("parsing des arguments")
    parser = OptionParser()
    parser.add_option("-u", "--update-list", action="store_true", dest="list_update_only",
                  help="se contente de mettre à jour la liste des mods", default=False)
    parser.add_option("-O", "--offline", action="store_true", dest="offline_mode",
                  help="lancer le programme en mode offline (aucune mise à jour, "
                       "seulement installation/désinstallation", default=False)
    # parser.add_option("-q", "--quiet",
    #               action="store_false", dest="verbose", default=True,
    #               help="don't print status messages to stdout")

    (options, args) = parser.parse_args()
    config.offline_mode = options.offline_mode
    logger.info("lecture du fichier tdcski.cfg")
    # noinspection PyBroadException
    try:
        conf = Config()
    except Exception:
        logger.error("le fichier de configuration est corrompu, supprimez-le et j'en réinstallerai un nouveau")
        logger.debug("appuyez sur ENTER pour quitter")
        input()
        exit(1)

    logger.info("recherche du répertoire d'installation de DCS")
    try:
        dcs_path, caribou = winreg.QueryValueEx (winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Eagle Dynamics\DCS World"), "Path")
    except FileNotFoundError:
        logger.error("impossible de trouver une installation de DCS")
        logger.debug("appuyez sur ENTER pour quitter")
        exit(1)
    # noinspection PyUnboundLocalVariable
    logger.info("le répertoire d'installation DCS détecté est: \n\t\t{}".format(dcs_path))
    # noinspection PyUnboundLocalVariable
    conf.create("general", "dcs_path", dcs_path)

    try:
        logger.info('détection du répertoire "Saved Games"')
        saved_games_path = os.path.normpath(os.path.expanduser("~/saved games/dcs"))
        logger.info('le répertoire "Saved Games" détecté est: \n\t\t{}'.format(saved_games_path))
        conf.create("general", "saved_games_path", saved_games_path)

        logger.info("lecture des répertoires à utiliser dans le fichier \"tdcski.cfg\"")
        config.git_exe = conf.get("general", "git_path")
        config.SaveGames_path = conf.get("general", 'saved_games_path')
        config.DCS_path = conf.get("general", 'dcs_path')
        logger.info('répertoire "DCS" utilisé: {}'.format(config.DCS_path))
        logger.info('répertoire "Saved Games" utilisé: {}'.format(config.SaveGames_path))

        if not os.path.exists("../repos/skins"):
            os.makedirs("../repos/skins")
        if not os.path.exists("../repos/mods"):
            os.makedirs("../repos/mods")

        logger.info("mise à jour de la liste des mods/skins")
        Repo("../repos/list", "https://github.com/TDC-bob/modlist.git")

        if options.list_update_only:
            logger.info("la mise à jour de la liste est terminée, je quitte")
            exit(0)

        sys.path.append(os.path.abspath("../repos/list/"))
        # noinspection PyUnresolvedReferences
        import list
        mods = []
        skins = []
        # noinspection PyUnresolvedReferences
        if offline_mode:
            logger.info("programme en mode offline, aucune mise à jour à ligne")
        else:
            for m in list.mods:
                logger.info("mise à jour du mod: {}".format(m))
                # noinspection PyUnresolvedReferences
                m = Mod(m, "mod", "../repos/mods", list.mods[m])
                mods.append(m)

            # noinspection PyUnresolvedReferences
            for s in list.skins:
                logger.info("mise à jour de la skin: {}".format(s))
                # noinspection PyUnresolvedReferences
                s = Mod(s, "skin", "../repos/skins", list.skins[s])
                skins.append(s)

            logger.info("fin des mises à jour")
        # logger.info("list des mods disponibles: {}".format("\n".join(m.name for m in mods)))
        # logger.info("list des skins disponibles: {}".format("\n".join(s.name for s in skins)))
        logger.info("(dés)installation des mods / skins")
        for mod in mods:
            mod.check()
        for skin in skins:
            skin.check()

    except Exception as e:
        logger.error(e.__class__)
        logger.error(e)
        logger.error("TRACEBACK: {}".format("\n".join(traceback.format_tb(e.__traceback__))))
        logger.debug("appuyez sur ENTER pour quitter")
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


