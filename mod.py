# coding=utf-8
__author__ = 'bob'

import os
import re
from config import Config
import shutil
import bobgit.git as git
from hashlib import md5 as MD5
from _logging._logging import mkLogger, DEBUG, logged


logger = mkLogger(__name__, DEBUG)

conf = Config()

class Mod():
    def __init__(self, name, _type, parent_dir, args):
        self.__name = name
        self.__type = _type
        self.__local = "{}/{}".format(parent_dir, self.__name)
        self.__remote = args["remote"]
        self.__repo = git.Repo(self.__local, self.__remote)
        self.__branch = "master"
        for arg in args:
            if arg in ["remote"]:
                continue
            elif arg in ["branch"]:
                self.__branch = args[arg]
                self.__repo.checkout(self.__branch)
            elif arg in ["desc"]:
                self.desc = args[arg]
            elif arg in ["version"]:
                self.version = args[arg]
            else:
                print("TODO: {}".format(arg))
        self.buil_files_list()


        conf.create(self.__type,  self.__name, "path", self.__local)
        conf.create(self.__type, self.__name, "desc", self.desc)
        conf.create(self.__type, self.__name, "installed", False)

    def buil_files_list(self):
        self.__files = []
        for root, dirs, files in os.walk(self.__local):
            if '.git' in dirs:
                dirs.remove('.git')
            for file in files:
                if file == '.gitignore':
                    continue
                full_path = os.path.join(root, file)
                rel_path = full_path.replace(os.path.abspath(self.__local), "")
                self.__files.append(ModFile(full_path,rel_path, self))

    @property
    def should_be_installed(self):
        return bool(conf.get(self.type, self.name, "installed"))

    @property
    def file_count(self):
        return len(self.__files)

    @property
    def files(self):
        return self.__files

    @property
    def repo(self):
        return self.__repo

    @property
    def name(self):
        return self.__name

    @property
    def type(self):
        return self.__type

    @property
    def repo_path(self):
        return self.__local

    @property
    def remote(self):
        return self.__remote

    @property
    def repo(self):
        return self.__repo

    @property
    def branch(self):
        return self.__branch

    def pull_repo(self):
        self.__repo.pull()
        self.buil_files_list()

    def install(self):
        logger.debug("installation du {}: {}".format(self.__type, self.__name))
        logger.warn("should_be_installed: {}".format(self.should_be_installed))
        logger.warn("should_be_installed: {}".format(type(self.should_be_installed)))
        if not self.should_be_installed:
            logger.debug("ce mod ne devrait pas être installé")
            return False
        for file in self.__files:
            logger.debug("ce mod devrait être installé")
            file.install()
        return True

    def __str__(self):
        return "Name: {}\nRemote: {}\nLocal: {}\nRepo: {}".format(self.__name, self.__remote, self.__local,repr(self.__repo))


class ModFile():
    def __init__(self, full_path, rel_path, parent_mod):
        self.__full_path = os.path.abspath(full_path)
        self.__rel_path = os.path.normpath(rel_path)
        self.__basename = os.path.normpath(os.path.basename(self.__rel_path))
        self.__parent = parent_mod
        strip = re.compile(".*{}".format(self.__parent.name))
        self.__install_to = re.sub(strip, '', self.__full_path).lstrip('\\')
        if self.__install_to[:11] == "SAVED_GAMES":
            self.__install_to = self.__install_to.lstrip("SAVED_GAMES")
            self.__install_to = "{}{}".format(conf.get("general","saved_games_path"), self.__install_to)
            self.__install_to = os.path.normpath((self.__install_to))
        if self.__install_to[:3] == "DCS":
            self.__install_to = self.__install_to.lstrip("DCS")
            self.__install_to = "{}{}".format(conf.get("general","dcs_path"), self.__install_to)
            self.__install_to = os.path.normpath((self.__install_to))

    @property
    def __local_copy_exists(self):
        logger.debug("local copy exists: {}".format(os.path.exists(self.__install_to)))
        return os.path.exists(self.__install_to)

    @property
    def __local_copy_identical(self):
        if not self.__local_copy_exists:
            return False
        logger.debug("local copy identical : {}".format(compare_files(self.full_path, self.__install_to)))
        return compare_files(self.full_path, self.__install_to)

    @property
    def should_be_installed(self):
        return self.__parent.should_be_installed

    @property
    def different(self):
        return not self.__local_copy_identical

    @property
    def installed(self):
        return self.__local_copy_identical

    @property
    def full_path(self):
        return self.__full_path

    @property
    def rel_path(self):
        return self.__rel_path

    @property
    def basename(self):
        return self.__basename

    @logged
    def install(self):
        self.logger.info("Installation du fichier: {}  --->   {}".format(self.__full_path, self.__install_to))

        if self.__parent.should_be_installed:
            if not self.installed:
                self.logger.debug("création des répertoires de destination")
                os.makedirs(os.path.dirname(self.__install_to), exist_ok=True)
                self.logger.debug("création du backup si nécessaire")
                if not backup(self.__install_to):
                    self.logger.error("Impossible de faire le backup")
                    return False
                self.logger.info("Copying: {}  --->   {}".format(self.__full_path, self.__install_to))
                print("Copying: {}  --->   {}".format(self.__full_path, self.__install_to))
                shutil.copy2(self.__full_path, self.__install_to)
                return True
            else:
                self.logger.debug("le fichier est déjà installé")
        else:
            self.logger.error("le mod parent ne devrait pas être installé, donc ce fichier non plus")

    def __str__(self):
        return "Full path: {}\n" \
               "Relative path: {}\n" \
               "Basename: {}\n"\
                "Install to: {}\n".format(self.__full_path,self.__rel_path,self.__basename, self.__install_to)

def compare_files(file1, file2):
    md5_1 = md5(file1)
    md5_2 = md5(file2)
    logger.debug("MD5_1: {} \nMD5_2: {}".format(md5_1, md5_2))
    return  md5_1 == md5_2

def md5(file):
    _md5 = MD5()
    with open(file,'rb') as f:
        for chunk in iter(lambda: f.read(128), b''):
             _md5.update(chunk)
    return _md5.digest()


def backup(file):
    logger.info("backup du fichier: {}".format(file))
    if not os.path.exists(file):
        logger.debug("le fichier n'existe pas, srien à sauvegarder")
        return True
    dest = "{}.tdcski.original".format(file)
    logger.debug("la destination du backup sera: {}".format(dest))
    shutil.copy2(file, dest)
    if not os.path.exists(dest):
        logger.error("la copie s'est mal passée")
        return False
    logger.debug("la copie s'est bien passée")
    return True