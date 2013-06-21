__author__ = 'bob'

import os
import unittest
import config

class TestGlobalFunctions(unittest.TestCase):

    testfile = "test_file"

    def setUp(self):
        pass

    def tearDown(self):
        os.remove(self.testfile)
        pass

    def test_config(self):
        conf = config.Config(file=self.testfile, must_exists=False)
        conf.set_or_create("general", "dcs_path",r"C:\Program Files\Eagle Dynamics\DCS World")
        with open(self.testfile) as file:
            print(file.readlines())

if __name__ == '__main__':
    try:
        unittest.main(verbosity=9)
    except KeyboardInterrupt:
        pass