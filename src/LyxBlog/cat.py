#! /usr/bin/env python
# -*- coding: utf-8 -*-
#####################       A U T H O R       ##########################
#                                                                      #
#   Copyright 2010 Jack Desert                                         #
#   <jackdesert@gmail.com>                                          #
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
import sys, time
import wordpresslib
from misc import pr3

def get_post_id(wp_obj, history = 9):
    DATE_FLAG = "DATE"
    pr3 ('\nUPDATE A PREVIOUS POST')
    pr3 ('Retrieving Previous Posts From Server')
    #~ post_list = wp_obj.getpostegoryList()
    post_counter = 1
    post_list = []
    posts = wp_obj.getRecentPosts(history)
    dict = {}   # This dictionary matches display number with post_id
    try:
        while True:
            a = posts.next()
            # Make note in the dictionary which post id (a.id) each displayed title represents
            date_string = ''
            if a.date:
                mon = str(a.date[1])
                day = str(a.date[2])
                if len(day) == 1:   # Formatting
                    day = '0' + day
                yr = str(a.date[0])
                date_string = '    ' + mon  + '/' + day + '/' + yr
            key = str(post_counter)
            dict[key] = MiniPost(in_post_id = a.id, in_title = a.title, in_date = date_string)
            display = key + '.  ' + dict[key].title + DATE_FLAG + dict[key].date
            post_list.append(display)
            post_counter += 1
    except StopIteration:
        # The StopIteration exception is called once all the function generator entries have passed
        formatted_list = same_length(post_list, DATE_FLAG)
        if history != 0:
            formatted_list.append('A.    --  Show All Entries  --  ')
        for item in formatted_list:
            try:
                print(item)
            except UnicodeEncodeError:
                print("This line skipped because the Unicode would not display properly")

    while (1):
        pr3 ('\nPlease enter the NUMBER next to the post to overwrite')
        if (len(formatted_list) > 12 and sys.platform != 'win32'):
            pr3('Hint: SHIFT + PageUp scrolls screen')
        response = sys.stdin.readline().replace('\n', '')
        if (response == 'a' or response == 'A'):
            pr3('\nPlease allow up to a minute to download all post headers')
            post_id = get_post_id(wp_obj, 0)  # List all entries
            break
        else:
            try:
                post_id = dict[response].post_id
                # Print used on this instead of pr3 to prevent erros with Unicode titles
                print ('Selected: ' + dict[response].title + dict[response].date)
                break
            except KeyError:
                pr3 ("Post Selection Not Understood.\n")
    return post_id

def same_length(in_list,date_flag):
    TRUNCATE_LENGTH = 50    # The longest
    # Find max length of the items in the list
    max_length = 0
    for item in in_list:
        a = len(item)
        if a > max_length:
            max_length = a
    # Now we know the max_length
    out_list = []
    for item in in_list:
        a = len(item)
        spaces_to_add = max_length - a
        assert(spaces_to_add >= 0)
        assert(date_flag in item)
        pieces = item.rpartition(date_flag)   # Looks for last 'Date:'space in item
        # Limit the length of the title
        title_w_spaces = pieces[0] + (spaces_to_add)*' '
        title_w_spaces = title_w_spaces[0:TRUNCATE_LENGTH]
        # Add space in the middle
        new_item = title_w_spaces + pieces[2]
        out_list.append(new_item)
    return out_list


def get_cat_id(wp_obj):
    pr3 ('\nCATEGORY')
    pr3 ('Retrieving Categories From Server')
    cat_list = wp_obj.getCategoryList()
    cat_counter = 1
    dict = {}
    for cat in cat_list:
        print (str(cat_counter) + '.  ' + cat.name)
        dict[cat_counter] = cat.id
        cat_counter += 1
    output_list = []
    while (1):
        try:
            pr3 ('Please enter the NUMBER next to the category for this post')
            pr3 ('To select multiple categories, separate with commas')
            cat_response = sys.stdin.readline().replace('\n', '')
            cat_response_list = cat_response.split(',')
            for cat in cat_response_list:
                cat_int = int(cat)
                cat_id = cat_list[cat_int-1].id
                output_list.append(cat_id)
                print ('Category Selected: ' + cat_list[cat_int-1].name + '\n')
            break
        except ValueError:
            pr3 ("Category Response Not Understood.\n")
    assert(len(output_list) > 0)
    return output_list

class MiniPost:
    "A minipost contains just the title, numerical selector, and post_id"
    def __init__(self, in_post_id, in_title, in_date):
        self.post_id = in_post_id
        self.title = in_title
        self.date = in_date
