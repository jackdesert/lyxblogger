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

import sys, os
from misc import pr3



def new_shell():
    # Determine which operating system is in use
    system = sys.platform
    if (sys.platform == 'win32'):
        pr3('Running on Windows')
        return('start "LyXBlogger" python.exe %s %s %s ')
    elif (sys.platform == 'darwin'):
        pr3('Running on OSX')
    elif (sys.platform == 'linux2'):
        pr3('Running on GNU/Linux')
    else:
        pr3('I\'m not sure what operating system you are running on.')
        pr3('Please write the author at jackdesert@gmail.com to report possible bug')
    # GNU/Linux, Mac, and unidentified OS's call xterm
    return('xterm -T "LyXBlogger" -fg gold -bg black -fn 10x20 -e python %s %s %s ')


def term_open(in_input_file):

    CALLED_FROM_XTERM = '--run-here'
    CALL_MODULE = '-m lyxblogger'
    # If already called from xterm, run the program as normal.
    # Otherwise, call the program from xterm so it's visible
    if (len(sys.argv) >= 3) and (sys.argv[2] == CALLED_FROM_XTERM):
        pass    # Called correctly, so code will execute
    else:
        # Spawn a new xterm window to run this program in
        # -hold means leave window open after process completes
        # -fg is foreground color
        # -bg is background color
        # -fn is font (size)
        # -e means call a program
        command = new_shell() % (CALL_MODULE, in_input_file, CALLED_FROM_XTERM)
        pr3('command is ' + command)
        os.system(command)
        sys.exit(0)     # Exit so program is not repeated.
        # Anything below this will not be executed



