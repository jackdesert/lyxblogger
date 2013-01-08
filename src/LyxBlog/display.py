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

import sys, getpass, pdb

class Display:

    MARKER = "  **"

    def __init__(self):
        self.indent = 4 * ' ' 

    def __send(self, text):
        # Use sys.stdout instead of print so results can be used for automated testing
        # For some reason a newline character is required to flush ?
        # That's okay, because we'll use str.rstrip on the other side
        text = str(text)  # This makes sure that anything printable can be passed through
        sys.stdout.write(text + '\n')
        # Each line must be flushed so it can be read by the other side.
        sys.stdout.flush()
        return text

    def ask_for_new_username(self):
        self.__send('\nCREATING NEW PROFILE.')
        self.__send("\nUSERNAME")
        while (1):
            self.__send("Please enter your WordPress username")
            username = self.__get_response()
            if username != '': break
        self.__send("Username is " + username + '.')
        return username

    def ask_for_new_url(self):
        self.__send("\nURL")
        while (1):
            self.__send("Please enter your WordPress URL")
            self.__send("Example: cool_site.wordpress.com")
            url = self.__get_response()
            if url != '': break
        return url

    def ask_for_new_password(self):
        self.__send("\nPROMPT for PASSWORD?")
        self.__send("Press ENTER now to be prompted each time (recommended).")
        self.__send("Or type your precious password here, to be saved as plain text on you computer.")
        password = getpass.getpass()
        return password


    def print_format(self, in_format):
        return self.__print_arbitrary('Format', in_format)

    def print_title(self, in_title):
        return self.__print_arbitrary('Title', in_title)

    def print_word_count(self, in_count):
        return self.__print_arbitrary('Word Count', in_count)

    def print_image_count(self, in_count):
        return self.__print_arbitrary('Image Count', in_count)

    def ask_for_password(self):
         self.__send('Please enter your password')
         return self.__get_hidden_response()

    def ask_which_account(self, accounts, recent_id, delete=False):
        self.__print_accounts(accounts, recent_id, delete)
        return self.__get_response()

    def __print_accounts(self, accounts, recent_id, delete):
        msg =  'ACCOUNTS\n'
        if delete:
            msg += 'Enter the number next the the account to delete\n'
        else:
            msg += 'Enter the number next to the desired account.\n'
            msg += '(**latest) N = New, D = Delete'
        for account in accounts:
            msg += "\n{0}. {1}@{2}".format(account.get_section_id(), account.get_username(), account.get_url())
            if account.get_section_id() == recent_id: msg += Display.MARKER
        return self.__send(msg)

    def __get_response(self):
        return sys.stdin.readline().replace('\n', '')

    def __get_hidden_response(self):
        return getpass.getpass()


    def __print_arbitrary(self, label, text, indent_level=1):
        msg = self.indent * indent_level
        msg += "{0}: {1}".format(label, text)
        return self.__send(msg)
        
        

    def __indent(self, text):
        msg = self.indent + text
        return msg

    def print_unrecognized_response(self, response):
        msg = "\nUNRECOGNIZED RESPONSE: '{0}'".format(response) 
        return self.__send(msg)
        
