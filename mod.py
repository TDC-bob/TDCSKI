# coding=utf-8
__author__ = 'bob'

import os
import re
import shutil
import bobgit.git as git
from hashlib import md5 as MD5
from _logging._logging import mkLogger, DEBUG, logged
import config


logger = mkLogger(__name__, DEBUG)


try:
    conf = config.Config()
except:
    logger.error("votre fichier de configuration est corrompu, supprimez le et j'en réinstallerai un nouveau")
    input()
    exit(1)

class Mod():
    @logged
    def __init__(self, name, _type, parent_dir, args):
        self.logger.debug("création d'un Mod")
        # try:
        #     self.conf = config.Config()
        # except:
        #     logger.error("votre fichier de configuration est corrompu, supprimez le et j'en réinstallerai un nouveau")
        #     input()
        #     exit(1)
        self.__name = name
        self.logger.debug("nom: {}".format(self.__name))
        self.__type = _type
        self.logger.debug("type: {}".format(self.__type))
        self.__local = "{}/{}".format(parent_dir, self.__name)
        self.logger.debug("dossier local: {}".format(self.__local))
        self.__remote = args["remote"]
        self.logger.debug("remote: {}".format(self.__remote))
        self.logger.debug("initialisation du repository dans le dossier local")
        self.__repo = git.Repo(self.__local, self.__remote)
        self.__branch = "master"
        for arg in args:
            if arg in ["remote"]:
                continue
            elif arg in ["branch"]:
                self.logger.debug("paramètre branche trouvé: {}".format(args[arg]))
                self.__branch = args[arg]
                self.logger.debug("checkout du repository")
                self.__repo.checkout(self.__branch)
            elif arg in ["desc"]:
                self.logger.debug("paramètre descritpion trouvé: {}".format(args[arg]))
                self.__desc = args[arg]
            elif arg in ["version"]:
                self.logger.debug("paramètre version trouvé: {}".format(args[arg]))
                self.__version = args[arg]
            else:
                self.error("paramètre inconnu trouvé: {} \t\t Valeur: {}".format(arg, args[arg]))
                input()
                exit(1)

        self.logger.debug("écriture du fichier de configuration")
        if not conf.set_or_create(self.__type,  self.__name, "path", self.__local):
            self.logger.error("erreur lors de l'écriture du nom")
            input()
            exit(1)
        if not conf.set_or_create(self.__type, self.__name, "desc", self.__desc):
            self.logger.error("erreur lors de l'écriture de la description")
            input()
            exit(1)
        if not conf.set_or_create(self.__type, self.__name, "version", self.__version):
            self.logger.error("erreur lors de l'écriture de la description")
            input()
            exit(1)
        if not conf.set_or_create(self.__type, self.__name, "branch", self.__branch):
            self.logger.error("erreur lors de l'écriture de la description")
            input()
            exit(1)
        conf.create(self.__type, self.__name, "installed", False)


        self.buil_files_list()

    @logged
    def buil_files_list(self):
        self.logger.debug("construction de la liste des fichiers")
        self.__files = []
        if os.path.exists("{}/DCS".format(self.__local)):
            for root, dirs, files in os.walk("{}/DCS".format(self.__local)):
                for file in files:
                    if file == '.gitignore':
                        self.logger.debug("fichier .gitignore trouvé, on zappe")
                        continue
                    self.logger.debug("fichier trouvé")
                    full_path = os.path.abspath(os.path.join(root, file))
                    self.logger.debug("chemin complet: {}".format(full_path))
                    rel_path = full_path.replace(os.path.abspath(self.__local), "")
                    self.logger.debug("chemin relatif {}".format(rel_path))
                    self.__files.append(ModFile(full_path,rel_path, self))
        if os.path.exists("{}/SAVED_GAMES".format(self.__local)):
            for root, dirs, files in os.walk("{}/SAVED_GAMES".format(self.__local)):
                for file in files:
                    if file == '.gitignore':
                        self.logger.debug("fichier .gitignore trouvé, on zappe")
                        continue
                    self.logger.debug("fichier trouvé")
                    full_path = os.path.abspath(os.path.join(root, file))
                    self.logger.debug("chemin complet: {}".format(full_path))
                    rel_path = full_path.replace(os.path.abspath(self.__local), "")
                    self.logger.debug("chemin relatif {}".format(rel_path))
                    self.__files.append(ModFile(full_path,rel_path, self))

    @property
    def should_be_installed(self):
        rtn = conf.get(self.type, self.name, "installed")
        self.logger.debug("test: ce mod doit-il être installé ? Réponse: {}".format(rtn))
        # if conf.get(self.type, self.name, "installed") == "True":
        #     self.logger.debug("réponse: oui")
        #     return True
        # self.logger.debug("réponse: non")
        return rtn

    @property
    def desc(self):
        return self.__desc

    @property
    def version(self):
        return self.__version

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
        self.logger.debug("pull du repository local")
        self.__repo.pull(self.remote, self.branch)
        self.buil_files_list()

    @logged
    def check(self):
        if self.should_be_installed:
            self.install()
        else:
            self.uninstall()

    @logged
    def uninstall(self):
        logger.debug("désinstallation du {}: {}".format(self.__type, self.__name))
        if self.should_be_installed:
            logger.debug("ce mod devrait être installé, annulation")
            return False
        for file in self.__files:
            logger.debug("ce mod devrait être désinstallé")
            file.uninstall()
        return True

    @logged
    def install(self):
        logger.debug("installation du {}: {}".format(self.__type, self.__name))
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
    @logged
    def __init__(self, full_path, rel_path, parent_mod):
        self.logger.debug("création d'un fichier de mod/skin")
        self.__full_path = os.path.abspath(full_path)
        self.logger.debug("chemin complet: {}".format(self.__full_path))
        self.__rel_path = os.path.normpath(rel_path)
        self.logger.debug("chemin relatif: {}".format(self.__rel_path))
        self.__basename = os.path.normpath(os.path.basename(self.__rel_path))
        self.logger.debug("basename: {}".format(self.__basename))
        self.__parent = parent_mod
        self.logger.debug("mod/skin parent: {}".format(self.__parent.name))
        strip = re.compile(".*{}".format(self.__parent.name))
        self.__install_to = re.sub(strip, '', self.__full_path).lstrip('\\')
        if self.__install_to[:11] == "SAVED_GAMES":
            self.__install_to = self.__install_to.lstrip("SAVED_GAMES")
            self.__install_to = "{}{}".format(config.SaveGames_path, self.__install_to)
            self.__install_to = os.path.normpath((self.__install_to))
        elif self.__install_to[:3] == "DCS":
            self.__install_to = self.__install_to.lstrip("DCS")
            self.__install_to = "{}{}".format(config.DCS_path, self.__install_to)
            self.__install_to = os.path.normpath((self.__install_to))
        self.logger.debug("chemin d'installation du fichier: {}".format(self.__install_to))

        self.__safe_to_delete = False
        self.__config_file = "{}.tdcski".format(self.__install_to)
        self.__config = config.Config(self.__config_file, False)
        self.logger.debug("config: {}".format(self.__config))
        self.__backup = "{}.tdcski.backup".format(self.__install_to)
        self.logger.debug("backup: {}".format(self.__backup))
        self.logger.debug("ce fichier sera installé dans: {}".format(self.__install_to))

    @property
    def config(self):
        return self.__config

    @property
    def safe_to_delete(self):
        return self.__safe_to_delete

    @property
    def __local_copy_exists(self):
        logger.debug("une copie locale existe déjà: {}".format(os.path.exists(self.__install_to)))
        return os.path.exists(self.__install_to)

    @property
    def __local_copy_identical(self):
        if not self.__local_copy_exists:
            return False
        logger.debug("la copie locale est identique : {}".format(compare_files(self.full_path, self.__install_to)))
        return compare_files(self.full_path, self.__install_to)

    @property
    def is_installed(self):
        return os.path.exists(self.__config_file)

    @property
    def should_be_installed(self):
        return self.__parent.should_be_installed

    @property
    def different(self):
        return not self.__local_copy_identical

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
    def uninstall(self):
        self.logger.info("Désinstallation du fichier: {}".format(self.__basename))
        if self.__parent.should_be_installed:
            logger.info("Annulation de la désinstallation, le mod parent devrait être installé")
            return
        if not os.path.exists(self.__config_file):
            logger.error("Ce fichier n'est pas installé, annulation de la désinstallation")
            return
        self.logger.debug("suppression du fichier configuration")
        os.remove(self.__config_file)
        if os.path.exists(self.__config_file):
            self.logger.error("échec de la suppression du fichier configuration")
            input()
            exit(1)
        if not os.path.exists((self.__backup)):
            self.logger.debug("aucun fichier de backup présent")
            if not os.path.exists(self.__safe_to_delete):
                self.logger.error("safe_to_delete n'est pas présent non plus, dans le doute, je quitte")
                return
        self.logger.debug("suppression du fichier local")
        os.remove(self.__install_to)
        if os.path.exists(self.__install_to):
            self.logger.error("échec de la suppression du fichier local")
            input()
            exit(1)
        if os.path.exists((self.__backup)):
            self.logger.debug("un backup existe pour ce fichier, restauration")
            shutil.copy2(self.__backup, self.__install_to)
            if not compare_files(self.__backup, self.__install_to):
                self.logger.error("le backup et la copie ne correspondent pas, échec de la restauration")
                input()
                exit(1)


    @logged
    def install(self):
        self.logger.info("Installation du fichier: {}  --->   {}".format(self.__full_path, self.__install_to))

        if self.__parent.should_be_installed:
            if not self.__local_copy_identical:
                self.logger.debug("ce fichier va devoir être installé")
                self.logger.debug("création des répertoires de destination")
                os.makedirs(os.path.dirname(self.__install_to), exist_ok=True)
                self.logger.debug("création du backup si nécessaire")
                if os.path.exists(self.__install_to):
                    self.logger.debug("le fichier local existe déjà")
                    if not os.path.exists(self.__backup):
                        self.logger.debug("aucun backup n'a été trouvé, création")
                        shutil.copy2(self.__install_to, self.__backup)
                    else:
                        self.logger.debug("un backup existe déjà")
                else:
                    self.__safe_to_delete = True
                    # self.logger.debug("le fichier local n'existe pas, écriture de safe_to_delete")
                    # with open(self.__safe_to_delete, mode="w") as file:
                    #     file.write(str(self.__parent.version))
                    self.logger.debug("pas de fichier local trouvé, aucun backup nécessaire, fichier noté 'safe_to_delete'")
                self.logger.debug("création du fichier configuration")
                self.__config.set_or_create("install", "safe_to_delete", self.__safe_to_delete)
                self.__config.set_or_create("install", "parent",self.__parent.name)
                self.__config.set_or_create("install", "version",str(self.__parent.version))
                self.__config.set_or_create("install","description",self.__parent.desc)
                # with open(self.__dummy,mode="w") as file:
                #     file.write(str(self.__parent.version))
                if not os.path.exists(self.__config_file):
                    self.logger.error("echec de la création du fichier configuration")
                    input()
                    exit(1)
                self.logger.info("Copie: {}  --->   {}".format(self.__full_path, self.__install_to))
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
