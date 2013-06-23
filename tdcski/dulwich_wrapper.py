#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Copyright 2013 Bob <TDC-bob@daribouca.net>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#

from dulwich import dulwich
from io import StringIO

__version__ = (0, 0, 1)
__author__ = 'TDC-Bob'

#~ class Repo():
    #~ def __init__(self, local_path, origin_url=None):
        #~ try:
            #~ self.repo = repo.Repo(local_path)
        #~ except repo.NotGitRepository:
            #~ self.repo = repo.Repo.init(local_path, True)
#~
#~ def fetch_refs():
    #~ url = "https://github.com/TDC-bob/modlist"
    #~ _client = client.HttpGitClient(url, dumb=None, thin_packs=True)
    #~ f = StringIO()
    #~ refs = _client.fetch_pack("/", determine_wants, DummyGraphWalker(), pack_data=f.write, progress=progress)
#~
#~ def determine_wants(refs):
    #~ print("refs: {}".format(refs))
    #~ # retrieve all objects
    #~ return refs.values()
#~
#~ class DummyGraphWalker():
    #~ def ack(self, sha):
        #~ print("ack: {}".format(sha))
    #~ def next(self): pass
#~
#~ def progress(data):
    #~ print("progress: {}".format(data))
#~



def main():
    import os
    import shutil
    import urllib
    #~ test = urllib.parse.urlparse("https://github.com:TDC-bob/modlist")
    #~ print(test)
    #~ exit(0)
    #~ try:
    path = "/home/bob/Git/testing_dulwich"
    remote_url = "https://github.com/TDC-bob/modlist"
    #~ repodulwich clone host:path [PATH]
    repo = dulwich.clone(remote_url, path)
    #~ pack = fetch_refs()
    #~ print(pack)
    #~ return
    #~ except:
        #~ print("except")
        #~ shutil.rmtree(path)

    #~ testing_repo = Repo(path)
    return 0

if __name__ == '__main__':
    main()

