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

def write_error_to_log(base_info, long_msg):
    logger.error('''{}\n\tMessage: {}'''.format(base_info, long_msg))

class Error(Exception):
    def __init__(self, base_info="Pas d'information sur cette erreur", long_msg="Pas de message pour cette erreur", logger=logger):
        write_error_to_log(base_info, long_msg)

class GitRunError(Error):
    def __init__(self, long_msg="Pas d'information supplémentaire", logger=logger):
        write_error_to_log("GIT RUN ERROR", long_msg)

class GitNotFound(Error):
    def __init__(self, long_msg="Pas d'information supplémentaire", logger=logger):
        write_error_to_log("GIT NOT FOUND", long_msg)

class GitFetchError(Error):
    def __init__(self, long_msg="Pas d'information supplémentaire", logger=logger):
        write_error_to_log("GIT FETCH ERROR", long_msg)

class GitCloneError(Error):
    def __init__(self, long_msg="Pas d'information supplémentaire", logger=logger):
        write_error_to_log("GIT CLONE ERROR", long_msg)
