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
import sys, os, traceback
from socket import gaierror
from misc import pr3
from misc import wait_for_consumer

def handle_general_error(name_string = '', suggestion_string = ''):
    pr3('\nAn error has occurred. If this error persists, please ')
    pr3('contact the author at jackdesert556@gmail.com.')
    pr3('The nutshell version is listed way down below. But here')
    pr3('are the details if you are interested:')
    print(traceback.print_exc())
    print('\n\n\n\n\n')
    print("\n************************************************************")
    if name_string == '':
        print("*******                     ERROR                    *******\n")
    else:
        print (name_string)
    exc_type, exc_value, exc_traceback = sys.exc_info()
    msg = traceback.format_exception_only(exc_type, exc_value)[0].replace('\n', '')
    print("System says: " + msg)
    if suggestion_string != '':
        print (suggestion_string + '\n')
    wait_for_consumer()


def handle_gaierror():
    name = ''
    suggestion = ''
    exc_type, exc_value, exc_traceback = sys.exc_info()
    msg = traceback.format_exc()
    if ('[Errno -2] Name or service not known' in msg):
        name = "*******               CONNECTION ERROR               *******\n"
        suggestion = "Please check your Internet connection and try again.\n"
        suggestion += "If your Internet connection is fine, make sure you typed\n"
        suggestion += "your domain correctly."
    if ('Bad login/pass combination' in msg):
        name = "*******           USERNAME / PASSWORD ERROR          *******\n"
        suggestion = "Make sure you are typing your username and password correctly.\n"
        suggestion += "Hint: is caps lock on?"
        suggestion += "Hint: are you uploading to the correct site?"
    handle_general_error(name, suggestion)

def handle_input_error():
    name = ''
    suggestion = ''
    exc_type, exc_value, exc_traceback = sys.exc_info()
    msg = traceback.format_exc()
    if ('input_file = sys.argv[1]' in msg) and ('IndexError: list index out of range' in msg):
        name = "*******                 INPUT ERROR                  *******\n"
        suggestion = "Most likely LyXBlogger was called without sufficient arguments.\n"
        suggestion += "Usage is:\n"
        suggestion += "     $ python -m lyxblogger <input_file>."
    handle_general_error(name, suggestion)
