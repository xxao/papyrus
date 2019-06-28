#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

# import modules
import wx

from .. import mwx
from .. import images


class RepositoryBottomBar(wx.Panel):
    """Repository bottom bar panel."""
    
    
    def __init__(self, parent):
        """Initializes repository bottom bar panel."""
        
        # init panel
        wx.Panel.__init__(self, parent, -1, size=(-1, mwx.BOTTOM_BAR_HEIGHT), style=wx.NO_FULL_REPAINT_ON_RESIZE)
        self.Bind(wx.EVT_PAINT, self._on_paint)
        
        # make UI
        self._make_ui()
    
    
    def SetLabel(self, label):
        """Sets status label."""
        
        self._status_label.SetLabel(label)
        self.Layout()
    
    
    def _on_paint(self, evt):
        """Draws background image."""
        
        mwx.panel_top_h_bgr(self, images.BGR_BOTTOM_BAR)
        mwx.panel_top_line(self, mwx.DARK_DIVIDER_COLOUR)
    
    
    def _make_ui(self):
        """Makes panel UI."""
        
        # make items
        self._status_label = wx.StaticText(self, -1, "", style=wx.ALIGN_CENTER)
        self._status_label.SetFont(wx.SMALL_FONT)
        
        # add to sizer
        self.Sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.Sizer.AddStretchSpacer()
        self.Sizer.Add(self._status_label, 1, wx.ALIGN_CENTER_VERTICAL)
        self.Sizer.AddStretchSpacer()
