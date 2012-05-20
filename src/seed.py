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

import sys, os, re, time
import wordpresslib
import getpass
from socket import gaierror
from wordpresslib import WordPressException
from exceptions import IndexError

from LyxBlog.image import up_images
from LyxBlog.image import get_dir_offset
from LyxBlog.term import term_open
from LyxBlog.misc import pr3
from LyxBlog.misc import wait_for_consumer
from LyxBlog.handle_exceptions import handle_general_error
from LyxBlog.handle_exceptions import handle_gaierror
from LyxBlog.handle_exceptions import handle_input_error
from LyxBlog.cat import get_post_id
from LyxBlog.cat import get_cat_id
from LyxBlog.parsing import get_html
from LyxBlog.profiles import get_credentials
from LyxBlog.profiles import run_init_config

def main():
    error_msg = ''
    input_file = sys.argv[1]    # Incoming file name
    # DIR_OFFSET is where the file being called is relative to where your shell is open to
    DIR_OFFSET = ''            # Empty until defined otherwise

    # Open LyXBlogger in a separate terminal
    term_open(input_file)

    pr3 ('LYXBLOGGER')
    pr3('Copyright 2010 - 2012 Jack Desert')
    pr3('Please send any comments, suggestions, or bug reports')
    pr3('to jackdesert@gmail.com')
    pr3 ('License: GNU GPL3. See <http://www.gnu.org/licenses>')
    pr3('Documentation at http://lyxblogger.nongnu.org\n')
    config = run_init_config()
    time.sleep(config.getfloat('DEFAULT', 'delay'))

    DIR_OFFSET = get_dir_offset(input_file)

    html, blog_title, ELYXER_ENGINE = get_html(input_file, config.get('DEFAULT', 'cut_flag'))

    keys = get_credentials(config)

    wordpress_url = keys.url
    user = keys.user
    password = keys.password

    # prepare client object
    wp = wordpresslib.WordPressClient(wordpress_url, user, password)

    # select blog id
    pr3('\nNEW OR EXISTING')
    while (1):
        pr3('Create New post or overwrite Existing? (N) E')
        cat_response = sys.stdin.readline().replace('\n', '')
        if cat_response == 'E' or cat_response == 'e':
            post_id = get_post_id(wp)
            break
        elif cat_response == 'N' or cat_response == 'n' or cat_response == '':
            post_id = 0
            pr3('Publishing new post')
            break
        else:
            pr3 ("Response Not Understood.\n")
    try:
        wp.selectBlog(post_id)
    except (gaierror, WordPressException):
        handle_gaierror()

    # create post object
    post = wordpresslib.WordPressPost()
    post.title = blog_title

    cat_id = get_cat_id(wp)
    # I have no idea why this takes a tuple (something, )
    post.categories = cat_id #(cat_id,)
    # publish images
    html = up_images(html, wp, ELYXER_ENGINE, DIR_OFFSET)
    post.description = html
    # publish post
    pr3 ("\nWORDS\nLet's upload your thoughts")
    
    filesize = str(os.path.getsize(input_file) / 1024) + ' kB'
    pr3("Uploading xhtml: " + input_file + '.  Size: ' + filesize )
    try:
        if(post_id == 0):
            wp.newPost(post, True)
        else:
            wp.editPost(post_id, post, True)
    except (gaierror, WordPressException):
        handle_gaierror()

    pr3 ('\nSUCCESS!')
    pr3 ('You just published your document to ' + wordpress_url[7:-11])
    pr3 ('Thank you for using LyXBlogger.\n\n')
    wait_for_consumer()


if __name__ == '__main__':
    try:
        main()
    except IndexError:
        handle_input_error()
    except SystemExit:
        pass    # Let this exception pass through so sys.exit() calls will work
    except:
        handle_general_error()


