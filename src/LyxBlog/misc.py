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

# Miscellaneous functioncs used by LyXBlogger
import sys, time, re

def pr3(input):
    # Use sys.stdout instead of print so results can be used for automated testing
    # For some reason a newline character is required to flush ?
    # That's okay, because we'll use str.rstrip on the other side
    input = str(input)  # This makes sure that anything printable can be passed through
    sys.stdout.write(input + '\n')
    # Each line must be flushed so it can be read by the other side.
    sys.stdout.flush()

def wait_for_consumer():
    if (sys.platform == 'win32'):
        pr3('\nPress ENTER to close LyXBlogger.')
    elif(sys.platform == 'darwin'):
        pr3("\nFN + SHIFT + UP_ARROW scrolls screen        ENTER closes LyXBlogger")
    else:
        pr3("\nSHIFT + PAGE UP scrolls screen        ENTER closes LyXBlogger")
    sys.stdin.readline()
    sys.exit(0)  # Call this to make sure the program ends

def get_format(in_html):
    exp = re.compile('<head>.*</head>', re.DOTALL)   # DOTALL makes '.' match newlines as well
    format_obj = exp.search(in_html)
    if (format_obj):
        html_head = format_obj.group()
        if '<meta name="GENERATOR" content="LyX' in html_head:
            pr3("You are using the LyXHTML format.")
            pr3("LyXBlogger also supports the eLyXer format.")
            pr3("For more information, see the user's guide at lyxblogger.nongnu.org.")
            return False    # False means LyxHTL format
        elif '<meta name="generator" content="http://www.nongnu.org/elyxer/"/>' in html_head:
            pr3("You are using the eLyXer format.")
            pr3("LyXBlogger also supports LyX 2.0's internal LyXHTML format.")
            pr3("For more information, see the user's guide at lyxblogger.nongnu.org.")
            return True     # True means eLyXer format
        elif '<META name="GENERATOR" content="hevea' in html_head:
            pr3('*****   ERROR:   Unsupported format:  Hevea   *****')
        elif '<!--Converted with LaTeX2HTML' in html_head:
            pr3('*****   ERROR:   Unsupported format:  LaTeX2HTML   *****')
        elif '<meta name="GENERATOR" content="TtH' in html_head:
            pr3('*****   ERROR:   Unsupported format:  TtH   *****')
        else:
            pr3('*****   ERROR:   Unknown file format.   *****')
    else:
        pr3('\n\nNo <head> tag found')

    pr3("LyXBlogger supports the eLyXer format and LyX 2.0's internal")
    pr3("LyXHTML format. The input file you provided appears to be neither of")
    pr3("these. For more information, see the user's guide at lyxblogger.nongnu.org.")
    sys.exit(0)     # Halt Program if invalid html found.


def trim_cut_material(html, CUT_FLAG, ELYXER_ENGINE):
    # This function removes after the CUT_FLAG. CUT_FLAG is user-
    # definable. Note that the CUT_FLAG must be found at the beginning
    # of a paragraph to be rcognized
    pr3 ("\nCUT FLAG")
    pr3 ("Anything placed after the cut flag in your document will not be uploaded.")
    pr3 ("This is helpful for keeping notes that you might put back in a later draft.")
    if(ELYXER_ENGINE):
        # ELYXER may put a <span> tag in if you change the size
        exp = re.compile('<div class="[^>]{1,}?">\n(<span class="\D{1,}?">){0,1}?' + CUT_FLAG)
    else:
        # INTERNAL uses a magicparlabel-num
        exp = re.compile('<div class="[^>]{1,}?"><a id=\'magicparlabel-\d{1,}\' />\n' + CUT_FLAG)

    srch_obj = exp.search(html)
    if(srch_obj):
        start_index = srch_obj.start()
        # pr3('start index is: ' + str(start_index))
        # pr3('this expression found at location: ' + str(start_index))
        html = html[0:start_index]
        pr3 ('The Following String was found in your document and was ')
        pr3 ('successfully used as a cut flag: ')
        pr3 (CUT_FLAG + '\n')
    else:
        pr3 ("Place the contents of the following line at the beginning of")
        pr3 ("a paragraph to use it as a cut flag: ")
        pr3 (CUT_FLAG)
    return(html)

