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
import config
try:
    from . import Exceptions
except (ImportError, SystemError):
    # noinspection PyUnresolvedReferences
    import Exceptions

from _logging._logging import logged, mkLogger, DEBUG

logger = mkLogger(__name__, DEBUG)


# noinspection PyUnresolvedReferences
class Repo():
    @logged
    def __init__(self, local, init_remote=None):
        self.logger.debug("création d'un repo:\n\t\tlocal: {}\n\t\tinit_remote: {}".format(local, init_remote))
        self.local = os.path.abspath(local)
        self.logger.debug("détection de l'existence du repository")
        self.initiliazed = os.path.exists(os.path.abspath(os.path.join(self.local, ".git")))
        self.local_repo_exists = os.path.exists(local)

        self.logger.debug("repository pré-existant: {}".format(self.initiliazed))
        self.git_exe = config.git_exe
        self.logger.debug("git exe: {}".format(self.git_exe))
        self.cloned = False
        self.fetched = False
        self.up_to_date = False
        self.merged = False
        self.remotes = []
        self.branches = []
        self.__active_branch = None
        if not (init_remote or self.local_repo_exists):
            raise Exceptions.GitRepoDoesNotExist(
                    "no local directory found, and no remote given")

        if not self.local_repo_exists:
            logger.debug("le repo local n'existe pas")
            self.clone(init_remote)
        elif not self.initiliazed:
            logger.debug("le repo local n'a pas encore été initialisé")
            self.init(init_remote)

        self.__build_remotes_list()
        self.__build_branches_list()

    @property
    def current_commit(self):
        logger.debug("commit courant: {}".format(self.__active_branch.commit))
        return self.active_branch.commit

    @property
    def active_branch(self):
        logger.debug("branche active: {}".format(self.__active_branch))
        return self.__active_branch

    # @logged
    # def init(self, init_remote):
    #     self.logger.debug("initialisation du repository")
    #     success, output, cmd = self.__run(["init"])
    #     if not success:
    #         raise Exceptions.GitInitError("\Output: {}\n\tCmd: {}".format(output, cmd), self.logger)
    #     success, output, cmd = self.__run(["add", ".", "-f"])
    #     if not success:
    #         raise Exceptions.GitInitError("\Output: {}\n\tCmd: {}".format(output, cmd), self.logger)
    #     success, output, cmd = self.__run(["remote", "add", "origin", init_remote])
    #     if not success:
    #         raise Exceptions.GitInitError("\Output: {}\n\tCmd: {}".format(output, cmd), self.logger)
    #     success, output, cmd = self.__run(["fetch", "origin"])
    #     if not success:
    #         raise Exceptions.GitInitError("\Output: {}\n\tCmd: {}".format(output, cmd), self.logger)
    #     success, output, cmd = self.__run(["reset", "--hard", "origin/master"])
    #     if not success:
    #         raise Exceptions.GitInitError("\Output: {}\n\tCmd: {}".format(output, cmd), self.logger)

    # def reset_to(self, ref="origin/master"):
    #     success, output, cmd = self.__run(["reset", "--hard", ref])
    #     if not success:
    #         raise Exceptions.GitResetError("\Output: {}\n\tCmd: {}".format(output, cmd), self.logger)

    def checkout(self, branch):
        self.logger.debug("checking out branch: {}".format(branch))
        if not branch in [branch.name for branch in self.branches]:
            raise Exceptions.GitBranchNotKnown("unknown branch: {}".format(branch))
        success, output, cmd = self.__run(["checkout",branch])
        if not success:
            raise Exceptions.GitCheckoutError("\Output: {}\n\tCmd: {}".format(output, cmd), self.logger)


    def clone(self, init_remote):
        self.logger.debug("cloning remote: {}".format(init_remote))
        success, output, cmd = self.__run(["clone","-v",init_remote, self.local], False)
        if not success:
            raise Exceptions.GitCloneError("\Output: {}\n\tCmd: {}".format(output, cmd), self.logger)

    def fetch(self, remote="origin"):
        self.logger.debug("fetching remote: {}".format(remote))
        if not remote in [remote.name for remote in self.remotes]:
            raise Exceptions.GitRemoteNotKnown("unknown remote: {}".format(remote))
        success, output, cmd = self.__run(["fetch","-v",remote])
        if not success:
            raise Exceptions.GitFetchError("\Output: {}\n\tCmd: {}".format(output, cmd), self.logger)

    def remote_add(self, name, remote):
        self.logger.debug("adding remote: {} ---> {}".format(name, remote))
        success, output, cmd = self.__run(["remote","add",name, remote])
        if not success:
            raise Exceptions.GitRemoteAddError("\Output: {}\n\tCmd: {}".format(output, cmd), self.logger)

    def merge(self, branch="master"):
        self.logger.debug("merging branch: {}".format(branch))
        if not branch in [branch.name for branch in self.branches]:
            raise Exceptions.GitBranchNotKnown("unknown branch: {}".format(branch))
        success, output, cmd = self.__run(["merge","-v",branch])
        if not success:
           raise Exceptions.GitMergeError("\Output: {}\n\tCmd: {}".format(output, cmd), self.logger)

    def pull(self, remote="origin", branch="master"):
        self.logger.debug('pulling branch "{}" from remote "{}"'.format(branch, remote))
        if not branch in [branch.name for branch in self.branches]:
            raise Exceptions.GitBranchNotKnown("unknown branch: {}".format(branch))
        self.checkout(branch)
        self.fetch(remote)
        success, output, cmd = self.__run(["pull",remote,branch])
        if not success:
           raise Exceptions.GitMergeError("\Output: {}\n\tCmd: {}".format(output, cmd), self.logger)
        # self.fetch(remote)
        # self.merge(branch)


    def __build_remotes_list(self):
        self.logger.debug("construction de la liste des remotes")
        success, output, cmd = self.__run(["remote","-v","show"])
        if not success:
            raise Exceptions.GitListRemoteError("\tOutput: {}\n\tCmd: {}".format(output, cmd), self.logger)
        lines = output.split("\n")
        for line in lines[:-1]:
            self.logger.debug("découverte d'un remote")
            chunks = re.split('\s+', line)
            self.remotes.append(Remote(chunks[0],chunks[1],re.sub("[\(\)]","",chunks[2]),self))

    def __build_branches_list(self):
        self.logger.debug("construction de la liste des branches")
        success, output, cmd = self.__run(["branch","-v"])
        if not success:
            raise Exceptions.GitListRemoteError("\tOutput: {}\n\tCmd: {}".format(output, cmd), self.logger)
        lines = output.split("\n")
        for line in lines[:-1]:
            regular_branch = re.compile("\s+(?P<name>\S*)\s+(?P<SHA>[a-z0-9]{7})\s+(?P<commit>\S*)")
            active_branch = re.compile("\*\s+(?P<name>\S*)\s+(?P<SHA>[a-z0-9]{7})\s+(?P<commit>\S*)")
            m = re.match(active_branch, line)
            if m:
                self.logger.debug("découvert de la branche active")
                self.__active_branch = Branch(m.group('name'), m.group("SHA"), m.group("commit"), self)
                self.branches.append(self.active_branch)
            else:
                self.logger.debug("découverte d'une branche inactive")
                m = re.match(regular_branch, line)
                if m:
                    self.branches.append(Branch(m.group('name'), m.group("SHA"), m.group("commit"), self))
