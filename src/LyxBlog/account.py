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
import re, pdb

class Account:
    HTTP_BEGINNING = 'http://'
    TAG_ENDING = '/xmlrpc.php'

    def __init__(self, url, username, password):
        self.__url = self.__format_url(url)
        self.__username = username
        self.__password = password 
        self.__section_id = None
        self.__verify_init()

    def __eq__(self, other):
        return self.__url == other._Account__url and self.__username == other._Account__username and self.__password == other._Account__password

    def __verify_init(self):
        assert(isinstance(self.__url, str)), 'Account url must be a string'
        assert(isinstance(self.__username, str)), 'Account username must be a string'
        assert(isinstance(self.__password, str) or self.__password is None), 'Account password, if present, must be a string'

    def set_section_id(self, id):
        self.__section_id = id

    def set_password(self, password):
        self.__password = password

    def __format_url(self, url):
        base = url.replace(Account.HTTP_BEGINNING, '')
        base = re.subn(r'^www\.', '', base)[0]
        base = base.replace(Account.TAG_ENDING, '')
        if base.endswith('/'):
            base = base[:-1]
        return base

    def get_section_id(self):
        return self.__section_id

    def get_password(self):
        return self.__password

    def get_url(self):
        return self.__url

    def get_full_url(self):
        return Account.HTTP_BEGINNING + self.__url + Account.TAG_ENDING
        
    def get_username(self):
        return self.__username

