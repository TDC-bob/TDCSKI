# coding=utf-8
__author__ = 'bob'

import os
import bobgit.git as git

class Mod():
    def __init__(self, name, args):
        self.name = name
        self.local = os.path.abspath("../mods/{}".format(name))
        self.remote = args["remote"]
        self.repo = git.Repo(self.local, self.remote)
        self.branch = "master"
        for arg in args:
            if arg in ["remote"]:
                continue
            if arg == "branch":
                self.branch = args[arg]
                self.repo.checkout(self.branch)
            print("TODO: {}".format(arg))


        self.__files = []
        for root, dirs, files in os.walk(self.local):
            if '.git' in dirs:
                dirs.remove('.git')
            for file in files:
                if file == '.gitignore':
                    continue
                full_path = os.path.join(root, file)
                rel_path = full_path.replace(os.path.abspath(self.local), "")
                self.__files.append(ModFile(full_path,rel_path))

    @property
    def file_count(self):
        return len(self.__files)

    @property
    def files(self):
        return self.__files



    def __str__(self):
        return "Name: {}\nRemote: {}\nLocal: {}\nRepo: {}".format(self.name, self.remote, self.local,repr(self.repo))


class ModFile():
    def __init__(self, full_path, rel_path):
        self.__full_path = full_path
        self.__rel_path = rel_path
        self.__basename = os.path.basename(self.__rel_path)

    @property
    def full_path(self):
        return self.__full_path

    @property
    def rel_path(self):
        return self.__rel_path

    @property
    def basename(self):
        return self.__basename

    def __str__(self):
        return "Full path: {}\n" \
               "Relative path: {}\n" \
               "Basename: {}\n".format(self.__full_path,self.__rel_path,self.__basename)