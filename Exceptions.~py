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


from _logging import mkLogger
logger = mkLogger("EXCEPTION")

class Error(Exception):
    def __init__(self, base_info="Pas d'information sur cette erreur", message="Pas de message pour cette erreur", logger=logger):
        logger.error('''FATAL ERROR: {}\n\tMessage: {}'''.format(base_info, message))


class InvalidMissionFile(Exception):
    def __init__(self, filepath="No filepath given", logger=logger, message="Pas de message spécifique pour cette exception"):
        logger.error('''ce fichier n'est pas un fichier mission valide: "{}"\n\tMessage: {}'''.format(filepath, message))


class InvalidMizFile(Exception):
    def __init__(self, filepath="No filepath given", logger=logger, message="Pas de message spécifique pour cette exception"):
        logger.error('''le fichier MIZ n'est pas valide: "{}"\n\tMessage: {}'''.format(filepath, message))
##        super(InvalidMizFile, self).__init__(filepath)
##        exit(-1)


class FileDoesNotExist(Exception):
    def __init__(self, filepath, logger, message="Pas de message spécifique pour cette exception"):
        logger.error('''le fichier mission spécifié n'existe pas: "{}"\n\tMessage: {}'''.format(filepath, message))


class MissingObjectInZipFile(Exception):
    def __init__(self, mizFilePath, objName, logger):
        logger.error('''le fichier "{}" ne contient pas de fichier "{}"'''.format(mizFilePath, objName))
        #~ super(Exceptions.MissingObjectInZipFile, self).__init__(file)
        #~ exit(-1)


class ParameterInvalid(Exception):
    def __init__(self, param, logger=logger, message="Pas de message spécifique pour cette exception"):
        logger.error('''le paramètre passé est invalide: "{}"\n\tMessage: {}'''.format(param, message))


class CantRemoveTempDir(Exception):
    def __init__(self, path, logger=logger, message="Pas de message spécifique pour cette exception"):
        logger.error('''impossible de supprimer le répertoire temporaire "{}"\n\tMessage: {}'''.format(path, message))


class CantCreateTempDir(Exception):
    def __init__(self, path, logger=logger, message="Pas de message spécifique pour cette exception"):
        logger.error('''impossible de créer le répertoire temporaire "{}"\n\tMessage: {}'''.format(path, message))


class EncodingError(Exception):
    def __init__(self, message="Pas de message spécifique pour cette exception", logger=logger, ):
        logger.error('''erreur durant l'encodage\n\tMessage: {}'''.format(message))


class CoultNotWriteZipFile(Exception):
    def __init__(self, filepath, logger=logger, ):
        logger.error('''erreur pendant l'écriture du fichier ZIP suivant: {}'''.format(filepath))


class CoultNotWriteMissionFile(Exception):
    def __init__(self, filepath, logger=logger, ):
        logger.error('''erreur pendant l'écriture du fichier mission: {}'''.format(filepath))


class CouldNotExtract(Exception):
    def __init__(self, filepath, obj, logger=logger, ):
        logger.error('''erreur pendant l'extraction de l'objet "{}" depuis le  fichier {}'''.format(obj, filepath))


class MultipleGroupsFoundWithSameName(Exception):
    def __init__(self, filepath, groupName, logger=logger):
        logger.error('''plusieurs groupes portant le nom {} ont été trouvés dans le fichier {}'''.format(groupName, filepath))


class GroupNameInvalid(Exception):
    def __init__(self, mizFile, groupName, logger=logger):
        logger.error("Nom de groupe \"{}\" invalide dans la mission {}".format(groupName, mizFile.path))
