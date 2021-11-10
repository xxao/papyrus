#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

# import modules
import wx

from .. import mwx
from .. import events
from .. import images


class RepositoryTopBar(wx.Panel):
    """Repository top bar panel."""
    
    
    def __init__(self, parent, mode):
        """Initializes repository top bar panel."""
        
        # init panel
        wx.Panel.__init__(self, parent, -1, style=wx.NO_FULL_REPAINT_ON_RESIZE)
        self.Bind(wx.EVT_PAINT, self._on_paint)
        
        self._mode = mode
        
        # make UI
        self._make_ui()
    
    
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
    
    
    def EnableSearchQuery(self, value):
        """Enables or disables query search field."""
        
        pass
        # currently looks bad
        # self._query_search.Enable(bool(value))
    
    
    def EnableSearchButton(self, value, label="Search"):
        """Enables or disables search button."""
        
        self._search_butt.Enable(bool(value))
        self._search_butt.SetLabel(label)
    
    
    def EnableMoreButton(self, value):
        """Enables or disables next page button."""
        
        self._more_butt.Enable(bool(value))
    
    
    def EnableOkButton(self, value):
        """Enables or disables OK button."""
        
        self._ok_butt.Enable(bool(value))
    
    
    def _on_paint(self, evt):
        """Draws background image."""
        
        mwx.panel_top_h_bgr(self, images.BGR_TOP_BAR)
        mwx.panel_bottom_line(self, mwx.DARK_DIVIDER_COLOUR)
    
    
    def _on_search(self, evt=None):
        """Handles search event."""
        
        event = events.RepositorySearchEvent(self.GetId())
        wx.PostEvent(self, event)
    
    
    def _on_more(self, evt=None):
        """Handles more items event."""
        
        event = events.RepositoryMoreEvent(self.GetId())
        wx.PostEvent(self, event)
    
    
    def _on_ok(self, evt=None):
        """Handles OK event."""
        
        event = events.RepositoryOkEvent(self.GetId())
        wx.PostEvent(self, event)
    
    
    def _make_ui(self):
        """Makes panel UI."""
        
        # make items
        self._query_search = wx.SearchCtrl(self, size=(100,-1), style=wx.TE_PROCESS_ENTER)
        self._query_search.SetDescriptiveText("Search PubMed")
        self._query_search.ShowSearchButton(wx.Platform != "__WXMSW__")
        self._query_search.ShowCancelButton(True)
        
        self._search_butt = wx.Button(self, label="Search", size=(95, -1))
        
        self._more_butt = wx.Button(self, label=">>", size=(40, -1))
        self._more_butt.SetToolTip("Retrieve next batch of articles")
        self._more_butt.Enable(False)
        
        label = "Apply" if self._mode == 'match' else "Import"
        tooltip = "Annotate article by selected record" if self._mode == 'match' else "Import checked articles to library"
        self._ok_butt = wx.Button(self, label=label)
        self._ok_butt.SetToolTip(tooltip)
        self._ok_butt.Enable(False)
        
        # bind events
        self._query_search.Bind(wx.EVT_TEXT_ENTER, self._on_search)
        self._search_butt.Bind(wx.EVT_BUTTON, self._on_search)
        self._more_butt.Bind(wx.EVT_BUTTON, self._on_more)
        self._ok_butt.Bind(wx.EVT_BUTTON, self._on_ok)
        
        # add to sizer
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self._query_search, 1, wx.ALIGN_CENTER_VERTICAL)
        sizer.Add(self._search_butt, 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 10)
        sizer.Add(self._more_butt, 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 10)
        sizer.Add(self._ok_butt, 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 20)
        self.Sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.Sizer.Add(sizer, 1, wx.EXPAND | wx.ALL, 10)
