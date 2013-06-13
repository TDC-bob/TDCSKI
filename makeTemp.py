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

import string, random, os


def random_string(prefix="", suffix="", size=8, chars=string.ascii_uppercase + string.digits):
   random_bit =  ''.join(random.choice(chars) for x in range(size))
##   return random_bit
   return "{}{}{}".format(prefix,random_bit,suffix)

def random_folder(base_path, prefix="", suffix="", size=8, chars=string.ascii_uppercase + string.digits):
    return os.path.join(base_path, random_string(prefix, suffix, size, chars))
