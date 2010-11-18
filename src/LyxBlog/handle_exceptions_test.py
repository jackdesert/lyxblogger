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
#   This file is part of LyXBlogger.                                   #
#                                                                      #
#   LyXBlogger is free software: you can redistribute it and/or modify #
#   it under the terms of the GNU General Public License as published  #
#   by the Free Software Foundation, either version 3 of the License,  #
#   or (at your option) any later version.                             #
#                                                                      #
#   LyXBlogger is distributed in the hope that it will be useful,      #
#   but WITHOUT ANY WARRANTY; without even the implied warranty of     #
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the      #
#   GNU General Public License for more details.                       #
#                                                                      #
#   You should have received a copy of the GNU General Public License  #
#   along with LyXBlogger.  If not, see <http://www.gnu.org/licenses>. #
#                                                                      #
########################################################################

import sys
from socket import gaierror
import unittest
import wordpresslib
from misc import pr3
from handle_exceptions import handle_gaierror
from handle_exceptions import handle_general_error
from handle_exceptions import handle_input_error

"Note: You must click ENTER during each test to close the program."
"Then after all tests are run it will tell you how many passed"

class HandleExceptionsTestCase(unittest.TestCase):

    def setUp(self):
        pass
    def test_handle_gaierror(self):
        try:
            raise gaierror
        except gaierror:
            self.assertRaises(SystemExit, handle_gaierror)

    def test_handle_general_error(self):
        try:
            raise gaierror
        except gaierror:
            self.assertRaises(SystemExit, handle_general_error)

    def test_handle_input_error(self):
        try:
            raise gaierror
        except gaierror:
            self.assertRaises(SystemExit, handle_input_error)



if __name__ == '__main__':
    unittest.main()
