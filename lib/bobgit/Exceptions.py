# -*- coding: utf-8 -*-
__author__ = 'bob'


from _logging._logging import mkLogger

logger = mkLogger("EXCEPTION")

def write_error_to_log(base_info, long_msg, logger=logger):
    logger.error('''{}\nMessage:\n{}'''.format(base_info, long_msg))

class GitError(Exception):
    def __init__(self, base_info="Pas d'information sur cette erreur", long_msg="Pas de message pour cette erreur", logger=logger):
        write_error_to_log(base_info, long_msg, logger=logger)

class GitRunError(GitError):
    def __init__(self, long_msg="Pas d'information supplémentaire", logger=logger):
        write_error_to_log("GIT RUN ERROR", long_msg, logger=logger)

class GitNotFound(GitError):
    def __init__(self, long_msg="Pas d'information supplémentaire", logger=logger):
        write_error_to_log("GIT NOT FOUND", long_msg, logger=logger)

class GitFetchError(GitError):
    def __init__(self, long_msg="Pas d'information supplémentaire", logger=logger):
        write_error_to_log("GIT FETCH ERROR", long_msg, logger=logger)

class GitCloneError(GitError):
    def __init__(self, long_msg="Pas d'information supplémentaire", logger=logger):
        write_error_to_log("GIT CLONE ERROR", long_msg, logger=logger)

class GitRepoDoesNotExist(GitError):
    def __init__(self, long_msg="Pas d'information supplémentaire", logger=logger):
        write_error_to_log("GIT REPO ERROR", long_msg, logger=logger)

class GitListRemoteError(GitError):
    def __init__(self, long_msg="Pas d'information supplémentaire", logger=logger):
        write_error_to_log("GIT LIST REMOTE ERROR", long_msg, logger=logger)

class GitRemoteError(GitError):
    def __init__(self, long_msg="Pas d'information supplémentaire", logger=logger):
        write_error_to_log("GIT REMOTE ERROR", long_msg, logger=logger)

class GitCheckoutError(GitError):
    def __init__(self, long_msg="Pas d'information supplémentaire", logger=logger):
        write_error_to_log("GIT CHECKOUT ERROR", long_msg, logger=logger)

class GitRemoteNotKnown(GitError):
    def __init__(self, long_msg="Pas d'information supplémentaire", logger=logger):
        write_error_to_log("GIT UNKNOWN REMOTE", long_msg, logger=logger)

class GitBranchNotKnown(GitError):
    def __init__(self, long_msg="Pas d'information supplémentaire", logger=logger):
        write_error_to_log("GIT UNKNOWN BRANCH", long_msg, logger=logger)

class GitRemoteAddError(GitError):
    def __init__(self, long_msg="Pas d'information supplémentaire", logger=logger):
        write_error_to_log("GIT REMOTE ADD ERROR", long_msg, logger=logger)

class GitResetError(GitError):
    def __init__(self, long_msg="Pas d'information supplémentaire", logger=logger):
        write_error_to_log("GIT RESET ERROR", long_msg, logger=logger)

class GitPullError(GitError):
    def __init__(self, long_msg="Pas d'information supplémentaire", logger=logger):
        write_error_to_log("GIT PULL ERROR", long_msg, logger=logger)

class GitInitError(GitError):
    def __init__(self, long_msg="Pas d'information supplémentaire", logger=logger):
        write_error_to_log("GIT INIT ERROR", long_msg, logger=logger)

class GitAddRemoteError(GitError):
    def __init__(self, long_msg="Pas d'information supplémentaire", logger=logger):
        write_error_to_log("GIT ADD REMOTE ERROR", long_msg, logger=logger)

class GitMergeError(GitError):
    def __init__(self, long_msg="Pas d'information supplémentaire", logger=logger):
        write_error_to_log("GIT MERGE ERROR", long_msg, logger=logger)
