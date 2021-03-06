#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

# import modules
import wx
import datetime

import core
from .. import mwx
from .list_ctrl import StatsList


class StatsView(wx.Dialog):
    """Statistics view panel."""
    
    
    def __init__(self, parent, library):
        """Initializes repository view panel."""
        
        # init panel
        wx.Dialog.__init__(self, parent, -1, size=(658, 500), title="Library Statistics", style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)
        
        # set library
        self._library = library
        
        # make UI
        self._make_ui()
        
        # show frame
        self.Layout()
        self.Centre(wx.BOTH)
        self.Show(True)
        
        # set min size
        self.SetMinSize(self.GetSize())
        
        # update data
        self.UpdateData()
    
    
    def SetLibrary(self, library=None):
        """Sets current library."""
        
        self._library = library
        self.UpdateData()
    
    
    def UpdateData(self):
        """Refreshes data from current library."""
        
        # show busy status
        self._status_label.SetLabel("Analyzing library...")
        self.Sizer.Show(1)
        self.Layout()
        wx.Yield()
        
        # analyze data
        self._show_data()
        
        # update status
        self._status_label.SetLabel("Ready" if self._library is not None else "No library available!")
        self.Sizer.Hide(1)
        self.Layout()
    
    
    def _make_ui(self):
        """Makes panel UI."""
        
        # make notebook
        notebook = wx.Notebook(self)
        
        # make authors page
        authors_page = wx.Panel(notebook)
        self._authors_list = StatsList(authors_page, "Author")
        notebook.AddPage(authors_page, "Authors")
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self._authors_list, 1, wx.ALL | wx.EXPAND)
        authors_page.SetSizer(sizer)

        # make journals page
        journals_page = wx.Panel(notebook)
        self._journals_list = StatsList(journals_page, "Journal")
        notebook.AddPage(journals_page, "Journals")
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self._journals_list, 1, wx.ALL | wx.EXPAND)
        journals_page.SetSizer(sizer)

        # make labels page
        labels_page = wx.Panel(notebook)
        self._labels_list = StatsList(labels_page, "Label")
        notebook.AddPage(labels_page, "Labels")
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self._labels_list, 1, wx.ALL | wx.EXPAND)
        labels_page.SetSizer(sizer)

        # make publisher year page
        published_page = wx.Panel(notebook)
        self._published_list = StatsList(published_page, "Year")
        notebook.AddPage(published_page, "Published")
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self._published_list, 1, wx.ALL | wx.EXPAND)
        published_page.SetSizer(sizer)

        # make imported year page
        imported_page = wx.Panel(notebook)
        self._imported_list = StatsList(imported_page, "Year")
        notebook.AddPage(imported_page, "Imported")
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self._imported_list, 1, wx.ALL | wx.EXPAND)
        imported_page.SetSizer(sizer)
        
        # make status
        self._status_label = wx.StaticText(self, -1, "No library available!")
        
        # pack all
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(notebook, 1, wx.ALL | wx.EXPAND, mwx.PANEL_SPACE_MAIN)
        sizer.Add(self._status_label, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM, mwx.PANEL_SPACE_MAIN)
        self.SetSizer(sizer)
    
    
    def _show_data(self):
        """Loads all data."""
        
        # reset current data
        self._authors_list.SetItems([])
        self._journals_list.SetItems([])
        self._labels_list.SetItems([])
        self._published_list.SetItems([])
        self._imported_list.SetItems([])
        
        # check library
        if self._library is None:
            return
        
        # load articles
        query = core.Query("", core.Article.NAME)
        articles = self._library.search(query)
        total = len(articles)
        
        # update authors
        items = []
        query = core.Query("", core.Author.NAME)
        data = self._library.search(query)
        for item in data:
            count = self._library.count(item)
            items.append((item.longname, count, count/total))
        
        self._authors_list.SetItems(items)
        
        # update journals
        items = []
        query = core.Query("", core.Journal.NAME)
        data = self._library.search(query)
        for item in data:
            count = self._library.count(item)
            items.append((item.abbreviation, count, count/total))
        
        self._journals_list.SetItems(items)
        
        # update labels
        items = []
        query = core.Query("", core.Label.NAME)
        data = self._library.search(query)
        for item in data:
            count = self._library.count(item)
            items.append((item.title, count, count/total))
        
        self._labels_list.SetItems(items)
        
        # update years
        published = {}
        imported = {}
        
        for item in articles:
            
            # year published
            if item.year is not None:
                year = item.year
                published[year] = 1 + published.get(year, 0)
            
            # year imported
            if item.imported is not None:
                year = datetime.datetime.utcfromtimestamp(item.imported).strftime('%Y')
                imported[year] = 1 + imported.get(year, 0)
        
        self._published_list.SetItems([(k, v, v/total) for k,v in published.items()])
        self._imported_list.SetItems([(k, v, v/total) for k,v in imported.items()])
