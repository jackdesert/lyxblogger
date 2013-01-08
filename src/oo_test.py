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

import time
import os

def pr3(something):
    print(something)

# First call all unit tests
# Note that we are not testing with python3.1 until the xmlrpclib is ported to it.
# versions = ['python2.4 ', 'python2.5 ', 'python2.6 ']
# simplifying tests by only testing one python version for now.
versions = ['python2.6 ']
# Running interact_test.py first
files = ['account_test.py',   # Nice short test requiring user to hit enter
        'account_manager_test.py', # longer test that requires "test" password entered once
        'display_test.py',
        'lyxblogger_test.py']
change_dir = 'cd LyxBlog\n' # Note that this does a cd and then a carriage return
for py_vers in versions:
    for test_file in files:
        pr3('Running unit tests from ' + test_file + ' using ' + py_vers)
        arg_string = change_dir + py_vers + test_file
        exit_code = os.system(arg_string)
        if (exit_code == 0):
            print('\n\nTESTS PASSED\n\n')
        else:
            raise Exception(' One or more tests failed. See above for details.')
pr3('All Unit Tests Passed')

# Also test the coalesce.py file
pr3('About to run test_coalesce.py')
a = os.system('python test_coalesce.py')
if a != 0:
    raise ValueError('test_coalesce.py failed')


