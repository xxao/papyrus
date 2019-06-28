#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

# import modules
import random


DEFAULT_COLOURS = [
    (16, 71, 185),
    (50, 140, 0),
    (241, 144, 0),
    (76, 199, 197),
    (143, 143, 21),
    (237, 187, 0),
    (120, 109, 255),
    (179, 78, 0),
    (128, 191, 189),
    (137, 136, 68),
    (200, 136, 18),
    (197, 202, 61),
    (123, 182, 255),
    (69, 67, 138),
    (24, 129, 131),
    (131, 129, 131),
    (69, 126, 198),
    (189, 193, 123),
    (127, 34, 0),
    (76, 78, 76),
    (31, 74, 145),
    (15, 78, 75),
    (79, 26, 81)]


def generate_colour(used_colours=[], default_colours=DEFAULT_COLOURS):
    """Gets next free colour or generates random colour.
        used_colours (list of (r,g,b)): list of used colours
        default_colours (list of (r,g,b)): list of default colours
    """
    
    # try to use default colour
    for colour in default_colours:
        if not colour in used_colours:
            return colour
    
    # generate random colour
    i = 0
    while True:
        i += 1
        colour = [random.randrange(0,255), random.randrange(0,255), random.randrange(0,255)]
        if not colour in used_colours or i == 10000:
            return colour


def hex_to_rgb(value):
    """Converts colour from hex triplet into rgb tuple.
        value (str): colour as hex triplet
    """
    
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i+lv//3], 16) for i in range(0, lv, lv//3))


def rgb_to_hex(value):
    """Converts colour from rgb tuple into hex triplet.
        value (str): colour rgb tuple
    """
    
    return '%02x%02x%02x' % value
