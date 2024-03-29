#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

# import modules
import wx


# init constants
IS_MAC = wx.Platform == "__WXMAC__"
IS_WIN = wx.Platform == "__WXMSW__"

SCROLL_DIRECTION = -1

SMALL_FONT_SIZE = 8
NORMAL_FONT_SIZE = 9

CAPTION_COLOUR = (200,200,200)
SASH_COLOUR = (200,200,200)
SASH_SIZE = 4
GRIPPER_SIZE = 10

LIGHT_DIVIDER_COLOUR = (200,200,200)
DARK_DIVIDER_COLOUR = (200,200,200)

PANEL_SPACE_MAIN = 10
LIST_CTRL_SPACE = 0
GRIDBAG_VSPACE = 7
GRIDBAG_HSPACE = 5

GAUGE_HEIGHT = 15
GAUGE_SPACE = 10

BOTTOM_BAR_HEIGHT = 23

COLLECTIONS_VIEW_BGR = (247,247,247)
DETAILS_VIEW_BGR = (247,247,247)
PDF_VIEW_BGR = (247,247,247)

RATING_SIZE = 5
RATING_SPACE = 2
RATING_OUTLINE_COLOUR = (255,255,255)
RATING_FILL_COLOUR = (50,50,255)
RATING_FILL_COLOUR_UNCHECKED = (150,150,150)
RATING_BGR_COLOUR = (230,230,230)
RATING_NAMES = ("none", "bad", "poor", "ok", "good", "excellent")

COLOUR_BULLET_SIZE = 5
COLOUR_BULLET_OUTLINE_COLOUR = (255,255,255)
COLOUR_BULLET_OUTLINE_COLOUR_CHECKED = (50,50,50)

COLOUR_BULLET_GRAY = (230,230,230)  # E6E6E6
COLOUR_BULLET_RED = (255,110,100)  # FF6E64
COLOUR_BULLET_ORANGE = (255,185,65)  # FFB941
COLOUR_BULLET_YELLOW = (240,230,65)  # F0E646
COLOUR_BULLET_GREEN = (180,230,70)  # B4E646
COLOUR_BULLET_BLUE = (100,175,255)  # 64AFFF
COLOUR_BULLET_PURPLE = (220,140,240)  # DC8CF0

COLOUR_NAMES = ("none", "red", "orange", "yellow", "green", "blue", "purple")
COLOUR_BULLETS = {
    "none": COLOUR_BULLET_GRAY,
    "red": COLOUR_BULLET_RED,
    "orange": COLOUR_BULLET_ORANGE,
    "yellow": COLOUR_BULLET_YELLOW,
    "green": COLOUR_BULLET_GREEN,
    "blue": COLOUR_BULLET_BLUE,
    "purple": COLOUR_BULLET_PURPLE,
}

ARTICLE_DELETED_COLOUR = (200,200,200)
AUTHOR_ORPHAN_COLOUR = (200,100,100)

LIBSTATUS_SIZE = 5
LIBSTATUS_OUTLINE_COLOUR = (255,255,255)
LIBSTATUS_ON_COLOUR = (50,50,255)
LIBSTATUS_OFF_COLOUR = (200,200,200)

STATSBAR_OUTLINE_COLOUR = (255,255,255)
STATSBAR_FILL_COLOUR = (50,50,255)
STATSBAR_BGR_COLOUR = (230,230,230)

ARROW_BUTTON_COLOUR = (100,100,100)

# set mac specific values
if IS_MAC:
    
    SMALL_FONT_SIZE = 11
    NORMAL_FONT_SIZE = 12
    
    CAPTION_COLOUR = (200,200,200)
    SASH_COLOUR = (130,130,130)
    SASH_SIZE = 1
    GRIPPER_SIZE = 10
    
    PANEL_SPACE_MAIN = 20
    GRIDBAG_VSPACE = 7
    GRIDBAG_HSPACE = 5
    
    DARK_DIVIDER_COLOUR = (130,130,130)
    
    BOTTOM_BAR_HEIGHT = 22
    
    COLLECTIONS_VIEW_BGR = (214,221,229)
