#! /usr/bin/env python

# print contents of all files, just to show that we can access them all

# Next step: get it to run recursively
# Typical usage is
# $ python get_all.py *.py

def print_contents(input_file):
    f = open(input_file, 'r')
    str = f.read()
    f.close()
    print(str)


# Note that when calling
if __name__ == '__main__':
    import sys
    args = sys.argv
    del args[0]     # This is the program name. Deleting it leaves args
    for arg in args:
        file_to_print = arg
        print_contents(file_to_print)



