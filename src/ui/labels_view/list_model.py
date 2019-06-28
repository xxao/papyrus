#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

# import modules
import wx.dataview as wxdv


class LabelsListModel(wxdv.PyDataViewIndexListModel):
    """Labels list data source model."""
    
    
    def __init__(self, data=None):
        """Initializes list data source model."""
        
        self._data = data if data is not None else []
        self._col_names = [
            'expander',
            'checked',
            'title']
        
        wxdv.DataViewIndexListModel.__init__(self, len(self._data))
    
    
    def GetColumnType(self, col):
        """Gets type of specified column."""
        
        # get column name
        name =  self._col_names[col]
        
        # return type
        if name == "checked":
            return "bool"
        
        return "string"
    
    
    def GetValueByRow(self, row, col):
        """Gets value for given row and column."""
        
        # get column name
        name =  self._col_names[col]
        
        # get native value
        value = self.GetItemValue(self._data[row], col)
        
        # return values
        if name == "expander":
            return ""
            
        if name == "checked":
            return value
        
        if name == "title":
            return value
    
    
    def GetItemValue(self, item, col):
        """Gets native column value from given item."""
        
        # get column name
        name =  self._col_names[col]
        
        # return value
        if name == "expander":
            return ""
        
        if name == "checked":
            return item.checked
        
        if name == "title":
            return item.title
    
    
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
        
        # get label
        label = self._data[row]
        
        # get column name
        name =  self._col_names[col]
        
        # return value
        if name == "checked":
            label.checked = value
        
        elif name == "title":
            label.title = value
        
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
        
        # compare values
        return (value1>value2)-(value1<value2)
