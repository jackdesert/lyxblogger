#! /usr/bin/env python
# -*- coding: utf-8 -*-
#######################  L Y X B L O G G E R   #########################
#   This program allows you to post to your WordPress blog right from  #
#   LyX. The input to this script is xhtml.                            #
#   Supported LyX --> xhtml converters:                                #
#                                                                      #
#      LyXHTML output from LyX 2.0.                                    #
#      eLyXer output from LyX 1.6 and later. (Earlier may work too)    #
#                                                                      #
#   This script will connect using xml-rpc.                            #
#                                                                      #
#################     D O C U M E N T A T I O N       ##################
#                                                                      #
#   Please see the docs/ folder for LyXBlogger documentation.          #
#   Alternatively, see the online docs for the latest version of       #
#   LyXBlogger at www.nongnu.org/lyxblogger                            #
#   Please submit any issues or suggestions to the author.             #
#                                                                      #
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
import os, unittest
from profiles import init_config
from profiles import delete_config_file

class ProfilesTestCase(unittest.TestCase):

    def setUp(self):
        self.a_file = ".profile"
        if os.path.exists(self.a_file):
            os.remove(self.a_file)
    def test_00_init_config(self):
        self.assertFalse(os.path.exists(self.a_file))
        init_config(self.a_file)
        self.assertTrue(os.path.exists(self.a_file))
        f = open(self.a_file, "r")
        text = f.read()
        assert("delay" in text)
        assert("cut_flag" in text)
        assert("last_profile" in text)
        assert("next_section_n" in text)
        assert("DEFAULT" in text)
    def test_01_delete_config_file(self):
        delete_config_file()

if __name__ == '__main__':
    unittest.main()
