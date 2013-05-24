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


from _logging._logging import mkLogger, logged, DEBUG, INFO, WARN, ERROR
logger = mkLogger("EXCEPTION")

class Error(Exception):
    def __init__(self, base_info="Pas d'information sur cette erreur", message="Pas de message pour cette erreur", logger=logger):
        logger.error('''FATAL ERROR: {}\n\tMessage: {}'''.format(base_info, message))

class GitRunError(Exception):
    def __init__(self, short_msg="Pas de description", long_msg="Pas d'information supplémentaire", logger=logger):
        logger.error('''FATAL ERROR: {}\n\tMessage: {}'''.format(short_msg, long_msg))
