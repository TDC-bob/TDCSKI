# -*- coding: utf-8 -*-
__author__ = 'bob'

import subprocess
import os
import re
import tdcski.config_handler
from tdcski._logging import logged, mkLogger, DEBUG

logger = mkLogger(__name__, DEBUG)

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

# noinspection PyUnresolvedReferences
class Repo():
    @logged
    def __init__(self, local, init_remote=None, branch="master", update=False):
        self.logger.debug("création d'un objet repo:\n\t\tlocal: {}\n\t\tinit_remote: {}\n\tOnline: {}".format(local, init_remote, update))

        self.__local = os.path.abspath(local)
        self.local_repo_exists = os.path.exists(local)

        self.remotes = []
        self.branches = []
        self.__active_branch = None
        if not (init_remote or self.local_repo_exists):
            raise Exceptions.GitRepoDoesNotExist(
                    "le repository n'existe pas en local , et aucun repo distant n'a été donné pour initialisation")

        if self.local_repo_exists:
            self.logger.debug("le repository local existe")
            if not os.path.exists(os.path.join(self.__local, ".git")) and not dir_is_empty(self.__local):
                raise Exceptions.GitError("le dossier local existe déjà, mais ce n'est pas un repo, et il n'est pas vide")
            if update:
                logger.debug("mise à jour du repository")
                self.update(branch)
        else:
            self.logger.debug("le repository local n'existe pas")
            if not update:
                raise Exceptions.GitError("le programme tourne en mode offline mais le repository local n'existe pas", self.logger)
            logger.debug("initialisation du repo local sur base de: {}".format(init_remote))
            self.init(init_remote, branch)

        self.__build_branches_list()
        self.__build_remotes_list()
        self.logger.debug("branche active: {}".format(self.active_branch))
        self.logger.debug("dernier commit: {}".format(self.current_commit))

    @property
    def local(self):
        return self.__local

    @property
    def current_commit(self):
        self.logger.debug("commit courant: {}".format(self.__active_branch.commit))
        return self.active_branch.commit

    @property
    def active_branch(self):
        self.logger.debug("branche active: {}".format(self.__active_branch))
        return self.__active_branch

    @logged
    def init(self, remote, branch):

        self.logger.debug("initialisation du repository\ncréation du répertoire si nécessaire")
        os.makedirs(self.__local)
        if not dir_is_empty(self.__local):
            raise Exceptions.GitInitError("tentative d'initialisation d'un repository non vide: {}".format(self.__local), self.logger)

        self.logger.debug("initialisation du répertoire en repository Git")
        success, output, cmd = self.__run(["init"])
        if not success:
            raise Exceptions.GitInitError("\Output: {}\n\tCmd: {}".format(output, cmd), self.logger)

        self.logger.debug("ajout et fetch du repository distant dans le répertoire local")
        success, output, cmd = self.__run(["remote", "add", "-t", branch, "-f", "origin", remote]) # "-f" switche makes Git fetch the remote immediately after the "remote add" command
        if not success:
            raise Exceptions.GitAddRemoteError("\Output: {}\n\tCmd: {}".format(output, cmd), self.logger)

        self.logger.debug("checkout de la branche en local")
        success, output, cmd = self.__run(["checkout", branch])
        if not success:
            raise Exceptions.GitCheckoutError("\Output: {}\n\tCmd: {}".format(output, cmd), self.logger)


        self.logger.debug("le répertoire a été initialisé avec succès")
        return self

    @logged
    def update(self, branch="master"):

        self.logger.debug("checkout de la branche en local")
        success, output, cmd = self.__run(["checkout", branch])
        if not success:
            raise Exceptions.GitFetchError("\Output: {}\n\tCmd: {}".format(output, cmd), self.logger)

        self.logger.debug("fetch de la branche distante: {}".format(branch))
        success, output, cmd = self.__run(["fetch", "-v", "origin", "{}:remotes/origin/{}".format(branch, branch)])
        if not success:
            raise Exceptions.GitFetchError("\Output: {}\n\tCmd: {}".format(output, cmd), self.logger)

        self.logger.debug("reset sur base du repo distant")
        success, output, cmd = self.__run(["reset", "--hard", "origin"])
        if not success:
            raise Exceptions.GitFetchError("\Output: {}\n\tCmd: {}".format(output, cmd), self.logger)

        self.logger.debug("le repository a été mis à jour avec succès")
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
        if ch_dir:
            cur_dir = os.getcwd()
            switch_dir(self.__local)
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
                    "Remotes: \n\t\t{}",
                    "Branches: \n\t\t{}"
                    ])).format(
                    self.__local,
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
        self.logger.debug("création d'un nouvel objet branche\n{}".format(str(self)))

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
        self.logger.debug("création d'un nouvel objet remote\n{}".format(str(self)))

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
    raise GitRunError("échec du changement de répertoire courant")

def dir_is_empty(path):
    return os.listdir(path)==[]