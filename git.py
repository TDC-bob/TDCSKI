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
import re
##try:
##    from . import Exceptions
##except (ImportError, SystemError):
##    import bobgit.Exceptions as Exceptions
##import bobgit.Exceptions as Exceptions
##from .Exceptions import *
from . import Exceptions

from _logging._logging import logged, mkLogger, DEBUG, INFO, WARN, ERROR
logger = mkLogger(__name__, DEBUG)

#todo: import _logging as a subtree (FFS, that's getting tangled)

class Repo():
    @logged
    def __init__(self, local, remote=None):
        self.local = local
        self.git_exe = self.__get_git_exe()
        self.cloned = False
        self.fetched = False
        self.up_to_date = False
        self.merged = False
        self.local_repo_exists = os.path.exists(local)
        self.remotes = []
        if not (remote or self.local_repo_exists):
            raise Exceptions.GitRepoDoesNotExist(
                    "no local directory found, and no remote given")

        if not self.local_repo_exists:
            pass
        self.build_remotes_list()

    def build_remotes_list(self):
        success, output, cmd = self.__run(["remote","-v","show"])
        if not success:
            raise Exceptions.GitListRemoteError("\tOutput: {}\n\tCmd: {}".format(output, cmd))
        lines = output.split("\n")
        for line in lines[:-1]:
            chunks = re.split('[ \t\r\f\v]', line)
            self.remotes.append(Remote(chunks[0],chunks[1],re.sub("[\(\)]","",chunks[2]),self))


    @logged
    def __run(self, args):
        '''
        Runs an arbitrary git command
        '''

        cur_dir = os.getcwd()
        if not cur_dir == self.local:
            os.chdir(self.local)
        cmd = [self.git_exe]
        for a in args:
            cmd.append(a)
##        cmd.append("-v")
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
            os.chdir(cur_dir)
            return False, e.output, e.cmd
        #TODO: parse return ?
        sep = "----------------------------------------------------"
        self.logger.info("output:\n{}\n{}\n{}".format(sep,rtn,sep))
        os.chdir(cur_dir)
        return True, rtn, cmd

    def __str__(self):
        return ("\n\t".join(["REPO:",
                    "Local: {}",
                    "Cloned: {}",
                    "Merged: {}",
                    "Remotes: \n\t\t{}"
                    ])).format(
                    self.local,
                    self.cloned,
                    self.merged,
                    "\n\t\t".join(
                            [str(remote) for remote in self.remotes]
                                )
                    )


    @staticmethod
    def __get_git_exe():
        paths = ["./bobgit/bin/git.exe",
                "./bin/git.exe"
                ]
        for p in paths:
            if os.path.exists(p):
                return os.path.abspath("./bobgit/bin/git.exe")
        if not self.git:
            raise Exceptions.GitNotFound("Could not find git",
                "Could not find git.exe in following paths: {}".format(repr(paths)))

class Remote():
    @logged
    def __init__(self, name, address, _type, repo):
        self.repo = repo
        self.name = name
        self.address = address
        self.type = _type
        if not self.type in ["fetch","push"]:
            raise Exceptions.GitRemoteError("Unknown remote type: {}".format(self.type))

    def __str__(self):
        return "REMOTE:\n\tName: {}\n\tAddress: {} ({})\n\tParent repo: {}".format(
                        self.name, self.address, self.type, self.repo.local
                        )

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
        success, rtn, cmd = self._run(["fetch", remote])
        if not success:
            raise Exceptions.GitFetchError("\tRepo: {}\n\tRemote: {}\n\tCmd: {}\n".format(repo,remote, cmd))
        if "[up to date]" in rtn:
            self.fetched = True
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
        for a in args:
            cmd.append(a)
        cmd.append("-v")
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
            return False, e.output, e.cmd
##            raise Exceptions.GitRunError(
##                "Git failed running: \n\n{}\n\n".format(" ".join([c for c in cmd[1:]])),
##                "OUTPUT:\n=========\n{}\n=========\nEND OF OUTPUT\n\n".format(output),
##                self.logger)
        #TODO: parse return ?
        self.logger.info("output: {}\n".format(rtn))
        return True, rtn, cmd
