#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

# Copyright (C) 2012 LibreSoft
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
#
# Authors :
#       Eduardo Menezes de Morais <companheiro.vermelho@gmail.com>
#       Alessandro Palmeira <alessandro.palmeira@gmail.com>
#
# To execute this test, run: "python -m unittest tests.file_path_test" in the
# root of the project

import unittest
import os
import shutil
import tempfile
import pysqlite2.dbapi2 as db
import pycvsanaly2.main

class FilePathTestCase(unittest.TestCase):

    TEST_REPOSITORY_PATH = "tests/input"
    TEST_TAR_FILE = "tests/input.tar.gz"

    def setUp(self):
        self.maxDiff = None
        if not os.path.exists(self.TEST_REPOSITORY_PATH):
            os.system("tar -xzf " + self.TEST_TAR_FILE + " -C tests")

    def tearDown(self):
        shutil.rmtree(self.TEST_REPOSITORY_PATH)

    def testFilePathOutput(self):
        # run CVSAnaly on test repository
        opened, temp_file_name = tempfile.mkstemp('.db', 'cvsanaly-test')
        os.close(opened)
        command_line_options = ["--db-driver=sqlite", "-d", temp_file_name, self.TEST_REPOSITORY_PATH]
        pycvsanaly2.main.main (command_line_options)

        # fetch generated result
        connection = db.connect (temp_file_name)
        cursor = connection.cursor()
        cursor.execute("SELECT file_path FROM file_links")
        actual = cursor.fetchall()
        cursor.close()
        connection.close()
        os.remove(temp_file_name)

        expected = [(u'aaa',), (u'aaa/otherthing',), (u'aaa/something',), (u'bbb',), (u'bbb/bthing',), (u'bbb/something',), (u'bbb/ccc',), (u'bbb/ccc/yet_anotherthing',), (u'ddd',), (u'ddd/finalthing',), (u'eee',), (u'eee/fff',), (u'eee/fff/wildthing',)]

        self.assertItemsEqual (actual, expected)

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(UnicodeTestCase)
    unittest.TextTestRunner(verbosity=2).run(suite)
