import unittest
import os
from utils import ShellUtils


class testShellUtils(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        os.removedirs("testdir")

    def testMkDir(self):
        self.assertFalse(os.path.exists("testdir"))
        ShellUtils.mkdir("testdir")
        self.assertTrue(os.path.exists("testdir"))
