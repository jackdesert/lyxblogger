#! /usr/bin/env python
# -*- coding: utf-8 -*-
#####################       A U T H O R       ##########################
#                                                                      #
#   Copyright 2010 Jack Desert                                         #
#   <jackdesert@gmail.com>                                          #
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
'''

NOTE:  YOU MUST ENTER THE PASSWORD OF 'test' WHEN ASKED FOR IT

For some reason getpass.getpass() does not recognize the automated
input. Actually, it asks for it before previous print() statements have
been processed.
This is part of the unit testing, although its approach is a bit
different. So far there are no assert() statements in this file.
However, the true grace of this testing procedure is one of testing
the entire package as one. This file puts LyXBlogger through its
paces. It tries each use case scenario at least once. And if it makes
it through to the last statement, then the logic in LyXBlogger passed,
plus it means that each major block of code within LyXBlogger is
basically functional.

What this file does not test for are the out of bounds conditions. For
example, when you expect a category response between 1 and 5, but you
get 6 instead. Ideall, this sort of testing would be provided for in
micro-scale unit tests as found in other test files within LyXBlogger.
At the time of this writing (version 0.35+) not all functions in
LyXBlogger have a unit test that tests them.
'''

import os
import subprocess
import unittest
import time
from profiles import delete_config_file

class OneLiner:
    def __init__(self, prompt, response):
        self.prompt = prompt
        self.response = response

def interact_once(args, one_liners):


    # I don't know why shell needs to be True
    proc = subprocess.Popen(args,
                            shell=True,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE
                            )
    for line in one_liners:
        print "-----------   New prompt: \'%s\'  Will respond with: \'%s\'" % (line.prompt, line.response)
        while True:
            # print '--------one-line-read-from-interact_test.py-------'
            output = proc.stdout.readline()
            print output.strip()  # strip trailing newlines we added in lyxblogger.pr3
            if line.prompt in output:
                break
        if line.prompt != one_liners[-1].prompt:   # Don't pass anything after the last prompt, otherwise sometimes it hangs
            proc.stdin.write(line.response + '\n')
        print "-----------   Prompt found. Response passed."


class InteractiveTestCase(unittest.TestCase):
    # Typical usage is:
    # self.args = 'python seed.py ../folder_test/test_file.xhtml --run-here'
    def setUp(self):
        print self
        self.elyxer_args = 'python ../seed.py ../../folder_test/test_file.xhtml --run-here'
        self.elyxer_no_title_args = 'python ../seed.py ../../folder_test/no_title_test_file.xhtml --run-here'
        self.lyxhtml_args = 'python ../seed.py test_files/lyxhtml_w_images/LyXHtml_test_with_image.xhtml --run-here'
        delete_config_file()
        elyxer_args = 'elyxer.py ../../folder_test/original_test_file.lyx ../../folder_test/test_file.xhtml'
        elyxer_args_2 = 'elyxer.py ../../folder_test/original_no_title.lyx ../../folder_test/no_title_test_file.xhtml'
        output = os.system(elyxer_args)
        output_2 = os.system(elyxer_args_2)
        assert(output == 0)
        assert(output_2 == 0)
    def test_01_publish_new_to_new_site(self):
        print("saying something")
        one_liners = [OneLiner('latest', 'N'),
            OneLiner('username', 'test'),
            OneLiner('Example: cool_site.wordpress.com', 'blogtest.letseatalready.com'),
            OneLiner('plain text', 'YOU_MUST_MANUALLY_TYPE_THIS_PASSWORD_ROMPT'),
            OneLiner('latest', '1'),
            OneLiner('overwrite', 'N'),
            OneLiner('multiple categories', '1'),
            OneLiner('You just published', '(No Input Required)')]
        interact_once(self.elyxer_args, one_liners)
        interact_once(self.lyxhtml_args, one_liners)

    def test_02_publish_new_to_default_site(self):
        one_liners = [OneLiner('latest', '0'),
            OneLiner('overwrite', 'N'),
            OneLiner('multiple categories', '1,2,3'),
            OneLiner('You just published', '(No Input Required)')]
        interact_once(self.lyxhtml_args, one_liners)


    def test_03_update_existing(self):
        one_liners = [OneLiner('latest', '0'),
            OneLiner('overwrite', 'E'),
            OneLiner('post to overwrite', '2'),
            OneLiner('multiple categories', '1'),
            OneLiner('You just published', '(No Input Required)')]
        interact_once(self.elyxer_args, one_liners)
    def test_04_show_all_previous_posts(self):
        one_liners = [OneLiner('latest', '0'),
            OneLiner('overwrite', 'E'),             # Update Existing
            OneLiner('post to overwrite', 'A'),     # Display all posts
            OneLiner('Hint', '2'),                  # Select post
            OneLiner('multiple categories', '1'),
            OneLiner('You just published', '(No Input Required)')]
        interact_once(self.lyxhtml_args, one_liners)
    def test_05_publish_new_ask_for_title(self):
        one_liners = [OneLiner('Please enter a title', 'My Cool Title'),
            OneLiner('latest', '0'),
            OneLiner('overwrite', 'N'),
            OneLiner('multiple categories', '1'),
            OneLiner('You just published', '(No Input Required)')]
        interact_once(self.elyxer_no_title_args, one_liners)        # Note this is the NO TITLE test


#################  OLD TESTS    ####################
'''
The following tests are no longer used, because it required a lot
of password typing. Besides, they haven't been up dated to the new
format that uses profiles
'''
    # This test commented out so that there is only test that requires manual password typing, and it's first
    #~ def test_01_update_existing_alt_URL(self):
        #~ one_liners = [OneLiner('Publish this document', 'n'),
            #~ OneLiner('Example:', 'blogtest.letseatalready.com'),
            #~ OneLiner('WordPress username', 'test'),
            #~ OneLiner('WordPress password', 'test'),
            #~ OneLiner('overwrite', 'E'),
            #~ OneLiner('post to overwrite', '2'),
            #~ OneLiner('multiple categories', '1'),
            #~ OneLiner('SHIFT', '(No Input Required)')]
        #~ interact_once(self.args, one_liners)
    # This test commented out so that there is only test that requires manual password typing, and it's first
    #~ def test_02_show_all_previous_posts_alt_URL(self):
        #~ one_liners = [OneLiner('Publish this document', 'n'),
            #~ OneLiner('Example:', 'blogtest.letseatalready.com'),
            #~ OneLiner('WordPress username', 'test'),
            #~ OneLiner('WordPress password', 'test'),
            #~ OneLiner('overwrite', 'E'),
            #~ OneLiner('post to overwrite', 'A'),     # Display all posts
            #~ OneLiner('Hint', '2'),                  # Select post
            #~ OneLiner('multiple categories', '1'),
            #~ OneLiner('SHIFT', '(No Input Required)')]
        #~ interact_once(self.args, one_liners)

if __name__ == '__main__':
    print "\n\nYou will be asked for a password twice"
    print "Enter the password 'test' without the quotes each time"
    time.sleep(5)
    unittest.main()



