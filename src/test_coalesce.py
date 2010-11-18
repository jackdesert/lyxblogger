#! /usr/bin/env python
# -*- coding: utf-8 -*-
#####################       A U T H O R       ##########################
#                                                                      #
#   Copyright 2010 Jack Desert                                         #
#   <jackdesert556@gmail.com>                                          #
#   <http://www.LetsEATalready.com>                                    #
#                                                                      #
######################      L I C E N S E     ##########################
#                                                                      #
#   This file is part of LyxBlogger.                                   #
#                                                                      #
#   LyxBlogger is free software: you can redistribute it and/or modify #
#   it under the terms of the GNU General Public License as published  #
#   by the Free Software Foundation, either version 3 of the License,  #
#   or (at your option) any later version.                             #
#                                                                      #
#   LyxBlogger is distributed in the hope that it will be useful,      #
#   but WITHOUT ANY WARRANTY; without even the implied warranty of     #
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the      #
#   GNU General Public License for more details.                       #
#                                                                      #
#   You should have received a copy of the GNU General Public License  #
#   along with LyxBlogger.  If not, see <http://www.gnu.org/licenses>. #
#                                                                      #
########################################################################

# This test script tests coalesce.py

import os, unittest

def save_to_file(input):
    # Read data rom file
    f = open('.temp_in.py', 'w')
    f.write(input)
    f.close()

def get_output():
    a = os.system('./coalesce.py .temp_in.py .temp_out.py')
    if a != 0:
        raise ValueError('Something wrong here')
    f = open('.temp_out.py', 'r')
    coalesced_data = f.read()
    f.close()
    return(coalesced_data)

class MenuTestCase(unittest.TestCase):

    def setUp(self):
        pass
    def test_local_import(self):
        # Only run this test if using Python 2.5 or later, which
        code = "from LyxBlog.misc import pr3"
        save_to_file(code)
        self.assertTrue('sys.stdout.write' in get_output())
    def test_system_module(self):
        code = "import os"
        save_to_file(code)
        self.assertTrue('import os' in get_output())
    def test_external_module(self):
        code = "import elyxer"
        save_to_file(code)
        self.assertTrue('import elyxer' in get_output())
    def test_socket(self):
        code = "from socket import gaierror"
        save_to_file(code)
        print('output is: ' + get_output())
        self.assertTrue('from socket import gaierror' in get_output())


if __name__ == '__main__':
    unittest.main()
    os.system('rm -f .temp_in.py .temp_out.py')     # cleanup

