#!/bin/bash
# -*- coding: utf-8 -*-
#####################       A U T H O R       ##########################
#                                                                      #
#   Copyright 2010 Jack Desert                                         #
#   <JackDesert@gmail.com>                                             #
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

# Export docs from .lyx format to .html format
python export.py
# download current docs
mkdir cvs
cd cvs
rm -Rf lyxblogger
cvs -z3 -d:ext:jackdesert@cvs.savannah.nongnu.org:/web/lyxblogger co lyxblogger
# overwrite with current docs
cp ../../*.html lyxblogger/
cp ../../*.css lyxblogger/
cp ../images/*.png lyxblogger/images/
# commit
cd lyxblogger
cvs commit -m "Automatic upload using upload.sh"
cd ../..
rm -Rf cvs
