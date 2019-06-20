#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

# import modules
import wx

# load library
if wx.Platform == '__WXMAC__':
    from . import images_mac as images
elif wx.Platform == '__WXMSW__':
    from . import images_msw as images

# app icons
APP_ICON_16 = images.getAppIcon16Icon()
APP_ICON_32 = images.getAppIcon32Icon()
APP_ICON_48 = images.getAppIcon48Icon()
APP_ICON_128 = images.getAppIcon128Icon()
APP_ICON_256 = images.getAppIcon256Icon()

# general icons
ICON_VIEW_COLLECTIONS = images.getIconViewCollectionsBitmap()
ICON_VIEW_DETAILS = images.getIconViewDetailsBitmap()
ICON_VIEW_CHARTS = images.getIconViewChartsBitmap()

ICON_COLLECTION_LIBRARY = images.getIconCollectionLibraryIcon()
ICON_COLLECTION_MANUAL = images.getIconCollectionManualIcon()
ICON_COLLECTION_SMART = images.getIconCollectionSmartIcon()
ICON_COLLECTION_LABEL = images.getIconCollectionLabelIcon()

ICON_INFO = images.getIconInfoBitmap()
ICON_PDF = images.getIconPdfBitmap()
ICON_PDF_MISSING = images.getIconPdfMissingBitmap()


# backgrounds
BGR_TOP_BAR = images.getBgrTopBarBitmap()
BGR_BOTTOM_BAR = images.getBgrBottomBarBitmap()
SPACER = images.getSpacerBitmap()


def bullet(radius, outline, fill):
    """Draws colour bullet icon for specific value."""
    
    # init drawing
    bitmap = wx.Bitmap(2*radius+2, 2*radius+2)
    mdc = wx.MemoryDC()
    mdc.SelectObject(bitmap)
    dc = wx.GCDC(mdc) if wx.Platform != "__WXMSW__" else mdc
    
    # draw bullet
    dc.SetPen(outline)
    dc.SetBrush(fill)
    dc.DrawCircle(radius+1, radius+1, radius)
    
    # release bitmap
    mdc.SelectObject(wx.NullBitmap)
    
    # set mask
    if wx.Platform == "__WXMSW__":
        bitmap.SetMaskColour(wx.BLACK)
    
    return bitmap


def rating(value, radius, space, outline, fill, bgr):
    """Draws rating icon for specific value."""
    
    # init drawing
    bitmap = wx.Bitmap(10*radius+5*space, 2*radius+1)
    mdc = wx.MemoryDC()
    mdc.SelectObject(bitmap)
    dc = wx.GCDC(mdc) if wx.Platform != "__WXMSW__" else mdc
    
    # start drawing
    x = radius
    
    dc.SetPen(outline)
    dc.SetBrush(fill)
    for i in range(value):
        dc.DrawCircle(x, radius, radius)
        x += 2*radius + space
    
    dc.SetBrush(bgr)
    for i in range(5-value):
        dc.DrawCircle(x, radius, radius)
        x += 2*radius + space
    
    # release bitmap
    mdc.SelectObject(wx.NullBitmap)
    
    # set mask
    if wx.Platform == "__WXMSW__":
        bitmap.SetMaskColour(wx.BLACK)
    
    return bitmap
