from PIL import Image
from math import floor
 
THUMBNAIL_PADDING_COLOUR = (255, 255, 255)
 
def pad(im, requested_size, opts):
    """
    Adds padding around the image to match the requested_size
    """
    if "pad" in opts and im.size != requested_size:
        canvas = Image.new("RGB", requested_size, THUMBNAIL_PADDING_COLOUR)
 
        left = floor((requested_size[0] - im.size[0]) / 2)
        top = floor((requested_size[1] - im.size[1]) / 2)
 
        canvas.paste(im, (left, top))
 
        im = canvas
 
    return im
 
pad.valid_options = ("pad", )


def extra_pad(im, requested_size, opts):
    """
    Adds padding around the image to match the requested_size
    """
    if "extra_pad" in opts:
        
        new_size = list(requested_size)
        if (im.size[0] > requested_size[0]): new_size[0] = im.size[0]
        if (im.size[1] > requested_size[1]): new_size[1] = im.size[1]
        
        canvas = Image.new("RGB", tuple(new_size), THUMBNAIL_PADDING_COLOUR)
         
        left = floor((new_size[0] - im.size[0]) / 2)
        top = floor((new_size[1] - im.size[1]) / 2)
        
        canvas.paste(im, (left, top))
 
        im = canvas
 
    return im
 
extra_pad.valid_options = ("extra_pad", )