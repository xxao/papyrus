#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

# import modules
import time
import wx
from .constants import *


class GaugeDlg(wx.Dialog):
    """Creates generic gauge dialog."""
    
    
    def __init__(self, parent, id=-1, message="", title="", cancellation=None, style=wx.CAPTION):
        """Initializes a new instance of GaugeDlg."""
        
        wx.Dialog.__init__(self, parent, id, title, style=style)
        self._cancellation = cancellation
        
        # init sizer
        self.Sizer = wx.BoxSizer(wx.VERTICAL)
        
        # add message
        self._message = wx.StaticText(self, -1, message)
        self._message.SetFont(wx.SMALL_FONT)
        self.Sizer.Add(self._message, 0, wx.ALIGN_LEFT|wx.TOP|wx.LEFT|wx.RIGHT, PANEL_SPACE_MAIN)
        
        # add gauge
        self._gauge = wx.Gauge(self, -1, 100, size=(300, GAUGE_HEIGHT))
        self.Sizer.Add(self._gauge, 0, wx.ALL, PANEL_SPACE_MAIN)
        
        # add cancel button
        if self._cancellation is not None:
            cancel_butt = wx.Button(self, -1, "Cancel")
            cancel_butt.Bind(wx.EVT_BUTTON, self.OnCancel)
            self.Sizer.Add(cancel_butt, 0, wx.ALIGN_RIGHT|wx.RIGHT|wx.BOTTOM, PANEL_SPACE_MAIN)
        
        # display dialog
        self.Layout()
        self.Sizer.Fit(self)
        self.Centre()
        wx.Yield()
    
    
    def OnCancel(self, evt=None):
        """Handles cancel button."""
        
        if self._cancellation is not None:
            self._cancellation.cancel()
    
    
    def SetMessage(self, message):
        """Sets message text."""
        
        if self._message.GetLabel() != message:
            self._message.SetLabel(message)
    
    
    def SetRange(self, value):
        """Sets gauge range."""
        
        if self._gauge.GetRange() != value:
            self._gauge.SetRange(value)
    
    
    def SetValue(self, value):
        """Sets gauge value."""
        
        value = int(value)
        if self._gauge.GetValue() != value:
            self._gauge.SetValue(value)
    
    
    def Pulse(self):
        """Pulses gauge."""
        
        self._gauge.Pulse()
    
    
    def Close(self):
        """Closes panel"""
        
        #self.MakeModal(False)
        self.Destroy()
