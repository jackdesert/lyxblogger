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

# Code to test image.py

import sys
import unittest
import pdb
from display import Display

class DisplayTestCase(unittest.TestCase):

    def setUp(self):
        self.display = Display()
    def test_print_format(self):
        expected = self.display.print_format('random')
        self.assertEqual(expected, "    Format: random")
    def test_print_title(self):
        expected = self.display.print_title('random')
        self.assertEqual(expected, "    Title: random")
    def test_print_word_count(self):
        expected = self.display.print_word_count('random')
        self.assertEqual(expected, "    Word Count: random")
    def test_print_image_count(self):
        expected = self.display.print_image_count('random')
        self.assertEqual(expected, "    Image Count: random")
    def test_ask_for_password(self):
        print "\n\nIn a couple of lines you will be asked for a password. You must type something in before the test can proceed.\n\nPlease enter the word 'test'\n\n"
        expected = self.display.ask_for_password()
        self.assertEqual(expected, "test")

if __name__ == '__main__':
    unittest.main()

