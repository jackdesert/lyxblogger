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
########################################################################

import sys, os, time, ConfigParser, xmlrpclib
import getpass
from misc import pr3
from misc import wait_for_consumer
from socket import gaierror
from xmlrpclib import Fault as xmlFault
from xmlrpclib import ProtocolError as xmlrpcProtocolError

def get_configpath():
    # Determine which operating system is in use
    system = sys.platform
    if (system == 'win32'):
        pr3('Running on Windows')
        return("~\\lyxblogger\\config.cfg")
    elif (system == 'darwin'):
        # pr3('Running on OSX')
        return "~/.lyxblogger/config.cfg"
    elif (system == 'linux2'):
        # pr3('Running on GNU/Linux')
        return "~/.lyxblogger/config.cfg"
    else:
        pr3('I\'m not sure what operating system you are running on.')
        pr3('Please write the author at jackdesert556@gmail.com to report possible bug')
        wait_for_consumer()
    # GNU/Linux, Mac, and unidentified OS's call xterm




def run_init_config():
    rel_file = get_configpath()
    abs_file = os.path.expanduser(rel_file)
    configdir = os.path.dirname(abs_file)
    if not os.path.exists(configdir): os.makedirs(configdir)
    config = init_config(abs_file)
    return config

def init_config(in_config_file):
    config = ConfigParser.ConfigParser()
    if not os.path.exists(in_config_file):
        # Set up initial config file
        config.set('DEFAULT', 'delay', '1.0') # wait while showing author info
        config.set('DEFAULT', 'cut_flag', '#! CUT MATERIAL') # we remove anything after this in the html
        config.set('DEFAULT', 'last_profile', '0') # use as default input option
        config.set('DEFAULT', 'next_section_n', '1') # next usable profile section number
        with open(in_config_file, 'wb') as configfile: config.write(configfile)
        pr3 ("Default config file created in " + in_config_file + '\n' )

    config.read(in_config_file)
    return config

def display_profiles(config):
    last_serial = config.get('DEFAULT', 'last_profile')

    disp_0 = '0. ' + str(Credentials.defaults())
    if last_serial == '0':
        disp_0 += "  **"
    pr3(disp_0)
    config_ctr = 1  # Zero is reserved for the test site, so we start one higher
    cfg_dict = {'0':'0'}  # This is to make sure the test site is reachable
    for section in config.sections():
        cfg_dict[str(config_ctr)] = section
        disp = str(config_ctr) + '. ' + str(Credentials.fromconfig(config,section))
        if section == last_serial:
            disp += "  **"
        pr3(disp)
        config_ctr += 1
    return cfg_dict

def get_serial(key, dict):
    if key.isdigit():
        try:
            return dict[key]
        except KeyError:
            # pr3("No such profile")
            # pr3("you entered: " + key)
            # pr3(dict)
            return None
    else:
        return None

def get_credentials(config):
    configpath = os.path.expanduser(get_configpath())

    # Select existing profile (and setting last_profile to that)
    # or create a new profile in the config file
    while (1):
        pr3 ('\nPROFILES')
        cfg_dict = display_profiles(config)

        last_serial = config.get('DEFAULT', 'last_profile')
        pr3 ('\nEnter the number next to the desired profile.')
        pr3 ('(**latest) N = New, D = Delete')
        cat_response = sys.stdin.readline().replace('\n', '')

        if cat_response == 'D' or cat_response == 'd':
            cfg_dict = display_profiles(config)
            pr3 ('Enter a number to delete that profile, N to cancel')
            del_response = sys.stdin.readline().replace('\n', '')
            d_serial = get_serial(del_response, cfg_dict)
            if del_response == '0':
                pr3 ('Default section 0 cannot be deleted\n')
                pr3("Keyboard control will resume in 5 seconds")
                time.sleep(3)
            elif d_serial:
                config.remove_section(d_serial)
                if d_serial == config.get('DEFAULT', 'last_profile'):
                    config.set('DEFAULT', 'last_profile', '0')
                with open(configpath, 'wb') as configfile: config.write(configfile)
                pr3 ('Profile ' + del_response + ' removed!\n')
            else:
                pr3 (del_response + " Is Not A Profile Number.\n")

        elif cat_response == 'N' or cat_response == 'n':
            section = config.get('DEFAULT', 'next_section_n')
            new = Credentials.ask()
            pr3("Your password is: " + len(new.password)*"*")
            if url_passes(new, new.password):
                config.set('DEFAULT', 'last_profile', section)
                config.add_section(section)
                config.set(section, 'url',      new.url)
                config.set(section, 'user',     new.user)
                config.set(section, 'password', new.password)                # make a previously unused number to be used by the next section created:
                config.set('DEFAULT', 'next_section_n', str(int(section)+1))
                with open(configpath, 'wb') as configfile: config.write(configfile)
                pr3 ("Profile created, config file saved to " + configpath + '\n')
            else:
                time.sleep(3)
        # USE THIS PROFILE
        elif get_serial(cat_response, cfg_dict) or cat_response == '':
            if cat_response == '':
                u_serial = config.get('DEFAULT', 'last_profile')
            else:
                u_serial = get_serial(cat_response, cfg_dict)
            selected = Credentials.fromconfig(config, u_serial)
            config.set('DEFAULT', 'last_profile', u_serial)
            with open(configpath, 'wb') as configfile: config.write(configfile)
            break

        else:
            pr3 ("Response " + cat_response + " Not Understood.\n")
            time.sleep(1)

    pr3 ('Profile selected:  ' + str(selected))
    if selected.password == '':
            pr3 ("Profile has no password set. Please enter your WordPress password")
            selected.password = getpass.getpass()
    # Repeat process until credentials pass
    while not url_passes(selected, CHECK_PASSWORD = True):
        selected = get_credentials(config)

    pr3("Credentials Passed")
    return selected

