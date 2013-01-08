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

import re
from display import Display
from account import Account
from account_manager import AccountManager

class LyXBlogger:
    def __init__(self, input_file):
        self.__display = Display()
        self.__state = 0
        self.__state_chain = ['ask', 'receive']
        # self.__entry = Entry(input_file)
        # self.__transmitter = Transmitter()
        self.__manager = AccountManager()

    def start(self):
        self.__welcome()
        self.__ensure_title()
        self.__verify_which_account()
        self.__verify_create_new_or_overwrite()
        self.__transmit()
        self.__closing_remarks()

    def __verify_which_account(self):
        dd = self.__display
        mm = self.__manager
        accounts = mm.get_accounts()
        recent_id = mm.get_recent_id()
        while(1):
            response_with_case = dd.ask_which_account(accounts, recent_id)
            response = response_with_case.lower()
            if response == 'd':
                account_id = dd.ask_which_account(accounts, True)
                mm.delete_account_by_id(int(account_id))
            elif response == 'n':
                username = dd.ask_for_new_username()
                url = dd.ask_for_new_url()
                password = dd.ask_for_new_password()
                new_account = Account(url, username, password)
                mm.add_account(new_account)
            elif response == '':
                account_id = -1 # negative indicates whatever was last used
                return mm.get_recent_account()
            elif re.compile('^\d+$').match(response):
                account_id = int(response)
                return mm.get_account_by_id(account_id)
            else:
                dd.print_unrecognized_response(response_with_case)


    def __ensure_title(self):
        return 0
    def __transmit(self):
        return 0
    def __verify_create_new_or_overwrite(self):
        return 0
    def __welcome(self):
        return 0
    def __closing_remarks(self):
        return 0


