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

import ConfigParser
from ConfigParser import DuplicateSectionError
import sys, os, pdb
from account import Account

class AccountManager:
    def __init__(self):
        self.__configpath  = self.__set_configpath()
        self.__config      = self.__init_config()
        self.__accounts    = []
        self.__load_accounts_from_config()

    def reset_config(self):
        self.__accounts = []
        if os.path.exists(self.__configpath):
            os.remove(self.__configpath)
        self.__config = self.__init_config()



    def __load_accounts_from_config(self):
        for section in self.__config.sections():
            url = self.__config.get(section, 'url')
            username = self.__config.get(section, 'username')
            password = self.__config.get(section, 'password')
            self.add_account(url, username, password)

    def get_accounts(self):
        return self.__accounts

    def add_account(self, url, username, password):
        section_id = self.__next_id()
        new_account = Account(section_id, url, username, password)
        self.__accounts.append(new_account)
        self.__add_account_to_config(new_account)

    def __next_id(self):
        return len(self.__accounts) + 1

    def __add_account_to_config(self, account):
        id = str(account.get_section_id())
        try:
            self.__config.add_section(id)
        except DuplicateSectionError:
            # No need to add it if it's already there
            message = 'a ok'

        self.__config.set(id, 'url', account.get_url())
        self.__config.set(id, 'username', account.get_username())
        self.__config.set(id, 'password', account.get_password())
        self.__save_config_to_file()

    def __save_config_to_file(self):
        with open(self.__configpath, 'wb') as handle: 
            self.__config.write(handle)

    def __init_config(self):
        config = ConfigParser.ConfigParser()
        if not os.path.exists(self.__configpath):
            # Set up initial config file
            config.set('DEFAULT', 'delay', '1.0') # wait while showing author info
            config.set('DEFAULT', 'cut_flag', '#! CUT MATERIAL') # we remove anything after this in the html
            config.set('DEFAULT', 'last_profile', '0') # use as default input option
            config.set('DEFAULT', 'next_section_n', '1') # next usable profile section number
            with open(self.__configpath, 'wb') as f: config.write(f)
        config.read(self.__configpath)
        return config


    def __set_configpath(self):
        # Determine which operating system is in use
        platform = sys.platform
        linux_relative_path = "~/.lyxblogger/config.cfg"
        try:
            relative_configpath = {'win32' : "~\\lyxblogger\\config.cfg", 
                              'darwin' : "~/.lyxblogger/config.cfg",
                              'linux2' : linux_relative_path,
                              'linux3' : linux_relative_path}[platform]
        except KeyError:
            raise SystemNotFoundError(platform)
        configpath = os.path.expanduser(relative_configpath)
        configdir = os.path.dirname(configpath)
        if not os.path.exists(configdir): os.makedirs(configdir)
        return configpath




class SystemNotFoundError(Exception):
    def __init__(self, system_found):
        self.system_found = system_found
        self.msg = '''Your operating system was not recognized. 
            Expected sys.platform to return either 'win32', 'darwin', or 'linux2'. 
            Yours returned '{0}'.'''.format(system_found)

if __name__ == '__main__':
  a = AccountManager()