def url_passes(selected, CHECK_PASSWORD = False):
    # prepare client object
    # verify that credentials work by getting info
    if CHECK_PASSWORD == False or CHECK_PASSWORD == '':
        pr3("Making sure " + selected.url + " exists and is reachable.")
    else:
        pr3("Verifying host, username, and password.")
    rpc_server = xmlrpclib.ServerProxy(selected.url)
    try:
        userinfo = rpc_server.blogger.getUserInfo('', selected.user, selected.password)
        return True
    except gaierror:    # gaierror caught if no connection to host
        exc_type, exc_value, exc_traceback = sys.exc_info()
        # print(exc_type, exc_value, exc_traceback)   # Use print intead of pr3 because print can take three args
        pr3("\n" + selected.url + " is unreachable.")
        pr3("Please check the spelling and make sure your Internet is working.")
        pr3("Working example: http://cool_url.com/xmlrpc.php")
        pr3("You may try again in just a moment.")
        time.sleep(3)
        return False
    except xmlFault:    # xmlFault caught if host found but user/pass mismatch
        if CHECK_PASSWORD == False or CHECK_PASSWORD == '':
            # Don't bother checking if password is correct
            return True
        else:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            print(exc_value)    # Using PRINT on purpose
            pr3("\nIncorrect Password. Please try again in just a moment.")
            time.sleep(3)
            return False
    except xmlrpcProtocolError:
            pr3("\nHTTP Protocol Error. Probably not your fault. Please try again in just a moment.")
            time.sleep(3)
            return False

def delete_config_file():
    rel_path = get_configpath()
    abs_path = os.path.expanduser(rel_path)
    pr3("abs_path is " + abs_path)
    if os.path.exists(abs_path):
        os.remove(abs_path)

class Credentials:
    def __init__(self, url, user, password):
        self.url = url
        self.user = user
        self.password = password

    @classmethod
    def ask(cls):
        "Initialize Credentials with values given by user"
        pr3 ('\nCREATING NEW PROFILE.')
        pr3 ("\nUSERNAME")
        while (1):
            pr3 ("Please enter your WordPress username")
            user = sys.stdin.readline().replace('\n', '')
            if user != '': break
        pr3 ("Username is " + user + '.')
        pr3 ("\nURL")
        while (1):
            pr3 ("Please enter your WordPress URL")
            pr3 ("Example: cool_site.wordpress.com")
            url = sys.stdin.readline().replace('\n', '')
            if url != '': break
        url = url.replace('http://', '')
        url = url.replace('www.', '')
        if url.endswith('/'):
            url = 'http://' + url + 'xmlrpc.php'
        else:
            url = 'http://' + url + '/xmlrpc.php'
        pr3 ("The PhP page we'll be talking to is " + url)
        pr3 ("\nPROMPT for PASSWORD?")
        pr3 ("Press ENTER now to be prompted each time (recommended).")
        pr3 ("Or type your precious password here, to be saved as plain text on you computer.")
        password = getpass.getpass()
        return cls(url, user, password)

    @classmethod
    def defaults(cls):
        "Initialize Credentials with default values"
        return cls('http://blogtest.letseatalready.com/xmlrpc.php',
                   'test',
                   'test')

    @classmethod
    def fromconfig(cls, config, section):
        "Initialize Credentials with values from config; use defaults if section is '0'"
        if section == '0': return cls.defaults()
        else:
            return cls(config.get(section, 'url'),
                       config.get(section, 'user'),
                       config.get(section, 'password'))

    def __str__(self):
        return self.user + "@" + self.url[7:-11]
