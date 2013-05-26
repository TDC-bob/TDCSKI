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
try:
    from . import Exceptions
except ImportError:
    import Exceptions
try:
    from _logging._logging import logged, mkLogger, DEBUG, INFO, WARN, ERROR
    logger = mkLogger(__name__, DEBUG)
    head_less = False
except ImportError:
    head_less = True

#todo: import _logging as a subtree (FFS, that's getting tangled)

class GSP():
    """
    Git wrapper

    Instanciation won't do anything to the local/remote FS, it's just to set up
    the local path to the Git executable and its libraries/templates.

    .. note::

       This is but a VERY basic stand-alone version of Git, with VERY limited functionalities.

    """
    def __init__(self):
        '''A really simple class.

        Args:
           foo (str): We all know what foo does.

        Kwargs:
           bar (str): Really, same as foo.

        '''
        self.git = os.path.normpath(os.path.join(os.getcwd(),"bobgit/bin/git.exe"))

    def clone(self, remote_repo, local_repo_name=""):
        '''
        Alias for the git 'clone' command

        :param remote_repo: full path or web address of the repo you want to clone
        :type remote_repo: string
        :param local_repo_name: the local path of the clone (defaults to Git default")
        :type local_repo_name: string
        :returns: output of both fetch & merge command
        :rtype: list
        '''
        cur_dir = os.getcwd()
        os.chdir(os.path.normpath(os.path.join(os.getcwd(),"bobgit")))
        self._run(["clone",remote_repo,local_repo_name])
        os.chdir(cur_dir)

    def pull(self, repo, remote="origin"):
        '''
        Alias for the git 'pull' command

        :param repo: full path to the repo in which the pull has to be run
        :type repo: string
        :param remote: the remote to pull from (defaults to origin)
        :type remote: string
        :returns: output of both fetch & merge command
        :rtype: list
        '''
        cur_dir = os.getcwd()
        os.chdir(repo)
        rtn_fetch = self._run(["fetch", remote])
        rtn_merge = self._run(["merge", "master"])
        os.chdir(cur_dir)
        return rtn_fetch, rtn_merge


    @logged
    def _run(self, args):
        '''
        Runs an arbitrary git command

        :param args: arguments passed to git
        :type args: list
        :returns: output of git subprocess
        :rtype: string
        :raises: Exceptions.GitRunError
        '''
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
        try:
            rtn = subprocess.check_output(cmd,
                                        shell=True,
                                        universal_newlines=True,
                                        stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as e:
            cmd, code, output = e.cmd, e.returncode, e.output
            raise Exceptions.GitRunError(
                "Git failed running: \n\n{}\n\n".format(" ".join([c for c in cmd[1:]])),
                "Git stdErr &> stdOut:\n=========\n{}\n=========\nEnd of Git output\n\n".format(output),
                self.logger)
        #TODO: parse return ?
        self.logger.info("git output:\n\n{}\n\nEND OF GIT OUTPUT\n\n".format(rtn))
        return rtn
