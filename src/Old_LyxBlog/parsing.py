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

import os, sys
import re
import wordpresslib
from misc import pr3
from misc import get_format
from misc import trim_cut_material

def get_html(input_file, CUT_FLAG):

    # Read data from file
    f = open(input_file, 'r')
    html = f.read()
    f.close()

    pr3 ("FORMAT")
    ELYXER_ENGINE = get_format(html)

    # Trim designated cut material from bottom of post
    html = trim_cut_material(html, CUT_FLAG, ELYXER_ENGINE)

    # RECORD TITLE FROM HEADER TO USE AS POST
    tit_exp = re.compile('''
        <title>         # Start of the <title> tag
        ..{1,}?         # Anything in the middle (non-greedy)
        </title>        # Closing </title> tag
        ''', re.VERBOSE)    # VERBOSE allows ''' '''
    tit_obj = tit_exp.search(html)
    # eLyXer uses 'Converted document' as the default title in the head
    # and body. LyXHTML uses 'LyX Document' as the default, but only
    # puts it in the head. The following code detects these default
    # titles and asks for a real title
    TITLE_EXPECTED_IN_BODY, TITLE_PROMPT = False, True
    pr3 ("\nTITLE")
    if(tit_obj):
        TITLE_EXPECTED_IN_BODY = True
        TITLE_PROMPT = False
        full_title_tag = tit_obj.group()
        blog_title = full_title_tag[7:-8]   # Strip tags off
        if (blog_title == 'Converted document'):    # eLyXer's default (head and body)
            TITLE_PROMPT = True
        if (blog_title == 'LyX Document'):  # LyXHTML's default (only in head)
            TITLE_PROMPT = True
            TITLE_EXPECTED_IN_BODY = False
    if(TITLE_PROMPT):
        pr3 ('No title found in document.')
        pr3 ('Please enter a title now')
        blog_title = sys.stdin.readline().replace('\n', '')
    pr3 ('Using title: ' + blog_title)

    # REMOVING TITLE FROM BODY
    # Typical body title using ENGINE_INTERNAL:
    #   <h1 class="title"><a id='magicparlabel-309' />
    #   Example Article Title</h1>
    #   <h1 class="title">
    # Typical body title using ELYXER_ENGINE using optional sizing:
    #   <h1 class="title">
    #   <span class="footnotesize">Hi Brian</span>
    #
    #   </h1>
    exp = re.compile('''
        <h1\                   # Beginning of tag with space
        class="title">         # The rest of the tag
        ..{1,}?                # Anything (non-greedy)
        </h1>                  # Closing tag
        ''', re.VERBOSE | re.DOTALL)                 # .. can include linebreaks
    bt_obj = exp.search(html)
    if(bt_obj):
        entire_bt_tag = bt_obj.group()
        html = html.replace(entire_bt_tag, '')
    elif (TITLE_EXPECTED_IN_BODY):
        pass
        #~ pr3 ('\nWARNING! The title of your entry may appear twice.')
        #~ pr3 ('Please notify the author at jackdesert556@gmail.com to')
        #~ pr3 ('have this bug squashed.\n\n Press Enter to continue uploading.')
        #~ sys.stdin.readline()
        # What this really means is an opening title tag was found, but
        # no title tag was found in the body.

    # Eliminate everything outside the <body></body> tags
    START_TAG = '<body>'
    END_TAG = '</body>'
    if (START_TAG in html):
        html = html.partition(START_TAG)[2]
    html = html.partition(END_TAG)[0]

    # Reinvoke <code> and </code> tags from their escape sequence counterparts
    html = html.replace('&lt;code&gt;', '<code>')
    html = html.replace('&lt;/code&gt;', '</code>')

    # Remove Arrows from footnotes and margin notes
    html = html.replace('[→', '[')
    html = html.replace('→]', ']')

    return html, blog_title, ELYXER_ENGINE

