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

    DEFAULT_ACCOUNT_ID = 0

    def __init__(self):
        self.__configpath  = self.__set_configpath()
        self.__config      = self.__init_config()
        self.__default_account = self.__create_default_account()
        self.__accounts    = []
        self.__load_accounts_from_config()

    def reset_config(self):
        self.__accounts = []
        if os.path.exists(self.__configpath):
            os.remove(self.__configpath)
        self.__config = self.__init_config()



    def __load_accounts_from_config(self):
        for section in self.__config.sections():
            section_id = self.__next_id()
            url = self.__config.get(section, 'url')
            username = self.__config.get(section, 'username')
            password = self.__config.get(section, 'password')
            new_account = Account(url, username, password)
            new_account.set_section_id(section_id)
            self.add_account(new_account)

    def get_accounts(self):
        return [self.__default_account] + self.__accounts

    def add_account(self, account):
        account.set_section_id(self.__next_id())
        self.__accounts.append(account)
        self.__add_account_to_config(account)

    def __next_id(self):
        return len(self.__accounts) + 1

    def __add_account_to_config(self, account):
        id = int(account.get_section_id()) # This will throw an exception if it's not a number
        id = str(id)
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

    def __create_default_account(self):
        # we are not going to set the id, because we never save this
        url = 'blogtest.letseatalready.com'
        username = 'test'
        password = 'test'
        default_account = Account(url, username, password)
        default_account.set_section_id(AccountManager.DEFAULT_ACCOUNT_ID)
        return default_account

    def get_recent_account(self):
        id = self.get_recent_id()
        id = int(id)
        return self.get_account_by_id(id)

    def __record_recent_account(self, id):
        self.__config.set('DEFAULT', 'last_profile', str(id))
        self.__save_config_to_file()

    def get_recent_id(self):
        id = self.__config.get('DEFAULT', 'last_profile')
        return int(id) 

    def get_account_by_id(self, id):
        self.__record_recent_account(id)
        if id == 0: return self.__default_account
        return self.__accounts[id - 1]
    
    def delete_account_by_id(self, id):
        offset_id = id - 1
        del self.__accounts[offset_id]
        self.__renumber_accounts()

    def __renumber_accounts(self):
        counter = 1
        renumbered_accounts = []
        for account in self.get_accounts():
            account.set_section_id(counter)
            counter += 1 
            renumbered_accounts.append(account)
        self.__accounts = renumbered_accounts
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
