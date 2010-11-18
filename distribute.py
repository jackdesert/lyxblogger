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

# This code creates a tar package containing the relevant files for
# LyXBlogger

# Instructions:
# cd to the directory containing this script and the other files listed.
# Call this file as:
# ./distribute.py <version>
# where <version> is a number like 1.49
import os, sys, time
from src.LyxBlog.misc import pr3

print('''\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n
About to run automated unit and interactive tests.
When you get the error screens, hit ENTER.
When asked for a password, enter "test" without the quotes.
''')
time.sleep(5)

def process_commands(command_list):
    for command in command_list:
        # Make sure each command executes properly. Otherwise, throw an exception
        a = os.system(command)
        if(a != 0):
            print('\nCommand was: ' + command)
            raise Exception('ERROR: There was a problem with one of your commands')


pre_commands = ['cd src \n python test_seed.py',  # Run unit tests and interactive on seed
    'rm -f INSTALL/lyxblogger.py ',    # Remove old version of lyxblogger
    'cd src \n ./coalesce.py seed.py > ../INSTALL/lyxblogger.py', # Construct lyxblogger.py
    'echo "Local password needed for installation of Python modules"', # Tell why password is needed
    'cd INSTALL \n sudo python setup.py install']  # Install the newly coalesced lyxblogger as a module

process_commands(pre_commands)
pr3('Unit tests passed')
filesize = os.path.getsize('INSTALL/lyxblogger.py')
assert(filesize > 15000) # As of LyXBlogger_0.33c, filesize was ~18k
pr3('seed.py with package coalesced into lyxblogger.py')


VERSION = sys.argv[1]
if VERSION == None:
    raise Exception('No version number given')
BASE = 'LyXBlogger_' + VERSION
FOLDER =  BASE + '/'
TARGET = BASE + '.tar.gz'
ZIP_TARGET = BASE + '.zip'
OUTPUT_DIRECTORY = 'releases/'
# Create a folder with the relevant bits in it
commands = ['mkdir ' + FOLDER,                      # Create a folder for this release
        'cp -r src ' + FOLDER ,                 # Put stuff in the folder
        'cp -r INSTALL ' + FOLDER ,
        'cd docs/raw \n ./export.py',           # Convert LyX documents to html for viewing
        'cp -r docs ' + FOLDER ,
        'rm -f ' + FOLDER + 'docs/raw/*.lyx#',  # Remove LyX lock files
        'cp README ' + FOLDER,
        'cp LICENSE ' + FOLDER,
        'rm -rf ' + FOLDER + 'INSTALL/build',       # Remove the build directory
        'rm -f ' + FOLDER + '*.pyc',                # Remove all *.pyc files
        'rm ' + FOLDER + 'INSTALL/*.pyc',
        'rm -f ' + FOLDER + 'src/*.pyc',
        'rm -f ' + FOLDER + 'src/io/*.pyc',
        'rm -f ' + FOLDER + 'src/util/*.pyc',
        'rm -f ' + FOLDER + 'src/LyxBlog/*.pyc',
        'tar -zcvf' + TARGET + ' --exclude-vcs ' + FOLDER,       # Create a compressed tar file
        'rm -rf ' + FOLDER,                                 # Remove the folder it was created from
        'tar -xvf ' + TARGET,                           # Open the tar file so now we have a folder without .svn
        'zip -r ' + ZIP_TARGET + ' ' + FOLDER,      # Create a compressed zip file
        'mv ' + TARGET + ' ' + OUTPUT_DIRECTORY,    # Move compressed files into archive
        'mv ' + ZIP_TARGET + ' ' + OUTPUT_DIRECTORY]

process_commands(commands)



print ("Distribution .zip and .tar.gz files have been created.")
print ("Remember to svn update and then add the SVN rev number to the changelog.\n")
print ("Would you like to publish the new documents and release version to the web? Y (N)")
publish = sys.stdin.readline().replace('\n', '')
UPFILES = TARGET + ' ' + TARGET + '.sig ' + ZIP_TARGET + ' ' + ZIP_TARGET + '.sig '
CHDIR = 'cd ' + OUTPUT_DIRECTORY + '\n' # This gets you to the directory you want to call from
post_commands = ['echo "Your SSH password is required to upload CVS docs"',
    'cd docs/raw/ \n ./upload_docs.sh',
    CHDIR + 'gpg -b ' + TARGET,
    CHDIR + 'gpg -b ' + ZIP_TARGET,
    CHDIR + 'gpg --verify  ' + TARGET + '.sig',
    CHDIR + 'gpg --verify  ' + ZIP_TARGET + '.sig',
    'echo "Your GPG key requires authentication to publish this release"',
    CHDIR + 'scp ' + UPFILES + 'jackdesert@dl.sv.nongnu.org:/releases/lyxblogger/']
if (publish == 'y' or publish == 'Y'):
    print("Did you update the CHANGELOG, add the svn rev number, and visually check a blog entry? Y (N)")
    changelog_updated = sys.stdin.readline().replace('\n', '')
    if (changelog_updated == 'y' or changelog_updated == 'Y'):
        process_commands(post_commands)
        print("LyXBlogger version " + VERSION + " has been published!")
        print("I suggest you test it out and then publicize it")
    else:
        print("Please update the changelog before publishing.")
else:
    print("Not published to web")
