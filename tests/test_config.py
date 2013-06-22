#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  untitled.py
#
#  Copyright 2013 bob <bob@tinybou>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
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

import unittest
import config
import os

from _logging._logging import mkLogger, logged, DEBUG
#logger = mkLogger(__name__, DEBUG)

class testConfig(unittest.TestCase):

    def setUp(self):
        test_content = [
            "str1 = value1\n",
            "str2 = value2\n",
            "boolt_1 = True\n",
            "boolf_1 = False\n",
            "boolt_2 = true\n",
            "boolf_2 = false\n"
            "boolt_3 = y\n",
            "boolt_4 = yes\n",
            "boolt_5 =  oui\n",
            "boolt_6 = o\n",
            "boolf_3 = no\n",
            "boolf_4 = non\n",
            "boolf_5 = n\n"
        ]
        self.file = "config.test_file"
        with open(self.file, mode="w") as file:
            file.writelines(test_content)
        self.config = config.Config(self.file)

    def tearDown(self):
        os.remove(self.file)
        if os.path.exists("tchoutchou"):
            os.remove("tchoutchou")

    def test_config_stringValues(self):
        self.assertEqual(self.config.get("str1"), "value1")
        self.assertEqual(self.config.get("str2"), "value2")

    def test_config_properties(self):
        self.assertEqual(self.config.file.path, "config.test_file")

    def test_config_reload(self):
        self.assertTrue(self.config.get("boolt_2"))
        with open(self.file, mode="a")as f:
            f.write("reload_test = true")
        self.assertIsNone(self.config.get("reload_test"))
        self.config.reload()
        self.assertTrue(self.config.get("reload_test"))

    def test_config_noneValues(self):
        self.assertIsNone(self.config.get("non_existent_key"))

    def test_config_bool(self):
        for x in ["boolt_1", "boolt_2", "boolt_3", "boolt_4",
        "boolt_5", "boolt_6"]:
            self.assertTrue(self.config.get(x))
        for x in ["boolf_1", "boolf_2", "boolf_3", "boolf_4",
        "boolf_5"]:
            self.assertFalse(self.config.get(x))

    def test_config_createString(self):
        self.config.create("writeStr_1", "baseValue")
        self.assertEqual(self.config.get("writeStr_1"), "baseValue")
        self.config.create("writeStr_1", "newValue")
        self.assertEqual(self.config.get("writeStr_1"), "baseValue")

    def test_config_setString(self):
        self.config.create("setStr_1", "baseValue")
        self.assertEqual(self.config.get("setStr_1"), "baseValue")
        self.config.set("setStr_1", "newValue")
        self.assertEqual(self.config.get("setStr_1"), "newValue")

    def test_config_createBool(self):
        self.config.create("createBool_1", "True")
        self.assertTrue(self.config.get("createBool_1"))
        self.config.create("createBool_2", "False")
        self.assertFalse(self.config.get("createBool_2"))
        self.config.create("createBool_1", "False")
        self.assertTrue(self.config.get("createBool_1"))
        self.config.create("createBool_3", True)
        self.assertTrue(self.config.get("createBool_3"))

    def test_config_setBool(self):
        self.config.create("setBool_1", "False")
        self.config.create("setBool_2", "True")
        self.assertFalse(self.config.get("setBool_1"))
        self.assertTrue(self.config.get("setBool_2"))
        self.config.set("setBool_1", True)
        self.assertTrue(self.config.get("setBool_1"))
        self.config.set("setBool_2", False)
        self.assertFalse(self.config.get("setBool_2"))

    def test_config_setOrCreate(self):
        self.config.set_or_create("setOrCreate_1", "init")
        self.assertEqual(self.config.get("setOrCreate_1"), "init")
        self.config.set_or_create("setOrCreate_1", "new_value")
        self.assertEqual(self.config.get("setOrCreate_1"), "new_value")

    def test_config_readTooDeep(self):
        with self.assertRaises(TypeError):
            self.config.get("str1", "value1")

    def test_config_intricateSetAndRead(self):
        lvl = ["l1", "l2", "l3", "l4", "l5", "l6", "l7"]
        val = ["l1", "l2", "l3", "l4", "l5", "l6", "l7", False]
        self.config.set_or_create(*val)
        self.assertFalse(self.config.get(*lvl))
        val = ["l1", "l2", "l3", "l4", "l5", "l6", "l7", True]
        self.config.set_or_create(*val)
        self.assertTrue(self.config.get(*lvl))
        val = ["l1", "l2", "l3", "l4", "l5", "l6", "l7", "test_string"]
        self.config.set_or_create(*val)
        self.assertEqual(self.config.get(*lvl), "test_string")

    def test_config_fileDoesNotExist(self):
        with self.assertRaises(config.ConfigFileDoesNotExist):
            config.Config("i_do_not_exist")

    def test_config_fileCreation(self):
        f = config.Config("tchoutchou", False)
        f.set_or_create("str", "value")
        f.set_or_create("bool", False)
        f.set_or_create("int", 12)
        f.set_or_create("float", 1.234)
        self.assertEqual(f.get("str"), "value")
        self.assertEqual(f.get("bool"), False)
        self.assertEqual(f.get("int"), 12)
        self.assertEqual(f.get("float"), 1.234)


def main():

    return 0

if __name__ == '__main__':
    unittest.main(verbosity=9)

