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
import _logging
from _logging import logged

import logging
logger = _logging.mkLogger(__name__, logging.DEBUG)

class GSP():
    def __init__self():
        pass

    def clone(self, target_dir, remote_repo):
        cur_dir = None
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)
        if not os.getcwd() == target_dir:
            cur_dir = os.getcwd()

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
        self.logger.info("running following git command: {}".format(" ".join([cc for cc in args])))
        cmd = [os.path.normpath(os.path.join(os.getcwd(),"bobgit/bin/_git.exe"))]
        print(cmd)
        for a in args:
            cmd.append(a)
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
                "Git stdErr &> stdOut:\n------------\n{}\n------------\nEnd of Git output\n\n".format(output),
                logger)
    ##        exit(1)
        #TODO: parse return
        logger.debug("git output:\n\n{}\n\nEND OF GIT OUTPUT\n\n".format(rtn))
        return rtn


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
