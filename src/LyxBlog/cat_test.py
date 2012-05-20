#! /usr/bin/env python
# -*- coding: utf-8 -*-
#####################       A U T H O R       ##########################
#                                                                      #
#   Copyright 2010 Jack Desert                                         #
#   <jackdesert@gmail.com>                                          #
#   http://TwoMoreLines.com                                            #
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

# Code to test cat.py

import sys
import unittest
import wordpresslib
from datetime import date
from misc import pr3
from cat import get_post_id
from cat import same_length
from cat import MiniPost


class CatTestCase(unittest.TestCase):

    def setUp(self):
        pass
    def test_get_post_id(self):
        # prepare client object
        in_wp_obj = wordpresslib.WordPressClient(
            'http://blogtest.twomorelines.com/xmlrpc.php', 'test', 'test')
        id = get_post_id(in_wp_obj)
        #Should we be validating 'id'?
    def test_same_length(self):
        date_flag = 'DDDDD'
        a_string = 'abcdefghij'
        a_string = a_string * 100
        a_string = a_string + date_flag + 'some_date'
        list_of_strings = [a_string]
        list_of_truncated_strings = same_length(list_of_strings, date_flag)
        self.assertTrue(len(list_of_truncated_strings[0]) < 60)
    def test_Mini_Post(self):
        mydate = date(1982, 12, 25)
        a = MiniPost(1,'Nice Title', mydate)
        self.assertTrue(a.title == 'Nice Title')
        self.assertTrue(a.post_id == 1)




if __name__ == '__main__':
    unittest.main()

