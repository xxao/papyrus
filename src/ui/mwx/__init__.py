#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

# import modules
import wx
from .constants import *
from .colours import *
from .message_dlg import *
from .gauge_dlg import GaugeDlg
from .drop_targets import *


def initialize():
    """Initializes some constants."""
    
    wx.SMALL_FONT.SetPointSize(SMALL_FONT_SIZE)


def panel_top_h_bgr(panel, image):
    """Draws repeating image as panel background."""
    
    if not panel:
        return
    
    win_size = panel.GetSize()
    img_width = image.GetWidth()
    dc = wx.PaintDC(panel)
    
    for x in range(0, win_size[0], img_width):
        dc.DrawBitmap(image, x, 0, True)


def panel_top_line(panel, colour=DARK_DIVIDER_COLOUR, width=1):
    """Draws panel top divider."""
    
    if not panel:
        return
    
    win_size = panel.GetSize()
    dc = wx.PaintDC(panel)
    dc.SetPen(wx.Pen(colour, width, wx.SOLID))
    dc.DrawLine(0, 0, win_size[0], 0)


def panel_bottom_line(panel, colour=DARK_DIVIDER_COLOUR, width=1):
    """Draws panel bottom divider."""
    
    if not panel:
        return
    
    win_size = panel.GetSize()
    dc = wx.PaintDC(panel)
    dc.SetPen(wx.Pen(colour, width, wx.SOLID))
    dc.DrawLine(0, win_size[1]-width, win_size[0], win_size[1]-width)
