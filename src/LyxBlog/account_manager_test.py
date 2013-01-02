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
import sys
from account import Account
from account_manager import AccountManager
from account_manager import SystemNotFoundError

class AccountManagerTestCase(unittest.TestCase):

#    def test_initialization(self):
#        a = AccountManager()
#        path = a._AccountManager__configpath
#        self.assertTrue(path.endswith(".lyxblogger/config.cfg"))
#    def test_system_not_found_error(self):
#        saved_platform = sys.platform
#        sys.platform = 'spiderman'
#        self.assertRaises(SystemNotFoundError, AccountManager)
#        sys.platform = saved_platform
#    def test_add_account(self):
#        a = AccountManager()
#        url = 'http://myblog.com'
#        username = 'charles'
#        password = 'not telling'
#        a.add_account(url, username, password)
#        accounts = a._AccountManager__accounts
#        self.assertEquals(a._AccountManager__accounts[0], Account(url, username, password))
    def test_save_accounts_to_file(self):
        aa = AccountManager()
        aa.reset_config()
        url = 'http://cheeky.com'
        username = 'mgh'
        password = 'no fair yelling'
        self.assertEqual(len(aa.get_accounts()), 0)
        aa.add_account(url, username, password)
        self.assertEqual(len(aa.get_accounts()), 1)
        bb = AccountManager()
        aa_account = aa.get_accounts()[0]
        bb_account = bb.get_accounts()[0]
        self.assertEquals(aa_account, bb_account)
        
        

if __name__ == '__main__':
    unittest.main()

