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
from handle_exceptions import handle_general_error


def find_local_image_tag(in_html, ELYXER_ENGINE):
    if(ELYXER_ENGINE):
    # eLyXer img tags looks something like this:
    # <img class="embedded" src="rv-8_tiny.jpg" alt="figure rv-8_tiny.jpg" style="max-width: 2048px; max-height: 1536px; "/>
    # Notice ELYXER uses double quotes instead of single quotes within the tag.
        img_exp = re.compile('''
            <img\ class="embedded"\          # The beginning of an <img> tag -- note two escaped spaces
            src="           # Note use of double quotes instead of single
            (?!http://)     # Negative lookahead expression (if it has http:// it's already been changed to web reference)
            ..*?            # Non-greedy (short as possible match) of stuff in middle
            />              # The closing of the <img> tag
            ''', re.VERBOSE)
    else:
    # INTERNAL img tags look something like this:
    # <img src='0_home_jd_Escritorio_rv-8_tiny.jpg' alt='image: 0_home_jd_Escritorio_rv-8_tiny.jpg' />
        img_exp = re.compile('''
            <img\ src='     # The beginning of an <img> tag -- note the escaped space in the verbose regex
            (?!http://)     # Negative lookahead expression (if it has http:// it's already been changed to web reference)
            ..*?            # Non-greedy (short as possible match) of stuff in middle
            />              # The closing of the <img> tag
            ''', re.VERBOSE)

    img_obj = img_exp.search(in_html)
    img_tag = ''
    if(img_obj):
        img_tag = img_obj.group()
    return(img_tag)



def up_images(in_html, wp_client_obj, ELYXER_ENGINE, in_DIR_OFFSET):
    # Find local location of a single image within the (x)html file
    img_tag = find_local_image_tag(in_html, ELYXER_ENGINE)
    imageSrc = None
    if(img_tag):
        pr3 ("\nIMAGES\nLet's upload your images")
    while(img_tag):
        local_image_url = get_local_image_url(img_tag, ELYXER_ENGINE)
        valid_local_image_url = validate_url(local_image_url, in_DIR_OFFSET)

        filesize = str(os.path.getsize(valid_local_image_url) / 1024) + ' kB'
        short_name = get_short_name(valid_local_image_url)
        pr3("Uploading image: " + short_name + '.  Size: ' + filesize )
        # upload image for post
        try:
            imageSrc = wp_client_obj.newMediaObject(valid_local_image_url)
        except (gaierror, WordPressException):
            handle_gaierror()
        try:
            assert(imageSrc.startswith('http://'))
        except AssertionError:
            print("There was a problem uploading your image.")
            print("imageSrc should start with http://")
            print("Please contact the author at jackdesert556@gmail.com")
            handle_general_error()
        try:
            assert(local_image_url in in_html)
        except AssertionError:
            print("There was a problem uploading your image.")
            print("local_image_url not found in in_html")
            print("Please contact the author at jackdesert556@gmail.com")
            handle_general_error()
        in_html = in_html.replace(local_image_url, imageSrc)
        try:
            assert(local_image_url not in in_html)
        except AssertionError:
            print("There was a problem uploading your image.")
            print("local_image_url still in in_html after upload")
            print("Please contact the author at jackdesert556@gmail.com")
            handle_general_error()
        img_tag = find_local_image_tag(in_html, ELYXER_ENGINE)
    return(in_html)

# FIND local_image DIRECTORY
# Look for either backslash (win32) or forslash (everything else)
# to find directory where images reside
def get_dir_offset(in_input_file):
    directory = ''
    if (sys.platform == 'win32'):
        input_exp = re.compile('..{1,}\\\\')   # Greedy to catch full folder
    else:
        input_exp = re.compile('..{1,}/')   # Greedy to catch full folder
    input_obj = input_exp.match(in_input_file) # Must match at beginning of expression
    if (input_obj):
        directory = input_obj.group()
    return directory


# The function 'validate_url' makes sure that the url that we feed the wordpress
# blog is valid. If it receives an absolute url like
# /home/name/folder/file.jpg
# then it passes the input to the output.
# If it receives a relative url like
# image_dir/pic.jpg
# or
# ../another_folder/pic.jpg
# This it adds the in_dir_offset to this relative url for output
def validate_url(in_url, in_dir_offset):
    # If the url is already absolute (starts with a forward slash or
    # something like c:\ or d:\, leave it as be
    if in_url.startswith('/') or in_url[1:3] == ':\x0c':  # A colon and the unicode for a backslash
        return in_url
    # Otherwise, just append the local url to the dir_offset for a
    else:
        return (in_dir_offset + in_url)


def get_local_image_url(img_tag, ELYXER_ENGINE):
    # Find local address of image
    # The only difference between the two is single vs double quotes
    if (ELYXER_ENGINE):
        add_exp = re.compile('''
            src="   # The beginning of the address
            ..*?    # Non-greedy rest of the address
            "       # The (first) closing (double) quotation mark
            ''', re.VERBOSE)
    else:
        add_exp = re.compile('''
            src='   # The beginning of the address
            ..*?    # Non-greedy rest of the address
            '       # The (first) closing (single) quotation mark
            ''', re.VERBOSE)
    add_obj = add_exp.search(img_tag)
    if (add_obj == None):
        pr3 ("Error parsing img tag: " + img_tag)
        msg = "LyXBlogger failed to find src attribute in <img> tag"
        raise Exception(msg)
    long_address = add_obj.group()
    short_address = long_address[5:-1]  # Strip off the src="
    return(short_address)

def get_short_name(valid_url):
    if (sys.platform == 'win32'):
        separator = '\\\\'
    else:
        separator = '/'
    short_name = valid_url.split(separator)[-1]
    return (short_name)
