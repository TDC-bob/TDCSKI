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
import Exceptions

import logging, _logging
logger = _logging.mkLogger(__name__, logging.INFO )

def clone(target_dir, remote_repo):
    cur_dir = None
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    if not os.getcwd() == target_dir:
        cur_dir = os.getcwd()


def _run(args):
    cmd = ["git"]
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
        raise Exceptions.GitRunError("failed while running git command: {}".format(cmd),
            "Git output was:\n------------\n{}\n------------\nEnd of Git output".format(output))
        exit(1)
    #TODO: parse return
##    print(rtn)


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
