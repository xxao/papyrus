#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

# import modules
import wx
import wx.dataview as wxdv

from .. import mwx
from .. import images


class RepositoryListModel(wxdv.DataViewIndexListModel):
    """Repository list data source model."""
    
    
    def __init__(self, data=None):
        """Initializes data source model."""
        
        self._data = data if data is not None else []
        self._init_status_bullets()
        self._col_names = [
            'expander',
            'status',
            'checked',
            'authors',
            'title',
            'journal',
            'year',
            'volume',
            'issue']
        
        wxdv.DataViewIndexListModel.__init__(self, len(self._data))
    
    
    def GetColumnType(self, col):
        """Gets type of specified column."""
        
        # return type
        if col == "status":
            return "bitmap"
        
        if col == "checked":
            return "bool"
        
        return "string"
    
    
    def GetValueByRow(self, row, col):
        """Gets value for given row and column."""
        
        # get column name
        name = self._col_names[col]
        
        # get native value
        value = self.GetItemValue(self._data[row], col)
        
        # return values
        if name == "expander":
            return ""
        
        if name == "status":
            return self._status_on if value else self._status_off
            
        if name == "checked":
            return value
        
        if value is None:
            return ""
        
        if name == "authors":
            return self._get_authors(value)
        
        if name == "title":
            return value
        
        if name == "journal":
            return value
        
        if name == "year":
            return str(value)
        
        if name == "volume":
            return value
        
        if name == "issue":
            return value
    
    
    def GetItemValue(self, item, col):
        """Gets native column value from given item."""
        
        # get column name
        name = self._col_names[col]
        
        # return value
        if name == "expander":
            return ""
        
        if name == "status":
            return item.in_library
        
        if name == "checked":
            return item.checked
        
        if name == "authors":
            return item.authors
        
        if name == "title":
            return item.title
        
        if name == "journal":
            return item.journal.abbreviation if item.journal else None
        
        if name == "year":
            return item.year
        
        if name == "volume":
            return item.volume
        
        if name == "issue":
            return item.issue
    
    
    def GetColumnCount(self):
        """Returns number of available columns."""
        
        return len(self._col_names)
    
    
    def GetCount(self):
        """Returns number of available rows."""
        
        return len(self._data)
    
    
    def GetAttrByRow(self, row, col, attr):
        """Returns specific attributes."""
        
        return False
    

    def SetValueByRow(self, value, row, col):
        """Sets new value into item."""
        
        # get article
        article = self._data[row]
        
        # get column name
        name = self._col_names[col]
        
        # return value
        if name == "checked":
            article.checked = value
        
        return True
    
    
    def Compare(self, item1, item2, col, ascending):
        """Compares given items by specific column."""
        
        # swap sort order
        if not ascending:
            item2, item1 = item1, item2
        
        # get corresponding rows
        row1 = self.GetRow(item1)
        row2 = self.GetRow(item2)
        
        # get native values
        value1 = self.GetItemValue(self._data[row1], col)
        value2 = self.GetItemValue(self._data[row2], col)
        
        # check for None
        if value1 is None:
            return -1
        if value2 is None:
            return 1
        
        # get column name
        name = self._col_names[col]
        
        # convert specific values
        if name == 'authors' and value1 and value2:
            value1 = value1[0].shortname
            value2 = value2[0].shortname
        
        # compare values
        return (value1 > value2) - (value1 < value2)
    
    
    def _init_status_bullets(self):
        """Initializes bullet icon for in-library status."""
        
        self._status_on = images.bullet(
            radius = mwx.LIBSTATUS_SIZE,
            outline = wx.Pen(mwx.LIBSTATUS_OUTLINE_COLOUR, 1, wx.SOLID),
            fill = wx.Brush(mwx.LIBSTATUS_ON_COLOUR, wx.SOLID))
        
        self._status_off = images.bullet(
            radius = mwx.LIBSTATUS_SIZE,
            outline = wx.Pen(mwx.LIBSTATUS_OUTLINE_COLOUR, 1, wx.SOLID),
            fill = wx.Brush(mwx.LIBSTATUS_OFF_COLOUR, wx.SOLID))
    
    
    def _get_authors(self, authors):
        """Formats authors."""
        
        # check authors
        if not authors:
            return ""
        
        # one author only
        if len(authors) == 1:
            return authors[0].shortname
        
        # two authors
        if len(authors) == 2:
            return "%s and %s" % (authors[0].shortname, authors[1].shortname)
        
        # more authors
        return "%s, %s et al." % (authors[0].shortname, authors[-1].shortname)
