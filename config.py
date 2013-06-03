__author__ = 'bob'

from lib.configobj import ConfigObj
from _logging._logging import mkLogger, logged, DEBUG
import os
logger = mkLogger(__name__, DEBUG)
git_exe = None
DCS_path = None
SaveGames_path = None

class Config():
    def __init__(self, file='../tdcski.cfg'):
        if not os.path.exists(file):
            logger.error("impossible de trouver le fichier de configuration sur le chemin suivant: {}".format(os.path.abspath(file)))
            exit(1)
        self.__config = ConfigObj(infile=file,encoding="latin-1", default_encoding="latin-1")

    def get(self, *args):
        if not args:
            return ''
        base = self.__config
        try:
            while len(args) > 1:
                base = base[args[0]]
                args = args [1:]
            return base[args[0]]
        except KeyError:
            return None

    @property
    def values(self):
        return self.__config.values()

    @property
    def keys(self):
        return self.__config.keys()

    @property
    def items(self):
        return self.__config.items()

    def iteritems(self):
        self.__config.iteritems()

    def iterkeys(self):
        self.__config.iterkeys()

    def itervalues(self):
        self.__config.itervalues()

    def reload(self):
        self.__config.reload()

    def set_or_create(self, *args):
        if not self.set(*args):
            if not self.create(*args):
                return None
        return True

    def create(self, *args):
        if self.get(*args[0:-1]):
            return None
        base = self.__config
        while len(args) > 2:
            try:
                base[args[0]]
            except KeyError:
                base[args[0]] = {}
            base = base[args[0]]
            args = args[1:]
        base[args[0]] = args[1]
        self.__config.write()
        return True

    def set(self, *args):
        if not self.get(*args[0:-1]):
            return None
        base = self.__config
        while len(args) > 2:
            base = base[args[0]]
            args = args[1:]
        base[args[0]] = args[1]
        self.__config.write()
        return True

    def delete(self, *args):
        if not self.get(*args[0:-1]):
            return True




