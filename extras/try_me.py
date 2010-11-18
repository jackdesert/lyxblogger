#! /usr/bin/env python

# This script is to investigate try scripts
    # Apparently syntax is checked regardless. However, some things that happen at runtime
                    # cannot be checked. For example, you cannot guarantee what type something will
                    # be, because an if() statement could have a var assigned to be either a float or an int,
                    # depending on some other condition
import sys, traceback

try:
    a
except:
    #~ print("An exception flew by")
    #~ print sys.exc_type
    #~ print sys.exc_value
    #~ print sys.exc_traceback
    #~ print NameError
    #~ print '\n\n'
    #~ print sys.exc_info()
    print '\n\n'
    print traceback.print_exc()
print ("What would you like to do now?")
sys.stdin.readline()
#~ except:
    #~ print("encountered an exception")


