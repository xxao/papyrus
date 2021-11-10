#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

# import modules
import wx
import wx.dataview as wxdv

from .. import mwx


class AuthorsListModel(wxdv.DataViewIndexListModel):
    """Authors list data source model."""
    
    
    def __init__(self, data=None):
        """Initializes data source model."""
        
        self._data = data if data is not None else []
        self._col_names = [
            'expander',
            'lastname',
            'firstname',
            'initials',
            'count']
        
        wxdv.DataViewIndexListModel.__init__(self, len(self._data))
    
    
    def GetColumnType(self, col):
        """Gets type of specified column."""
        
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
        
        if name == "lastname":
            return value
        
        if name == "firstname":
            return value
        
        if name == "initials":
            return value
        
        if name == "count":
            return str(value)
        
        if value is None:
            return ""
    
    
    def GetItemValue(self, item, col):
        """Gets native column value from given item."""
        
        # get column name
        name = self._col_names[col]
        
        # return value
        if name == "expander":
            return ""
        
        if name == "lastname":
            return item.lastname
        
        if name == "firstname":
            return item.firstname
        
        if name == "initials":
            return item.initials
        
        if name == "title":
            return item.title
        
        if name == "count":
            return item.count
    
    
    def GetColumnCount(self):
        """Returns number of available columns."""
        
        return len(self._col_names)
    
    
    def GetCount(self):
        """Returns number of available rows."""
        
        return len(self._data)
    
    
    def GetAttrByRow(self, row, col, attr):
        """Returns specific attributes."""
        
        # mark orphan authors
        if self._data[row].count == 0:
            attr.SetColour(wx.Colour(mwx.AUTHOR_ORPHAN_COLOUR))
            return True
        
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
