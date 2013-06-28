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


import logging, makeTemp, mission
from _logging._logging import mkLogger, logged
logger = mkLogger(__name__, logging.INFO )

##from os.path import isfile, exists, join, abspath, dirname, basename
import os, shutil, zipfile, Exceptions
##from os import remove, mkdir, rename, listdir
##from shutil import copyfile, rmtree
##from os.path import exists, basename, dirname
##import string, zipfile, Exceptions

class MizFile:
    """
    Représente un fichier *.miz

    Permet de décompresser, manipuler puis recompresser le fichier pour édition
    Effectue quelques vérifications de bases quant à l'intégrité du fichier *.miz
    """
    @logged
    def __init__(self, path_to_file, temp_dir=None):
        self.logger.info("Initializing MizFile({},{})".format(path_to_file,temp_dir))
        self.path = path_to_file
        self.basename = os.path.basename(path_to_file)
        split = os.path.splitext(self.basename)
        self.filename = split[0]
        self.ext = split[1]

        if self.ext != ".miz":
            self.logger.warning("extention for this file is \"{}\", where \".miz\" was expected")

        self.logger.debug("Basename: {}".format(self.basename))
        self.folder = os.path.dirname(path_to_file)
        self.logger.debug("Path to file: {}".format(self.folder))

        if temp_dir == None:
            self.temp_dir = makeTemp.random_folder(self.folder, prefix="".join([self.filename,"_"]))
        else:
            self.temp_dir = temp_dir
        self.logger.debug("temporary directory for this MIZ will be: {}".format(self.temp_dir))
        self.flat = False
        self.checked = False

    @logged
    def check(self):
        """
        Vérifie:
            1° l'existence
            2° l'intégrité du fichier ZIP (MIZ)
        """
        self.logger.info("runing sanity checks")
        self.logger.debug("checking for existence ...")
        if not os.path.exists(self.path):
            raise Exceptions.FileDoesNotExist("File does not exist",self.path, self.logger)
##            raise Exceptions.FileDoesNotExist(self.path,self.logger)
        self.logger.debug("files exists")
        self.logger.debug("checking for ZIP consistency ...")
        try:
            with zipfile.ZipFile(self.path) as zip_file:
                corruptedFile = zip_file.testzip()
                if corruptedFile:
                    raise zipfile.BadZipFile
        except zipfile.BadZipFile:
            raise Exceptions.InvalidMizFile(self.path, self.logger, "le fichier MIZ est corrompu")
        except PermissionError:
            raise Exceptions.PermissionError("Impossible d'accéder au fichier", "Erreur fatale pendant la décompression du fichier suivant: {} (peut-être s'agit-il d'un dossier ?)".format(self.path))
        self.logger.debug("ZIP format is correct")
        self.logger.info("all sanity checks OK")
        self.checked = True
        return self

    @logged
    def decompact(self):
        """
        Extrait les fichiers contenus dans le fichier MIZ

        Les fichiers sont extraits dans un répertoire temporaire (self.temp_dir)
        se trouvant (par défaut) dans le même répertoire que le fichier MIZ
        """
        with zipfile.ZipFile(self.path) as zip_file:
            try:
                zip_content = zip_file.infolist()
                self.files_in_zip = [f.filename for f in zip_content] # files_in_zip = list(str)
                self.logger.debug("contenu du fichier zip: {}".format(", ".join(self.files_in_zip)))
                for item in zip_content:
                    # Je n'utilise pas ZipFile.extractall() parce que ça pourrait potentiellement être une faille de sécurité
                    # (extraction en dehors du répertoire qui m'intéresse)
                    try:
                        zip_file.extract(item, self.temp_dir)
                        self.logger.debug('extraction OK: {}'.format(item.filename))
                    except RuntimeError:
                        raise Exceptions.CouldNotExtract(self.path, item, self.logger)
            except zipfile.BadZipFile:
                raise Exceptions.Error("erreur lors de la décompression du fichier MIZ","Chemin vers le fichier: {}".format(self.path), self.logger)
        self.logger.debug("parsing content ...")
        filelist = os.listdir(self.temp_dir)
        for f in ["mission","options","warehouses"]:
            if not f in filelist:
                raise Exceptions.Error("Fichier manquant", 'Impossible de trouver le fichier {} après extraction ({})'.format(f, self.path))
        self.logger.debug("ZIP file content: {}".format(str(filelist)))
        self.flat = True
        return self

    @logged
    def recompact(self, folder_to_extract_to=None, out_zip_file=None):
        """
        Recrée un fichier MIZ sur base du contenu du répertoire temporaire

        La destination par défaut est un dossier TDCMEME créé juste à côté du
        fichier MIZ originel
        """
        # check for TDCMEME folder existence
        if not folder_to_extract_to:
            folder_to_extract_to = os.path.join(self.folder,"TDCMEME")
        self.logger.debug("dossier de sortie: {}".format(folder_to_extract_to))
        if not os.path.exists(folder_to_extract_to):
            self.logger.debug("le dossier de sortie n'existe pas, création")
            try:
                os.mkdir(folder_to_extract_to)
            except OSError:
                raise Exceptions.Error("Erreur lors de la création du dossier de sortie", "Impossible de créer le dossier suivant: {}".format(folder_to_extract_to), self.logger)
        self.logger.info("création du fichier zip de sortie")
        if not out_zip_file:
            out_zip_file = self.basename
        self.out_zip_file = os.path.join(folder_to_extract_to,out_zip_file)
        self.logger.debug("fichier de sortie: {}".format(out_zip_file))
        with zipfile.ZipFile(self.out_zip_file, mode='w', compression=8) as zip_file:
            for f in self.files_in_zip:
                full_path_to_file = os.path.join(self.temp_dir,f)
                zip_file.write(full_path_to_file,arcname=f)
        self.logger.debug("fichier zip en sortie créé avec succès")
        return self

    @logged
    def delete_temp_dir(self):
        self.logger.info("suppression du répertoire temporaire")
        try:
            shutil.rmtree(self.temp_dir)
        except:
            raise Exceptions.Error("Impossible de supprimer le répertoire temporaire","Impossible de supprimer le répertoire temporaire suivant: {}".format(self.temp_dir))
        self.logger.debug("répertoire temporaire supprimé")
        self.flat = False

# not needed anymore
##    @logged
##    def parse_mission(self):
##        if not self.checked:
##            self.check()
##        if not self.flat:
##            self.decompact()
##        self.mission_file = os.path.join(self.temp_dir,"mission")
##        return mission.Mission(self.mission_file)



