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

import unittest
import pdb
from account import Account

class AccountTestCase(unittest.TestCase):

    def test_initialization(self):
        url = 'http://hi.com'
        user = 'joe'
        password = 'nobodys business'
        section_id = 300
        a = Account(section_id, url, user, password)
        self.assertEqual(a._Account__section_id, 300)
        self.assertEqual(a._Account__url, url)
        self.assertEqual(a._Account__username, user)
        self.assertEqual(a._Account__password, password)
        self.assertEqual(a._Account__section_id, section_id)
    def test_url(self):
        url = 'blah'
        a = Account(1, url, 'moose', 'long_underwear')
        self.assertEqual(a.get_url(), url)
    def test_username(self):
        username = 'bones'
        a = Account(1, 'http://hi.com', username, 'fancy_password')
        self.assertEqual(a.get_username(), username)
    def test_password(self):
        a = Account(1, 'blah', 'barry', None)
        self.assertEqual(a.get_password(), None)
        password = 'password'
        a.set_password(password)
        self.assertEqual(a.get_password(), password)
    def test_eq(self):
        url = 'long one'
        username = 'shirade'
        password = 'long'
        aa = Account(1, url, username, password)
        bb = Account(1, url, username, password)
        self.assertEqual(aa, bb)
        

if __name__ == '__main__':
    unittest.main()

