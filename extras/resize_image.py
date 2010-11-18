#! /usr/bin/env python


# resize an image using the PIL image library
#
# free from: http://www.pythonware.com/products/pil/index.htm
#
# tested with Python24 vegaseat 11oct2005
#

#
import Image
import sys, os
from PIL import Image as PIL_Image



#
# adjust width and height to your needs
#
NEW_WIDTH = 500

#
NEW_WIDTH = float(NEW_WIDTH)
sys.argv.pop(0) # remove first
for imageFile in sys.argv:
    try:
        im = PIL_Image.open(imageFile)
    except IOError:
        print "failed to identify", file
    else:
        print "image format:", im.format
        print "image mode:", im.mode
        print "image size:", im.size
        if im.info.has_key("description"):
            print "image description:", im.info["description"]

    im1 = Image.open(imageFile)
    # use one of these filter options to resize the image
    #
    # im2 = im1.resize((width, height), Image.NEAREST) # use nearest neighbour
    #
    # im3 = im1.resize((width, height), Image.BILINEAR) # linear interpolation in a 2x2 environment
    #
    orig_width = im.size[0]
    orig_height = im.size[1]
    scale = NEW_WIDTH / orig_width
    new_height = scale * orig_height
    new_size = (NEW_WIDTH, new_height)
    print("Resizing " + imageFile)
    print("size: " + str(new_height) + " x " + str(NEW_WIDTH))
    im4 = im1.resize(new_size, Image.BICUBIC) # cubic spline interpolation in a 4x4 environment
    #
    # im5 = im1.resize((width, height), Image.ANTIALIAS) # best down-sizing filter
    #
    im4.save(imageFile)

#~
#~ #
#~ ext = ".jpg"
#~ #
#~ im2.save("NEAREST" + ext)
#~ #
#~ im3.save("BILINEAR" + ext)
#~ #
#~ im4.save("BICUBIC" + ext)
#~ #
#~ im5.save("ANTIALIAS" + ext)
