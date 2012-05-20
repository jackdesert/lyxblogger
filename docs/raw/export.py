#! /usr/bin/env python
# -*- coding: utf-8 -*-
#####################       A U T H O R       ##########################
#                                                                      #
#   Copyright 2010 Jack Desert                                         #
#   <JackDesert@gmail.com>                                             #
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

# This file produces html documents from the .lyx documents
import os

def process_commands(command_list):
    for command in command_list:
        # Make sure each command executes properly. Otherwise, throw an exception
        a = os.system(command)
        if(a != 0):
            print('\nCommand was: ' + command)
            raise Exception('ERROR: There was a problem with one of your commands')

def insert_license(input_file):
    # Read data from file
    f = open(input_file, 'r')
    html = f.read()
    f.close()
    license_text = '''<!--
#####################       A U T H O R       ##########################
#                                                                      #
#   Copyright 2010 Jack Desert                                         #
#   <JackDesert@gmail.com>                                             #
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
-->\n'''
    html = license_text + html
    f = open(input_file, 'w')
    f.write(html)
    f.close()



file_list = ['changelog.lyx', 'devguide.lyx', 'index.lyx', 'userguide.lyx']
for in_doc in file_list:
    out_doc = '../' + in_doc[0:-4] + '.html'
    command_list = ['elyxer --nofooter --css style.css ' + in_doc + ' ' + out_doc,
        'rm -f ' + in_doc + '~']
    process_commands(command_list)
    insert_license(out_doc)
