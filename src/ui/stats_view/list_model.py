#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

# import modules
import wx
import wx.dataview as wxdv

from .. import mwx
from .. import images


class StatsListModel(wxdv.DataViewIndexListModel):
    """Statistics list data source model."""
    
    
    def __init__(self, data=None):
        """Initializes data source model."""
        
        self._data = data if data is not None else []
        self._col_names = [
            'expander',
            'label',
            'bar',
            'count',
            'perc']
        
        wxdv.DataViewIndexListModel.__init__(self, len(self._data))
    
    
    def GetColumnType(self, col):
        """Gets type of specified column."""
        
        # return type
        if col == "bar":
            return "bitmap"
        
        return "string"
    
    
    def GetValueByRow(self, row, col):
        """Gets value for given row and column."""
        
        # get column name
        name = self._col_names[col]
        
        # get native value
        value = self.GetItemValue(self._data[row], col)
        
        # check value
        if value is None:
            return ""
        
        # return values
        if name == "expander":
            return ""
        
        if name == "label":
            return str(value)
        
        if name == "bar":
            return self._make_bar(value)
        
        if name == "count":
            return str(value)
        
        if name == "perc":
            return "%.0f" % (100*value)
    
    
    def GetItemValue(self, item, col):
        """Gets native column value from given item."""
        
        # get column name
        name = self._col_names[col]
        
        # return value
        if name == "expander":
            return ""
        
        if name == "label":
            return item[0]
        
        if name == "bar":
            return item[1]
        
        if name == "count":
            return item[1]
        
        if name == "perc":
            return item[2]
    
    
    def GetColumnCount(self):
        """Returns number of available columns."""
        
        return len(self._col_names)
    
    
    def GetCount(self):
        """Returns number of available rows."""
        
        return len(self._data)
    
    
    def GetAttrByRow(self, row, col, attr):
        """Returns specific attributes."""
        
        return False
    
    
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
        
        # compare values
        return (value1 > value2) - (value1 < value2)
    
    
    def _make_bar(self, value):
        """Gets bar for given value."""
        
        width = 305 * value / max(x[1] for x in self._data)
        
        img = images.bar(
            width = width,
            height = 11,
            outline = wx.Pen(mwx.STATSBAR_OUTLINE_COLOUR, 1, wx.PENSTYLE_SOLID),
            fill = wx.Brush(mwx.STATSBAR_FILL_COLOUR, wx.BRUSHSTYLE_SOLID))
        
        return img
