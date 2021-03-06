# -*- coding: UTF-8 -*-
__author__ = 'bob'

import subprocess
import os
import re
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
        self.logger.debug("création d'un objet repo:\n\t\tlocal: {}\n\t\tinit_remote: {}".format(local, init_remote))
        self.cloned = False
        self.fetched = False

        self.local = os.path.abspath(local)
        self.local_repo_exists = os.path.exists(local)

        self.remotes = []
        self.branches = []
        self.__active_branch = None
        if not (init_remote or self.local_repo_exists):
            raise Exceptions.GitRepoDoesNotExist(
                    "no local directory found, and no remote given")

        if not self.local_repo_exists:
            logger.debug("le repo local n'existe pas, lancement du clonage")
            self.clone(init_remote)

        self.__build_remotes_list()
        self.__build_branches_list()
        logger.debug("mise à jour du repository (pulling)")
        self.pull()



    @property
    def current_commit(self):
        logger.debug("commit courant: {}".format(self.__active_branch.commit))
        return self.active_branch.commit

    @property
    def active_branch(self):
        logger.debug("branche active: {}".format(self.__active_branch))
        return self.__active_branch

    def checkout(self, branch):
        self.logger.debug("checking out branch: {}".format(branch))
        if self.__active_branch.name == branch:
            self.logger.debug("ce repo est déjà sur la branche demandée, on passe")
            return self
        if not branch in [branch.name for branch in self.branches]:
            raise Exceptions.GitBranchNotKnown("unknown branch: {}".format(branch))
        success, output, cmd = self.__run(["checkout",branch])
        if not success:
            raise Exceptions.GitCheckoutError("\Output: {}\n\tCmd: {}".format(output, cmd), self.logger)
        return self


    def clone(self, init_remote):
        self.logger.debug("clonage du remote: {}".format(init_remote))
        if self.cloned:
            self.logger.debug("ce repo a déjà été cloné")
        self.cloned = True
        success, output, cmd = self.__run(["clone","-v",init_remote, self.local], False)
        if not success:
            raise Exceptions.GitCloneError("\Output: {}\n\tCmd: {}".format(output, cmd), self.logger)
        return self

    def fetch(self, remote="origin"):
        self.logger.debug("fetch du remote: {}".format(remote))
        if self.fetched:
            self.logger.debug("ce repo a déjà été fetché")
            return self
        self.fetched = True
        if not remote in [remote.name for remote in self.remotes]:
            raise Exceptions.GitRemoteNotKnown("remote inconnu: {}".format(remote))
        success, output, cmd = self.__run(["fetch","-v",remote])
        if not success:
            raise Exceptions.GitFetchError("\Output: {}\n\tCmd: {}".format(output, cmd), self.logger)
        return self

    def pull(self, remote="origin", branch="master"):
        self.logger.debug('pull de la branche "{}" à partir du remote "{}"'.format(branch, remote))
        self.logger.debug("vérification de l'existence de la branche dans le repo local")
        if not branch in [branch.name for branch in self.branches]:
            self.logger.debug("la branche n'existe pas (encore), fetch pour vérifier")
            self.fetch(remote=remote).pull(remote=remote, branch=branch)
            return self
        self.checkout(branch).fetch(remote)
        self.logger.debug("pull du repo")
        success, output, cmd = self.__run(["pull",remote,branch])
        if not success:
           raise Exceptions.GitPullError("\Output: {}\n\tCmd: {}".format(output, cmd), self.logger)
        return self


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


    @logged
    def __run(self, args, ch_dir=True):
        """
        Runs an arbitrary git command
        """
        self.logger.debug("lancement de la commande git: {}".format(args))
        if ch_dir:
            cur_dir = os.getcwd()
            switch_dir(self.local)
        cmd = [config.git_exe]
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
    logger.debug("changement de répertoire courant\n\trépertoire courant: {}\n\trépertoire cible: {}".format(os.getcwd(), new_dir))
    if os.getcwd() == new_dir:
        logger.debug("le répertoire courant et la cible sont identiques, retour")
        return True
    logger.debug("changement de répertoire courant nécessaire")
    os.chdir(new_dir)
    if os.getcwd() == new_dir:
        logger.debug("changement de répertoire réussi !")
        return True
    raise Exceptions.GitRunError("échec du changement de répertoire courant")