##            chunks = re.split('\s+', line)
##            self.remotes.append(Remote(chunks[0],chunks[1],re.sub("[\(\)]","",chunks[2]),self))
##            for chunk in chunks:
##                print(chunk)


    @logged
    def __run(self, args, ch_dir=True):
        """
        Runs an arbitrary git command
        """
        self.logger.debug("lancement de la commande git: {}".format(args))
        if ch_dir:
            cur_dir = os.getcwd()
            switch_dir(self.local)
        # if not cur_dir == self.local and not no_ch_dir:
        #     self.logger.debug("switch du répertoire courant vers: {}".format(self.local))
        #     os.chdir(self.local)
        #     if not os.getcwd() == self.local:
        #         raise Exceptions.GitRunError("Echec du changement de répertoire courant")
        cmd = [self.git_exe]
        for a in args:
            cmd.append(a)
        self.logger.debug("lancement de la commande Git: {}".format(cmd[1:]))
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
        self.logger.debug("output:\n{}\n{}\n{}".format(sep,rtn,sep))
        self.logger.debug
        if ch_dir:
            switch_dir(cur_dir)
        self.logger.debug("la commande Git a été exécutée avec succès")
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


    # @staticmethod
    # def __get_git_exe():
    #     paths = ["./bobgit/bin/git.exe",
    #             "./bin/git.exe"
    #             ]
    #     for p in paths:
    #         if os.path.exists(p):
    #             return os.path.abspath(p)
    #     if not self.git:
    #         raise Exceptions.GitNotFound("Could not find git.exe in following paths: {}".format(
    #                     repr(paths)), self.logger)

class Branch():
    @logged
    def __init__(self, name, sha, commit, parent_repo):
        self.name = name
        self.sha = sha
        self.commit = commit
        self.repo = parent_repo
        self.logger.debug("création d'une nouvelle branche\n{}".format(str(self)))

    def __str__(self):
        return "BRANCH:\n\tName: {}\n\tSHA: {}\n\tCommit: {}\n\tParent repo: {}".format(
                        self.name, self.sha, self.commit, self.repo.local
                        )

# noinspection PyUnresolvedReferences
class Remote():
    @logged
    def __init__(self, name, address, _type, repo):
        self.repo = repo
        self.name = name
        self.address = address
        self.type = _type
        if not self.type in ["fetch","push"]:
            raise Exceptions.GitRemoteError("Unknown remote type: {}".format(self.type), self.logger)
        self.logger.debug("création d'un remote\n{}".format(str(self)))

    def __str__(self):
        return "REMOTE:\n\tName: {}\n\tAddress: {} ({})\n\tParent repo: {}".format(
                        self.name, self.address, self.type, self.repo.local
                        )

def switch_dir(new_dir):
    logger.debug("changement de répertoire courant\nrépertoire courant: {}\nrépertoire cible: {}".format(os.getcwd(), new_dir))
    if os.getcwd() == new_dir:
        logger.debug("le répertoire courant et la cible sont identiques")
        return True
    logger.debug("changement de répertoire courant")
    os.chdir(new_dir)
    if os.getcwd() == new_dir:
        logger.debug("changement de répertoire réussi")
        return True
    raise Exceptions.GitRunError("échec du changement de répertoire courant")
