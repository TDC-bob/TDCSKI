﻿# -*- coding: UTF-8 -*-
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


from _logging._logging import mkLogger

logger = mkLogger("EXCEPTION")

def write_error_to_log(base_info, long_msg, logger=logger):
    logger.error('''{}\nMessage:\n{}'''.format(base_info, long_msg))

class Error(Exception):
    def __init__(self, base_info="Pas d'information sur cette erreur", long_msg="Pas de message pour cette erreur", logger=logger):
        write_error_to_log(base_info, long_msg, logger=logger)

class GitRunError(Error):
    def __init__(self, long_msg="Pas d'information supplémentaire", logger=logger):
        write_error_to_log("GIT RUN ERROR", long_msg, logger=logger)

class GitNotFound(Error):
    def __init__(self, long_msg="Pas d'information supplémentaire", logger=logger):
        write_error_to_log("GIT NOT FOUND", long_msg, logger=logger)

class GitFetchError(Error):
    def __init__(self, long_msg="Pas d'information supplémentaire", logger=logger):
        write_error_to_log("GIT FETCH ERROR", long_msg, logger=logger)

class GitCloneError(Error):
    def __init__(self, long_msg="Pas d'information supplémentaire", logger=logger):
        write_error_to_log("GIT CLONE ERROR", long_msg, logger=logger)

class GitRepoDoesNotExist(Error):
    def __init__(self, long_msg="Pas d'information supplémentaire", logger=logger):
        write_error_to_log("GIT REPO ERROR", long_msg, logger=logger)

class GitListRemoteError(Error):
    def __init__(self, long_msg="Pas d'information supplémentaire", logger=logger):
        write_error_to_log("GIT LIST REMOTE ERROR", long_msg, logger=logger)

class GitRemoteError(Error):
    def __init__(self, long_msg="Pas d'information supplémentaire", logger=logger):
        write_error_to_log("GIT REMOTE ERROR", long_msg, logger=logger)

class GitCheckoutError(Error):
    def __init__(self, long_msg="Pas d'information supplémentaire", logger=logger):
        write_error_to_log("GIT CHECKOUT ERROR", long_msg, logger=logger)

class GitRemoteNotKnown(Error):
    def __init__(self, long_msg="Pas d'information supplémentaire", logger=logger):
        write_error_to_log("GIT UNKNOWN REMOTE", long_msg, logger=logger)

class GitBranchNotKnown(Error):
    def __init__(self, long_msg="Pas d'information supplémentaire", logger=logger):
        write_error_to_log("GIT UNKNOWN BRANCH", long_msg, logger=logger)

class GitMergeError(Error):
    def __init__(self, long_msg="Pas d'information supplémentaire", logger=logger):
        write_error_to_log("GIT MERGE ERROR", long_msg, logger=logger)

class GitInitError(Error):
    def __init__(self, long_msg="Pas d'information supplémentaire", logger=logger):
        write_error_to_log("GIT INIT ERROR", long_msg, logger=logger)

class GitRemoteAddError(Error):
    def __init__(self, long_msg="Pas d'information supplémentaire", logger=logger):
        write_error_to_log("GIT REMOTE ADD ERROR", long_msg, logger=logger)

class GitResetError(Error):
    def __init__(self, long_msg="Pas d'information supplémentaire", logger=logger):
        write_error_to_log("GIT RESET ERROR", long_msg, logger=logger)

class GitPullError(Error):
    def __init__(self, long_msg="Pas d'information supplémentaire", logger=logger):
        write_error_to_log("GIT PULL ERROR", long_msg, logger=logger)
