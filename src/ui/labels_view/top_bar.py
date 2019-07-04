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
    
    
    def GetLabelValue(self):
        """Gets current search value."""
        
        return self._label_value.GetValue().strip()
    
    
    def SetLabelValue(self, value):
        """Sets current search value."""
        
        if value is None:
            value = ""
        
        return self._label_value.SetValue(value)
    
    
    def _on_paint(self, evt):
        """Draws background image."""
        
        mwx.panel_top_h_bgr(self, images.BGR_TOP_BAR)
        mwx.panel_bottom_line(self, mwx.DARK_DIVIDER_COLOUR, 1)
    
    
    def _on_type(self, evt=None):
        """Handles type label event."""
        
        # enable/disable add button
        self._add_butt.Enable(bool(self.GetLabelValue()))
        
        # post event
        event = events.LabelsTypeEvent(self.GetId())
        wx.PostEvent(self, event)
    
    
    def _on_add(self, evt=None):
        """Handles add label event."""
        
        event = events.LabelsAddEvent(self.GetId())
        wx.PostEvent(self, event)
    
    
    def _on_apply(self, evt=None):
        """Handles apply labels event."""
        
        event = events.LabelsApplyEvent(self.GetId())
        wx.PostEvent(self, event)
    
    
    def _make_ui(self):
        """Makes panel UI."""
        
        # make items
        self._label_value = wx.TextCtrl(self, -1, "", style=wx.TE_PROCESS_ENTER)
        self._add_butt = wx.Button(self, label="Add", size=(60,-1))
        self._apply_butt = wx.Button(self, label="Apply", size=(60,-1))
        
        # set state
        self._add_butt.Disable()
        
        # bind events
        self._label_value.Bind(wx.EVT_TEXT, self._on_type)
        self._label_value.Bind(wx.EVT_TEXT_ENTER, self._on_add)
        self._add_butt.Bind(wx.EVT_BUTTON, self._on_add)
        self._apply_butt.Bind(wx.EVT_BUTTON, self._on_apply)
        
        # add to sizer
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self._label_value, 1, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 10)
        sizer.Add(self._add_butt, 0, wx.ALIGN_CENTER_VERTICAL)
        sizer.Add(self._apply_butt, 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 10)
        self.Sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.Sizer.Add(sizer, 1, wx.EXPAND | wx.ALL, 10)
