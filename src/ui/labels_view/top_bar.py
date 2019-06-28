#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

# import modules
import wx

from .. import mwx
from .. import events
from .. import images


class LabelsTopBar(wx.Panel):
    """Labels top bar panel."""
    
    
    def __init__(self, parent):
        """Initializes labels top bar panel."""
        
        # init panel
        wx.Panel.__init__(self, parent, -1, style=wx.NO_FULL_REPAINT_ON_RESIZE)
        self.Bind(wx.EVT_PAINT, self._on_paint)
        
        # make UI
        self._make_ui()
    
    
    def _on_paint(self, evt):
        """Draws background image."""
        
        mwx.panel_top_h_bgr(self, images.BGR_TOP_BAR)
        mwx.panel_bottom_line(self, mwx.DARK_DIVIDER_COLOUR, 1)
    
    
    def _on_new(self, evt=None):
        """Handles add new label event."""
        
        event = events.LabelsNewEvent(self.GetId())
        wx.PostEvent(self, event)
    
    
    def _on_apply(self, evt=None):
        """Handles apply labels event."""
        
        event = events.LabelsApplyEvent(self.GetId())
        wx.PostEvent(self, event)
    
    
    def _make_ui(self):
        """Makes panel UI."""
        
        # make items
        self._new_butt = wx.Button(self, label="Add New")
        self._apply_butt = wx.Button(self, label="Apply")
        
        # bind events
        self._new_butt.Bind(wx.EVT_BUTTON, self._on_new)
        self._apply_butt.Bind(wx.EVT_BUTTON, self._on_apply)
        
        # add to sizer
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self._new_butt, 0, wx.ALIGN_CENTER_VERTICAL)
        sizer.AddStretchSpacer()
        sizer.Add(self._apply_butt, 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 10)
        self.Sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.Sizer.Add(sizer, 1, wx.EXPAND | wx.ALL, 10)
