#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

# import modules
import wx
from .constants import *
from .. import images


class MessageDlg(wx.Dialog):
    """Creates generic message dialog."""
    
    
    def __init__(self, parent, id, message, details="", title="", buttons=[], icon=True, style=wx.DEFAULT_DIALOG_STYLE):
        """Initializes a new instance of MessageDlg."""
        
        wx.Dialog.__init__(self, parent, id, title, style=style)
        
        # make message
        message_label = wx.StaticText(self, -1, message)
        message_label.SetFont(wx.Font(wx.NORMAL_FONT.GetPointSize(), wx.NORMAL_FONT.GetFamily(), wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        
        # make details
        details_label = wx.StaticText(self, -1, details)
        details_label.SetFont(wx.SMALL_FONT)
        
        # use default button
        if not buttons:
            buttons = [DlgButton(wx.ID_CANCEL, "OK", (80,-1), True, 0)]
        
        # make buttons
        buttons_sizer = wx.BoxSizer(wx.HORIZONTAL)
        for button in buttons:
            button_butt = button.Create(self)
            button_butt.Bind(wx.EVT_BUTTON, self.OnButton)
            buttons_sizer.Add(button_butt, 0, wx.RIGHT, button.GetSpace())
        
        # pack elements
        elements_sizer = wx.BoxSizer(wx.VERTICAL)
        elements_sizer.Add(message_label, 0, wx.ALIGN_LEFT)
        if details:
            elements_sizer.Add(details_label, 0, wx.ALIGN_LEFT | wx.TOP, 10)
        elements_sizer.Add(buttons_sizer, 0, wx.ALIGN_RIGHT | wx.TOP, PANEL_SPACE_MAIN)
        
        # init main sizer
        self.Sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        # add icon
        if icon is True:
            icon = images.ICON_INFO
        if icon is not None and icon is not False:
            bitmap = wx.StaticBitmap(self, -1, icon)
            self.Sizer.Add(bitmap, 0, wx.TOP | wx.LEFT | wx.BOTTOM, PANEL_SPACE_MAIN)
        
        # add elements
        self.Sizer.Add(elements_sizer, 0, wx.ALIGN_BOTTOM | wx.ALIGN_LEFT | wx.ALL, PANEL_SPACE_MAIN)
        
        # fit layout
        self.Layout()
        self.Sizer.Fit(self)
        self.Centre()
    
    
    def OnButton(self, evt):
        """Returns pressed button ID."""
        
        self.EndModal(evt.GetId())


class DlgButton(object):
    """Represents message dialog button definition."""
    
    
    def __init__(self, id, label, size=(80,-1), default=False, space=0):
        """Initializes a new instance of DlgButton."""
        
        super(DlgButton, self).__init__()
        
        self._id = id
        self._label = label
        self._size = size
        self._default = default
        self._space = space
    
    
    def GetSpace(self):
        """Gets right margin."""
        
        return self._space
    
    
    def Create(self, parent):
        """Creates corresponding wx.Button instance."""
        
        button = wx.Button(parent, self._id, self._label, size=self._size)
        
        if self._default:
            button.SetDefault()
            button.SetFocus()
        
        return button
