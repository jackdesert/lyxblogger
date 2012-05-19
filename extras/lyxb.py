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
#   Please see README.html for LyXBlogger documentation.               #
#   Alternatively, see the wiki page at                                #
#   http://wiki.lyx.org/Tools/LyXBlogger                               #
#   Please note the capitalization of the previous url.                #
#   Please submit any issues or suggestions to the author.             #
#                                                                      #
#####################       A U T H O R       ##########################
#                                                                      #
#   Copyright 2010 Jack Desert                                         #
#   <JackDesert@gmail.com>                                          #
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

AUTO_URL = 'http://blogtest.letseatalready.com/xmlrpc.php'             #
AUTO_USER = 'test'                                                     #
AUTO_PASSWORD = 'test'                                                 #
AUTO_LOGIN = True                                                      #
CUT_FLAG = '#! CUT MATERIAL'                                           #

########################################################################

import sys, os, re
import wordpresslib
import getpass
from socket import gaierror
from wordpresslib import WordPressException


import os, sys
import re
import wordpresslib

import sys, time, re

def pr3(input):
    # Use sys.stdout instead of print so results can be used for automated testing
    # For some reason a newline character is required to flush ?
    # That's okay, because we'll use str.rstrip on the other side
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
            pr3("For more information, see the user's guide at www.nongnu.org/lyxblogger.")
            return False    # False means LyxHTL format
        elif '<meta name="generator" content="http://www.nongnu.org/elyxer/"/>' in html_head:
            pr3("You are using the eLyXer format.")
            pr3("LyXBlogger also supports LyX 2.0's internal LyXHTML format.")
            pr3("For more information, see the user's guide at www.nongnu.org/lyxblogger.")
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
    pr3("these. For more information, see the user's guide at www.nongnu.org/lyxblogger.")
    return None

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
        pr3('start index is: ' + str(start_index))
        # pr3('this expression found at location: ' + str(start_index))
        html = html[0:start_index]
        pr3 ('The Following String was found in your document and was ')
        pr3 ('successfully used as a cut flag: ')
        pr3 (CUT_FLAG + '\n')
    else:
        pr3 ("Place the contents of the following line at the beginning of")
        pr3 ("a paragraph to use it as a cut flag: ")
        pr3 (CUT_FLAG + '\n')
    return(html)


def find_image_tag(in_html, ELYXER_ENGINE):
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
    img_tag = find_image_tag(in_html, ELYXER_ENGINE)
    imageSrc = None
    if(img_tag):
        pr3 ('IMAGES\nFirst We\'ll Upload Your Images')
    while(img_tag):
        image_url = get_image_url(img_tag, ELYXER_ENGINE)
        valid_image_url = validate_url(image_url, in_DIR_OFFSET)

        filesize = str(os.path.getsize(valid_image_url) / 1024) + ' kB'
        short_name = get_short_name(valid_image_url)
        pr3("Uploading image: " + short_name + '.  Size: ' + filesize )
        # upload image for post
        imageSrc = wp_client_obj.newMediaObject(valid_image_url)
        in_html = in_html.replace(valid_image_url, imageSrc)
        img_tag = find_image_tag(in_html, ELYXER_ENGINE)
    return(in_html)

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


def validate_url(in_url, in_dir_offset):
    # If the url is already absolute (starts with a forward slash or
    # something like c:\ or d:\, leave it as be
    if in_url.startswith('/') or in_url[1:3] == ':\x0c':  # A colon and the unicode for a backslash
        return in_url
    # Otherwise, just append the local url to the dir_offset for a
    else:
        return (in_dir_offset + in_url)


def get_image_url(img_tag, ELYXER_ENGINE):
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

import sys, os



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
        pr3('Please write the author at JackDesert@gmail.com to report possible bug')
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



import sys, os, traceback
from socket import gaierror

def handle_general_error(name_string = '', suggestion_string = ''):
    pr3('\nAn error has occurred. If this error persists, please ')
    pr3('contact the author at JackDesert@gmail.com.')
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

def main(keys):
    error_msg = ''
    input_file = sys.argv[1]    # Incoming file name
    # DIR_OFFSET is where the file being called is relative to where your shell is open to
    DIR_OFFSET = ''            # Empty until defined otherwise

    # Open LyXBlogger in a separate terminal
    term_open(input_file)

    pr3 ('LYXBLOGGER')
    pr3 ('Welcome to LyXBlogger')
    pr3 ('Author: Jack Desert')
    pr3 ('Website: LetsEATalready.com\n')

    DIR_OFFSET = get_dir_offset(input_file)

    # Read data from file
    f = open(input_file, 'r')
    html = f.read()
    f.close()

    pr3 ("FORMAT")
    ELYXER_ENGINE = get_format(html)
    if ELYXER_ENGINE == None:
        sys.exit(0)     # Halt Program if invalid html found.


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
        #~ pr3 ('Please notify the author at JackDesert@gmail.com to')
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

    html = trim_cut_material(html, keys.CUT_FLAG, ELYXER_ENGINE)

    if (keys.AUTO_LOGIN == True):
        display_url = keys.AUTO_URL[0:-11]
        pr3 ("Publish this document to " + display_url + "?   Y (N)")
        a = sys.stdin.readline()
        if (a == 'Y\n' or a == 'y\n'):
            wordpress_url = keys.AUTO_URL
            user = keys.AUTO_USER
            password = keys.AUTO_PASSWORD
        else:
            keys.AUTO_LOGIN = False

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
    wp.selectBlog(0)

    pr3 ('\nCATEGORY')
    pr3 ('Retrieving Categories From Server')
    cat_list = wp.getCategoryList()
    cat_counter = 1
    for cat in cat_list:
        pr3 (str(cat_counter) + '.  ' + cat.name)
        cat_counter += 1
    cat_id = None
    while (1):
        try:
            pr3 ('Please enter the NUMBER next to the category for this post')
            cat_response = sys.stdin.readline().replace('\n', '')
            cat = int(cat_response)
            cat_id = cat_list[cat-1].id
            pr3 ('Category Selected: ' + cat_list[cat-1].name + '\n')
            break
        except:
            pr3 ("Category Response Not Understood.\n")

    html = up_images(html, wp, ELYXER_ENGINE, DIR_OFFSET)

    # create post object
    post = wordpresslib.WordPressPost()
    post.title = blog_title
    post.description = html

    # I have no idea why this takes a tuple (something, )
    post.categories = (cat_id,)
    # publish post
    pr3 ('\nWORDS\nNow We\'ll Upload Your Thoughts')
    filesize = str(os.path.getsize(input_file) / 1024) + ' kB'
    pr3("Uploading xhtml: " + input_file + '.  Size: ' + filesize )
    idNewPost = wp.newPost(post, True)

    pr3 ('\nSUCCESS!')
    pr3 ('You just published your document to ' + wordpress_url[7:-11])
    pr3 ('Thank you for using LyXBlogger.\n\n')
    wait_for_consumer()



class Credentials:
    def __init__(self, url, user, pw, auto_login, flag):
        self.AUTO_URL = url
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


