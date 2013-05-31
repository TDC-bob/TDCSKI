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
try:
    from . import Exceptions
except (ImportError, SystemError):
    import Exceptions

from _logging._logging import logged, mkLogger, DEBUG, INFO, WARN, ERROR
logger = mkLogger(__name__, DEBUG)


class Repo():
    @logged
    def __init__(self, local, init_remote=None):
        self.local = local
        self.git_exe = self.__get_git_exe()
        self.cloned = False
        self.fetched = False
        self.up_to_date = False
        self.merged = False
        self.local_repo_exists = os.path.exists(local)
        self.remotes = []
        self.branches = []
        self.__active_branch = None
        if not (init_remote or self.local_repo_exists):
            raise Exceptions.GitRepoDoesNotExist(
                    "no local directory found, and no remote given")

        if not self.local_repo_exists:
            self.clone(init_remote)

        self.__build_remotes_list()
        self.__build_branches_list()

    @property
    def current_commit(self):
        return self.active_branch.commit

    @property
    def active_branch(self):
        return self.__active_branch

    def checkout(self, branch):
        if not branch in [branch.name for branch in self.branches]:
            raise Exceptions.GitBranchNotKnown("unknown branch: {}".format(branch))
        success, output, cmd = self.__run(["checkout",branch])
        if not success:
            raise Exceptions.GitCheckoutError("could not checkout branch: {}".format(branch))


    def clone(self, init_remote):
        success, output, cmd = self.__run(["clone","-v",init_remote, self.local], True)
        if not success:
            raise Exceptions.GitCloneError("\Output: {}\n\tCmd: {}".format(output, cmd), self.logger)

    def fetch(self, remote="origin"):
        if not remote in [remote.name for remote in self.remotes]:
            raise Exceptions.GitRemoteNotKnown("unknown remote: {}".format(remote))
        success, output, cmd = self.__run(["fetch","-v",remote], True)
        if not success:
            raise Exceptions.GitFetchError("\Output: {}\n\tCmd: {}".format(output, cmd), self.logger)

    def merge(self, branch="master"):
        if not branch in [branch.name for branch in self.branches]:
            raise Exceptions.GitBranchNotKnown("unknown branch: {}".format(branch))
        success, output, cmd = self.__run(["merge","-v",branch], True)
        if not success:
           raise Exceptions.GitMergeError("\Output: {}\n\tCmd: {}".format(output, cmd), self.logger)

    def pull(self, remote="origin", branch="master"):
        self.fetch(remote)
        self.merge(branch)


    def __build_remotes_list(self):
        success, output, cmd = self.__run(["remote","-v","show"])
        if not success:
            raise Exceptions.GitListRemoteError("\tOutput: {}\n\tCmd: {}".format(output, cmd), self.logger)
        lines = output.split("\n")
        for line in lines[:-1]:
            chunks = re.split('\s+', line)
            self.remotes.append(Remote(chunks[0],chunks[1],re.sub("[\(\)]","",chunks[2]),self))

    def __build_branches_list(self):
        success, output, cmd = self.__run(["branch","-v"])
        if not success:
            raise Exceptions.GitListRemoteError("\tOutput: {}\n\tCmd: {}".format(output, cmd), self.logger)
        lines = output.split("\n")
        for line in lines[:-1]:
            regular_branch = re.compile("\s+(?P<name>\S*)\s+(?P<SHA>[a-z0-9]{7})\s+(?P<commit>\S*)")
            active_branch = re.compile("\*\s+(?P<name>\S*)\s+(?P<SHA>[a-z0-9]{7})\s+(?P<commit>\S*)")
            m = re.match(active_branch, line)
            if m:
                self.__active_branch = Branch(m.group('name'), m.group("SHA"), m.group("commit"), self)
                self.branches.append(self.active_branch)
            else:
                m = re.match(regular_branch, line)
                if m:
                    self.branches.append(Branch(m.group('name'), m.group("SHA"), m.group("commit"), self))
##            chunks = re.split('\s+', line)
##            self.remotes.append(Remote(chunks[0],chunks[1],re.sub("[\(\)]","",chunks[2]),self))
##            for chunk in chunks:
##                print(chunk)


    @logged
    def __run(self, args, no_ch_dir=False):
        '''
        Runs an arbitrary git command
        '''

        cur_dir = os.getcwd()
        if not cur_dir == self.local and not no_ch_dir:
            os.chdir(self.local)
        cmd = [self.git_exe]
        for a in args:
            cmd.append(a)
##        cmd.append("-v")
        self.logger.info("running git command: {}".format(cmd[1:]))
        sep = "----------------------------------------------------"
        try:
            rtn = subprocess.check_output(
                        cmd,
                        shell=True,
                        universal_newlines=True,
                        stderr=subprocess.STDOUT
                        )
        except subprocess.CalledProcessError as e:
            cmd, code, output = e.cmd, e.returncode, e.output
            self.logger.error("output:\n{}\n{}\n{}".format(sep,output,sep))
            os.chdir(cur_dir)
            return False, e.output, e.cmd
        #TODO: parse return ?
        self.logger.info("output:\n{}\n{}\n{}".format(sep,rtn,sep))
        os.chdir(cur_dir)
        return True, rtn, cmd

    def __str__(self):
        return ("\n\t".join(["REPO:",
                    "Local: {}",
                    "Cloned: {}",
                    "Merged: {}",
                    "Remotes: \n\t\t{}",
                    "Branches: \n\t\t{}"
                    ])).format(
                    self.local,
                    self.cloned,
                    self.merged,
                    "\n\t\t".join(
                            [str(remote) for remote in self.remotes]
                                ),
                    "\n\t\t".join(
                            [str(branch) for branch in self.branches]
                                )
                    )


    @staticmethod
    def __get_git_exe():
        paths = ["./bobgit/bin/git.exe",
                "./bin/git.exe"
                ]
        for p in paths:
            if os.path.exists(p):
                return os.path.abspath(p)
        if not self.git:
            raise Exceptions.GitNotFound("Could not find git.exe in following paths: {}".format(
                        repr(paths)), self.logger)

class Branch():
    @logged
    def __init__(self, name, sha, commit, parent_repo):
        self.name = name
        self.sha = sha
        self.commit = commit
        self.repo = parent_repo

    def __str__(self):
        return "BRANCH:\n\tName: {}\n\tSHA: {}\n\tCommit: {}\n\tParent repo: {}".format(
                        self.name, self.sha, self.commit, self.repo.local
                        )

class Remote():
    @logged
    def __init__(self, name, address, _type, repo):
        self.repo = repo
        self.name = name
        self.address = address
        self.type = _type
        if not self.type in ["fetch","push"]:
            raise Exceptions.GitRemoteError("Unknown remote type: {}".format(self.type), self.logger)

    def __str__(self):
        return "REMOTE:\n\tName: {}\n\tAddress: {} ({})\n\tParent repo: {}".format(
                        self.name, self.address, self.type, self.repo.local
                        )