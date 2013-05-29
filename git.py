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

import subprocess
import os
##try:
##    from . import Exceptions
##except (ImportError, SystemError):
##    import bobgit.Exceptions as Exceptions
##import bobgit.Exceptions as Exceptions
##from .Exceptions import *
from . import GitExceptions

from _logging._logging import logged, mkLogger, DEBUG, INFO, WARN, ERROR
logger = mkLogger(__name__, DEBUG)

#todo: import _logging as a subtree (FFS, that's getting tangled)

class Git():
    """
    Git wrapper

    Instanciation won't do anything to the local/remote FS, it's just to set up
    the local path to the Git executable and its libraries/templates.

    .. note::

       This is but a VERY basic stand-alone version of Git, with VERY limited functionalities.

    """
    @logged
    def __init__(self):
        '''
        Checks for git.exe path.

        May switch to a glob.glob() type os search in the PATH later on
        '''
        self.git = None
        paths = ["./bobgit/bin/git.exe",
                "./bin/git.exe"
                ]
        for p in paths:
            if os.path.exists(p):
                self.git = os.path.abspath("./bobgit/bin/git.exe")
        if not self.git:
            raise Exceptions.GitNotFound("Could not find git",
                "Could not find git.exe in following paths: {}".format(repr(paths)))

    def clone(self, remote_repo, local_repo_name=""):
        '''
        Alias for the git 'clone' command

        :param remote_repo: full path or web address of the repo you want to clone
        :type remote_repo: string
        :param local_repo_name: the local path of the clone (defaults to Git default")
        :type local_repo_name: string
        :returns: output of both fetch & merge command
        :rtype: list
        '''
##        cur_dir = os.getcwd()
##        os.chdir(os.path.normpath(os.path.join(os.getcwd(),"bobgit")))
        if os.path.exists(local_repo_name):
            return False
        success, rtn = self._run(["clone",remote_repo,local_repo_name])
        self.logger.debug("Git clone: {}".format(rtn))
        print("success: {}".format(success))
        print(rtn == "Cloning into '{}'...")
##        os.chdir(cur_dir)

    def pull(self, repo, remote="origin"):
        '''
        Alias for the git 'pull' command

        :param repo: full path to the repo in which the pull has to be run
        :type repo: string
        :param remote: the remote to pull from (defaults to origin)
        :type remote: string
        :returns: output of both fetch & merge command
        :rtype: list
        '''
        cur_dir = os.getcwd()
        os.chdir(repo)
        rtn_fetch = self.fetch(repo,remote)
        rtn_merge = self.merge(repo,"master")
        os.chdir(cur_dir)
        return rtn_fetch, rtn_merge

    def fetch(self, repo, remote="origin"):
        cur_dir = os.getcwd()
        os.chdir(repo)
        success, rtn = self._run(["fetch", remote])
        if not success:
            raise GitExceptions.GitFetchError("\tRepo: {}\n\tRemote: {}\n".format(repo,remote))
        os.chdir(cur_dir)
        return rtn

    def merge(self, repo, branch="master"):
        cur_dir = os.getcwd()
        os.chdir(repo)
        success, rtn = self._run(["merge", branch])
        if not success:
            raise Exceptions.GitCloneError("\tRepo: {}\n\tBranch: {}\n".format(repo,branch))
        os.chdir(cur_dir)
        return rtn


    @logged
    def _run(self, args):
        '''
        Runs an arbitrary git command
        '''

        cmd = [self.git]
        cmd.append("-v")
        for a in args:
            cmd.append(a)
        self.logger.info("running git command: {}".format(cmd[1:]))
        try:
            rtn = subprocess.check_output(
                        cmd,
                        shell=True,
                        universal_newlines=True,
                        stderr=subprocess.STDOUT
                        )
        except subprocess.CalledProcessError as e:
            cmd, code, output = e.cmd, e.returncode, e.output
            return False, e.output
##            raise Exceptions.GitRunError(
##                "Git failed running: \n\n{}\n\n".format(" ".join([c for c in cmd[1:]])),
##                "OUTPUT:\n=========\n{}\n=========\nEND OF OUTPUT\n\n".format(output),
##                self.logger)
        #TODO: parse return ?
        self.logger.info("output: {}\n".format(rtn))
        return True, rtn
