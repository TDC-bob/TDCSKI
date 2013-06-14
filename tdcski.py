# -*- coding: utf-8 -*-
__author__ = 'bob'

import os
import sys
import winreg
import traceback
from mission import Mission
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

def main():
    # test_path = r"C:\Users\bob\Saved Games\DCS\Missions\TDCSKI_test.miz"
    # with Mission(test_path) as mission:
    #     print(mission.next_group_id())
    #     print(mission.next_unit_id())
    #     print(mission.unit_ids)
    #     print(mission.group_ids)
    #     pass
    # return
    logger.info("parsing des arguments")
    parser = OptionParser()
    parser.add_option("-U", "--update-list", action="store_true", dest="update_list_only",
                  help="se contente de mettre à jour la liste des mods", default=False)
    parser.add_option("-u", "--update", action="store_true", dest="update",
                  help="mettre les mods / skins à jour", default=False)

    (options, args) = parser.parse_args()
    config.update = options.update
    config.update_list_only = options.update_list_only


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
        input()
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
        Repo("../repos/list", "https://github.com/TDC-bob/modlist.git", "master", (config.update or config.update_list_only))

        if config.update_list_only:
            logger.info("la mise à jour de la liste est terminée, je quitte")
            exit(0)

        sys.path.append(os.path.abspath("../repos/list/"))
        # noinspection PyUnresolvedReferences
        import list
        mods = []
        skins = []
        # noinspection PyUnresolvedReferences
        if config.update:
            logger.info("mise à jour des mods et des skins en ligne")
        else:
            logger.info("programme en mode offline, lecture sur le disque dur local")
        for m in list.mods:
            logger.info("traitement du mod: {}".format(m))
            # noinspection PyUnresolvedReferences
            m = Mod(m, "mod", "../repos/mods", list.mods[m], config.update)
            mods.append(m)

        # noinspection PyUnresolvedReferences
        for s in list.skins:
            logger.info("traitement de la skin: {}".format(s))
            # noinspection PyUnresolvedReferences
            s = Mod(s, "skin", "../repos/skins", list.skins[s], config.update)
            skins.append(s)


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

    if config.update:
        conf.set_or_create("general", "initialized", "y")
    logger.info("tout s'est bien passé !")
    print("Press ENTER to close this window")

if __name__ == '__main__':
    main()


