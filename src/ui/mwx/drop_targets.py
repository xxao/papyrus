#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

# import modules
import wx
import pickle


class FileDropTarget(wx.FileDropTarget):
    """Represents file drop target."""
    
    
    def __init__(self, func):
        """Initializes a new instance of FileDropTarget."""
        
        wx.FileDropTarget.__init__(self)
        self._func = func
    
    
    def OnDropFiles(self, x, y, paths):
        """Opens dropped files."""
        
        wx.CallAfter(self._func, paths)
        return True


class ArticlesIDsDropData(wx.CustomDataObject):
    """Represents articles IDs drop data."""
    
    NAME = "ARTICLES_IDS"
    PICKLE_PROTOCOL = 2
    
    
    def __init__(self):
        """Initializes a new instance of ArticlesIDsDropTarget."""
        
        wx.CustomDataObject.__init__(self, ArticlesIDsDropData.NAME)
    
    
    def SetIDs(self, ids):
        """Sets articles IDs to hold."""
        
        data = pickle.dumps(ids, 2)
        self.SetData(data)
    
    
    def GetIDs(self):
        """Gets stored articles IDs."""
        
        return pickle.loads(self.GetData())


class ArticlesIDsDropTarget(wx.DropTarget):
    """Represents articles IDs drop target."""
    
    
    def __init__(self, obj):
        """Initializes a new instance of ArticlesIDsDropTarget."""

        wx.DropTarget.__init__(self)
        
        self._obj = obj
        
        self.data = ArticlesIDsDropData()
        self.SetDataObject(self.data)
    
    
    def OnDragOver(self, x, y, result):
        """Gets a flag informing whether the drop position is valid."""
        
        if not self._obj.IsDropPossible(x, y):
            return wx.DragNone
        
        return result
    
    
    def OnDrop(self, x, y):
        """Gets a flag informing whether the drop position is valid."""
        
        return self._obj.IsDropPossible(x, y)
    
    
    def OnData(self, x, y, result):
        """Calls target drop function."""
        
        if not self.GetData():
            return wx.DragNone
        
        wx.CallAfter(self._obj.DropArticles, x, y, self.data.GetIDs())
        
        return result
