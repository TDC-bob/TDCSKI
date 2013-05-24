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
from . import Exceptions
from _logging._logging import logged, mkLogger, DEBUG, INFO, WARN, ERROR
import pygit2

logger = mkLogger(__name__, DEBUG)

class GSP():
    def __init__(self):
        self.git = os.path.normpath(os.path.join(os.getcwd(),"bobgit/bin/git.exe"))

    def clone(self, remote_repo, local_repo_name):
        cur_dir = os.getcwd()
        os.chdir(os.path.normpath(os.path.join(os.getcwd(),"bobgit")))
        self._run(["clone",remote_repo,local_repo_name])
        os.chdir(cur_dir)

    def pull(self, repo, remote="origin"):
        cur_dir = os.getcwd()
        os.chdir(repo)
        self._run(["fetch", remote])
        self._run(["merge", "master"])
        os.chdir(cur_dir)



    @logged
    def _run(self, args):

    ##    with subprocess.Popen(args,
    ##     bufsize=-1,
    ##     executable=os.path.normpath(os.path.join(os.getcwd(),"dist/bin/git.exe")),
    ##     stdin=None,
    ##     stdout=subprocess.PIPE,
    ##     stderr=subprocess.STDOUT,
    ##     preexec_fn=None,
    ##     close_fds=False,
    ##     shell=True,
    ##     cwd=None,
    ##     env=None,
    ##     universal_newlines=True,
    ##     startupinfo=None,
    ##     creationflags=0,
    ##     restore_signals=True,
    ##     start_new_session=False,
    ##     pass_fds=()) as proc:
    ##        rtn = proc.stdout.read()
    ##    print(rtn)
    ##    return

        cmd = [self.git]
        for a in args:
            cmd.append(a)
        self.logger.info("running following git command: {}".format(cmd))
    ##    print(cmd)
        try:
            rtn = subprocess.check_output(cmd,
                                        shell=True,
                                        universal_newlines=True,
                                        stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as e:
            cmd, code, output = e.cmd, e.returncode, e.output
    ##        print("GIT FATAL ERROR\nCMD: {}\nOUTPUT:\n-------\n{}\n------------\nEND OF OUTPUT"
    ##                                                                        .format(cmd,output))
            raise Exceptions.GitRunError("échec de la commande Git: \n\n{}\n\n".format(" ".join([c for c in cmd[1:]])),
                "Git stdErr &> stdOut:\n=========\n{}\n=========\nEnd of Git output\n\n".format(output),
                self.logger)
    ##        exit(1)
        #TODO: parse return
        self.logger.info("git output:\n\n{}\n\nEND OF GIT OUTPUT\n\n".format(rtn))
##        return rtn


def main():
    _run(["test",])
    return
    os.chdir("C:\\")
    if not os.path.exists(r"d:\test\test1"):
        os.makedirs(r"d:\test\test1")
    os.chdir(r"d:\test\test1")
    try:
        rtn = subprocess.check_output(
        [
            "git","clone","C:\Documents and Settings\owner\My Documents\BORIS\TDC\TDCSKI.git",r"d:\test\test2"
        ],
        shell=True,
        universal_newlines=True,
        stderr=subprocess.STDOUT
        )
        rtn = subprocess.check_output(
        [
            "git","fetch"
        ],
        shell=True,
        universal_newlines=True,
        stderr=subprocess.STDOUT
        )
        rtn = subprocess.check_output(
        [
            "git","merge","master"
        ],
        shell=True,
        universal_newlines=True,
        stderr=subprocess.STDOUT
        )
    except subprocess.CalledProcessError as e:
        print(e.cmd)
        print(e.returncode)
        print(e.output)
        exit(1)
    print(rtn)
    exit(0)

if __name__ == '__main__':
    main()
