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
#########   U S E R    D E F I N E D    V A R I A B L E S   ############

AUTO_URL = 'http://blogtest.letseatalready.com'                        #
AUTO_USER = 'test'                                                     #
AUTO_PASSWORD = 'test'                                                 #
AUTO_LOGIN = True                                                      #
CUT_FLAG = '#! CUT MATERIAL'                                           #
DELAY = 1.0
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

def main(keys):
    error_msg = ''
    input_file = sys.argv[1]    # Incoming file name
    # DIR_OFFSET is where the file being called is relative to where your shell is open to
    DIR_OFFSET = ''            # Empty until defined otherwise

    # Open LyXBlogger in a separate terminal
    term_open(input_file)

    pr3 ('LYXBLOGGER')
    pr3 ('Welcome to LyXBlogger, hosted at www.nongnu.org/lyxblogger')
    pr3 ('License: GNU GPL3. See <http://www.gnu.org/licenses>\n')

    pr3('AUTHOR')
    pr3('Copyright 2010 Jack Desert')
    pr3('Please send any comments, suggestions, or bug reports')
    pr3('to jackdesert556@gmail.com')
    pr3("Author's personal blog: www.LetsEATalready.com\n")
    time.sleep(DELAY)

    DIR_OFFSET = get_dir_offset(input_file)

    html, blog_title, ELYXER_ENGINE = get_html(input_file, keys.CUT_FLAG)

    pr3('\nDOMAIN')
    if (keys.AUTO_LOGIN == True):
        display_url = keys.AUTO_URL[0:-11]
        while True:
            pr3 ("Publish this document to " + display_url + "?   (Y) N")
            a = sys.stdin.readline()
            if (a == 'N\n' or a == 'n\n'):
                keys.AUTO_LOGIN = False
                break
            elif (a == 'Y\n' or a == 'y\n' or a == '\n'):
                wordpress_url = keys.AUTO_URL
                user = keys.AUTO_USER
                password = keys.AUTO_PASSWORD
                break
            else:
                pr3('Response not understood')

    if (keys.AUTO_LOGIN ==False):
        pr3 ("URL")
        pr3("Please enter your WordPress URL")
        pr3("Example: cool_site.wordpress.com")
        wordpress_url = sys.stdin.readline()
        wordpress_url = wordpress_url.replace('http://', '')
        wordpress_url = wordpress_url.replace('www.', '')
        wordpress_url = wordpress_url.replace('\n', '')
        wordpress_url = 'http://' + wordpress_url + '/xmlrpc.php'
        pr3 ("The page we'll be talking is " + wordpress_url)
        pr3 ("\nUSERNAME")
        pr3("Please enter your WordPress username")
        user = sys.stdin.readline().replace('\n', '')
        pr3("Username is " + user + '.')
        pr3 ("\nPASSWORD")
        pr3("Please enter your WordPress password")
        password = getpass.getpass()
        pr3 ("Thank you.")

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

    wp.selectBlog(post_id)


    # create post object
    post = wordpresslib.WordPressPost()
    post.title = blog_title

    cat_id = get_cat_id(wp)
    # I have no idea why this takes a tuple (something, )
    post.categories = (cat_id,)
    # publish images
    html = up_images(html, wp, ELYXER_ENGINE, DIR_OFFSET)
    post.description = html
    # publish post
    pr3 ("\nWORDS\nLet's upload your thoughts")
    filesize = str(os.path.getsize(input_file) / 1024) + ' kB'
    pr3("Uploading xhtml: " + input_file + '.  Size: ' + filesize )
    if(post_id == 0):
        wp.newPost(post, True)
    else:
        wp.editPost(post_id, post, True)


    pr3 ('\nSUCCESS!')
    pr3 ('You just published your document to ' + wordpress_url[7:-11])
    pr3 ('Thank you for using LyXBlogger.\n\n')
    wait_for_consumer()



class Credentials:
    def __init__(self, url, user, pw, auto_login, flag):
        if url.endswith('/'):
            self.AUTO_URL = url + 'xmlrpc.php'
        else:
            self.AUTO_URL = url + '/xmlrpc.php'
        self.AUTO_USER = user
        self.AUTO_PASSWORD = pw
        self.AUTO_LOGIN = auto_login
        self.CUT_FLAG = flag



if __name__ == '__main__':
    my_credentials = Credentials(AUTO_URL,
        AUTO_USER, AUTO_PASSWORD, AUTO_LOGIN, CUT_FLAG)
    try:
        main(my_credentials)
    except (gaierror, WordPressException):
        handle_gaierror()
    except IndexError:
        handle_input_error()
    except SystemExit:
        pass    # Let this exception pass through so sys.exit() calls will work
    except:
        handle_general_error()


