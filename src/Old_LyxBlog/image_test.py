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

# Code to test image.py

import sys
import unittest
import wordpresslib
from image import get_dir_offset
from image import find_local_image_tag
from image import get_local_image_url
from image import validate_url
from image import up_images
from image import get_short_name
from misc import pr3


class ImageTestCase(unittest.TestCase):

    def setUp(self):
        pass
    def test_md5_sums(self):
        # Only run this test if using Python 2.5 or later, which
        # Supports hashlib.
        req_version = (2,5)
        cur_version = sys.version_info
        if(cur_version >= req_version):
            import hashlib
            dict = {'test_files/basic_blog.html' : '6736518f123b0d6c3995a5ca1f2649fc',
                'test_files/basic_blog.xhtml' : '025e596c6f9dc8ee174ac2f372d801a4'}
            for in_file, md5sum in dict.iteritems():
                computed =  hashlib.md5(file(in_file).read()).hexdigest()
                self.assertEqual(computed, md5sum)
        else:
            print("Skipping md5sum tests because hashlib is not available in the version of Python.")
            print (sys.version_info)


    def test_get_dir_offset(self):
        dict = {'/hi_there/file.txt' : '/hi_there/',
            '/once/there/was/a/dog.txt' : '/once/there/was/a/',
            'no_leading_slash/once.txt' : 'no_leading_slash/',
            '../../up_two_levels/level.txt' : '../../up_two_levels/',
            '/theres_a space/file.txt': '/theres_a space/',
            'no_dir' : '',
            '/what/about\backslashes.txt' : '/what/'}
        for input_file, dir_offset in dict.iteritems():
            self.assertEqual(get_dir_offset(input_file), dir_offset)

    def test_validate_url(self):
        DIR_OFFSET = 'local_folder/'
        dict = {'a_file.jpg' : 'local_folder/a_file.jpg',
            '/absolute_dir/file.jpg' : '/absolute_dir/file.jpg' }
        for input, output in dict.iteritems():
            self.assertEqual(validate_url(input, DIR_OFFSET), output)

    def test_find_local_image_tag(self):
        dict = {'test_files/basic_blog.html' : True,
            'test_files/basic_blog.xhtml' : False}
        for in_file, ELYXER_ENGINE in dict.iteritems():
            # Read data from file
            f = open(in_file, 'r')
            html = f.read()
            f.close()
            for counter in range(2):
                tag = find_local_image_tag(html, ELYXER_ENGINE)
                self.assertTrue(tag)
                # Remove the tag and make sure it's gone
                html = html.replace(tag, '')
                self.assertFalse(tag in html)
            # Third image is nonexistent
            tag = find_local_image_tag(html, ELYXER_ENGINE)
            self.assertFalse(tag)
    def test_get_local_image_url(self):
        dict = {'''<img src='some_url' alt='none' />''' : ('some_url', False),
            '''<img alt = ni src='helloáthere'>''' : ('helloáthere', False),
            '''<blah~ src="been there" /> ''': ('been there', True)}
        for tag, url in dict.iteritems():
            found_url = get_local_image_url(tag, url[1])
            self.assertEqual(found_url, url[0])
            self.assertTrue(len(found_url) > 0)
    def test_up_images(self):
        # A typical eLyXer image tag : ELYXER_ENGINER = True
        # A typical LyXHTML image tag : ELYXER_ENGINE = False
        dict = {'<img class="embedded" src="test_files/images/table.jpg" />' : True,
            "<img src='test_files/images/table.jpg' />" : False}
        wp = wordpresslib.WordPressClient(
            'http://blogtest.letseatalready.com/xmlrpc.php', 'test', 'test')
        for html, ELYXER_ENGINE in dict.iteritems():
            pr3('\n\n***   Testing the upload of a single image   ***')
            up_images(html, wp, ELYXER_ENGINE, in_DIR_OFFSET = '')
    def test_get_short_name(self):
        a_url = 'wants/to/be/shorter.ext'
        short_name = get_short_name(a_url)
        self.assertEqual(short_name, 'shorter.ext')



if __name__ == '__main__':
    unittest.main()

