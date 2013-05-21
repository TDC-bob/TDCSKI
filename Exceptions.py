# -*- coding: UTF-8 -*-
#-------------------------------------------------------------------------------
# Author:      Bob Daribouca
#
# Copyright:   (c) Bob Daribouca 2013
# Licence:     CC BY-NC-SA 3.0
#
#               Please refer to the "LICENSE" file distributed with the package,
#               or to http://creativecommons.org/licenses/by-nc-sa/3.0/
#
#-------------------------------------------------------------------------------
#!/usr/bin/env python


from . import _logging
logger = _logging.mkLogger("EXCEPTION")

def wait_for_console():
    print("\n\nAppuyez sur ENTER pour fermer la fenêtre")
    input()

class Error(Exception):
    def __init__(self, short_msg="Pas de description", long_msg="Pas d'information supplémentaire", logger=logger):
        logger.exception('''FATAL ERROR: {}\n\tMessage: {}'''.format(base_info, message))

class GitRunError(Exception):
    def __init__(self, short_msg="Pas de description", long_msg="Pas d'information supplémentaire", logger=logger):
        logger.exception('''ERREUR FATALE\n\nDESCRIPTION: {}\nMESSAGE: {}\nDETAILS TECHNIQUES:\n\n'''.format(short_msg, long_msg))
        wait_for_console()
