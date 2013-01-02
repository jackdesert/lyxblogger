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

# Code to test misc.py

import sys
import unittest
from misc import trim_cut_material
from misc import get_format


class MiscTestCase(unittest.TestCase):

    def setUp(self):
        pass
    def test_trim_cut_material(self):
        # Note that the cut flag must be right after the <div><a>\n
        # That is why this string has been allowed to drift left, is
        # to make sure no spaces come between the <a> and the \n
        html_LyXHTML = '''<div class="standard"><a id='magicparlabel-69' />
Hi there</div>

<div class="standard"><a id='magicparlabel-72' />
#! CUT MATERIAL</div>

<div class="standard"><a id='magicparlabel-80' />
What's up?</div>'''
        html_LyXHTML = trim_cut_material(html_LyXHTML, '#! CUT MATERIAL', False)
        print ('new value is: ' + html_LyXHTML)
        self.assertTrue('Hi there' in html_LyXHTML)
        self.assertFalse('CUT MATERIAL' in html_LyXHTML)
        self.assertFalse('''What's up?''' in html_LyXHTML)

    def test_trim_cut_material2(self):
        # Note that the cut flag must be right after the <div><a>\n
        # That is why this string has been allowed to drift left, is
        # to make sure no spaces come between the <a> and the \n
        html_eLyXer = '''<div id="globalWrapper">

<div class="Standard">
Hi there
</div>

<div class="Standard">
#! CUT MATERIAL
</div>
<div class="Standard">
What’s up?
</div>

</div>
'''
        html_eLyXer = trim_cut_material(html_eLyXer, '#! CUT MATERIAL', True)
        self.assertTrue('Hi there' in html_eLyXer)
        self.assertFalse('CUT MATERIAL' in html_eLyXer)
        self.assertFalse('''What's up?''' in html_eLyXer)

    def test_get_format1(self): # LyXHTML
        html = '<head><meta name="GENERATOR" content="LyX 2.0.0svn" /></head>'
        engine = get_format(html)
        self.assertFalse(engine)    # ENGINE_ELYXER is false
    def test_get_format2(self): # eLyXer
        html = '<head><meta name="generator" content="http://www.nongnu.org/elyxer/"/></head>'
        engine = get_format(html)
        self.assertTrue(engine)    # ENGINE_ELYXER is true

    def test_get_format3(self): # Hevea
        html = '<head><META name="GENERATOR" content="hevea 1.10"></head>'
        self.assertRaises(SystemExit,get_format, html)


    def test_get_format4(self): # LaTeX2HTML
        html = '''<!--Converted with LaTeX2HTML 2002-2-1 (1.71)
            original version by:  Nikos Drakos, CBLU, University of Leeds
            * revised and updated by:  Marcus Hennecke, Ross Moore, Herb Swan
            * with significant contributions from:
            Jens Lippmann, Marek Rouchal, Martin Wilck and others -->'''
        self.assertRaises(SystemExit,get_format, html)


    def test_get_format5(self): # TtH
        html = '<head><meta name="GENERATOR" content="TtH 3.85"></head>'
        self.assertRaises(SystemExit,get_format, html)

    def test_get_format6(self): # Anything else
        html = '<head><just a bunch of jibberish></head>'
        self.assertRaises(SystemExit,get_format, html)



if __name__ == '__main__':
    unittest.main()

