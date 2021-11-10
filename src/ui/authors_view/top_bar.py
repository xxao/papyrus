#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

# import modules
import wx

from .. import mwx
from .. import events
from .. import images


class AuthorsTopBar(wx.Panel):
    """Authors top bar panel."""
    
    
    def __init__(self, parent):
        """Initializes authors top bar panel."""
        
        # init panel
        wx.Panel.__init__(self, parent, -1, style=wx.NO_FULL_REPAINT_ON_RESIZE)
        self.Bind(wx.EVT_PAINT, self._on_paint)
        
        # make UI
        self._make_ui()
    
    
    def SetFocusToQuery(self):
        """Sets focus on search query field."""
        
        self._query_search.SetFocus()
    
    
    def GetQuery(self):
        """Gets current query value."""
        
        return self._query_search.GetValue().strip()
    
    
    def ChangeQuery(self, value):
        """Sets query without raising the change event."""
        
        # check value
        if not value:
            value = ""
        
        # update control
        self._query_search.ChangeValue(value)
    
    
    def _on_paint(self, evt):
        """Draws background image."""
        
        mwx.panel_top_h_bgr(self, images.BGR_TOP_BAR)
        mwx.panel_bottom_line(self, mwx.DARK_DIVIDER_COLOUR)
    
    
    def _on_query_changed(self, evt=None):
        """Handles query changed event."""
        
        event = events.AuthorsQueryChangedEvent(self.GetId())
        wx.PostEvent(self, event)
    
    
    def _make_ui(self):
        """Makes panel UI."""
        
        # make items
        self._query_search = wx.SearchCtrl(self, size=(100,-1), style=wx.TE_PROCESS_ENTER)
        self._query_search.SetDescriptiveText("Search Authors")
        self._query_search.ShowSearchButton(wx.Platform != "__WXMSW__")
        self._query_search.ShowCancelButton(True)
        
        # bind events
        self._query_search.Bind(wx.EVT_TEXT, self._on_query_changed)
        self._query_search.Bind(wx.EVT_TEXT_ENTER, self._on_query_changed)
        
        # add to sizer
        self.Sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.Sizer.Add(self._query_search, 1, wx.EXPAND | wx.ALL, 10)
