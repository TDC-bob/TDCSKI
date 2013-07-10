# coding=utf-8
__version__ = (0, 0, 2)
version = ".".join([str(x) for x in __version__])
__author__="bob"
import os
if os.environ['TRAVIS'] == "true":
    pass
else:
    import winreg
from tdcski import config_handler as config_handler
config_file = config_handler.ConfigHandler(must_exists=False)

class Config():
    def __init__(self):
        self.server = ServerConfig()
        self.path_to = FoldersConfig()

class ServerConfig():
    def __init__(self):
        self.__port = "10307"
        self.__interface = "127.0.0.1"
        config_file.create("server", "interface", self.__interface)
        config_file.create("server", "port", self.__port)
        self.__port = config_file.get("server", "port")
        self.__interface = config_file.get("server","interface")

    @property
    def interface(self):
        return self.__interface
    @interface.setter
    def interface(self, value):
        self.__interface = value
        config_file.set("server", "interface", value)

    @property
    def port(self):
        return self.__port
    @port.setter
    def port(self, value):
        self.__port = value
        config_file.set("server", "port", value)

class FoldersConfig():
    def __init__(self):
        self.own_dir = '.'
        self.own_full_path = os.path.normpath(os.path.abspath(os.path.join(os.getcwd(), "tdcski.exe")))
        self.own_name = os.path.basename(self.own_full_path)
        self.own_dir = os.path.dirname(self.own_full_path)

        self.__DCS, caribou = winreg.QueryValueEx (winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Eagle Dynamics\DCS World"), "Path")
        del caribou
        config_file.create("paths", "dcs_install", self.DCS)
        self.__DCS = config_file.get("paths", "dcs_install")

        self.__saved_games = os.path.normpath(os.path.expanduser("~/saved games/dcs"))
        config_file.create('paths','saved_games', self.__saved_games)
        self.__saved_games = config_file.get('paths', 'saved_games')

    @property
    def DCS(self):
        return self.__DCS
    @DCS.setter
    def DCS(self, value):
        self.__DCS = value
        config_file.set("paths", "dcs_install", value)

    @property
    def saved_games(self):
        return self.__saved_games
    @saved_games.setter
    def saved_games(self, value):
        self.__saved_games = value
        config_file.set("paths", "saved_games", value)


config = Config()