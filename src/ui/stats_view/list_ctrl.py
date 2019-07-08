#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

# import modules
import wx
import wx.dataview as wxdv

from .. import mwx
from .list_model import StatsListModel


class StatsList(wx.Panel):
    """Statistics list panel."""
    
    
    def __init__(self, parent, label):
        """Initializes repository list panel."""
        
        # init panel
        wx.Panel.__init__(self, parent, -1, style=wx.NO_FULL_REPAINT_ON_RESIZE)
        
        # set buffs
        self._label = label
        self._items = []
        
        # make ui
        self._make_ui()
    
    
    def SetItems(self, items):
        """Sets items to display."""
        
        # set data
        self._items[:] = items if items else []
        
        # sort data
        self._items.sort(key=lambda x:x[1], reverse=True)
        
        # update list
        self._list_model.Reset(len(self._items))
        self._list_model.Resort()
    
    
    def _make_ui(self):
        """Makes panel UI."""
        
        # init list control
        self._list_ctrl = wxdv.DataViewCtrl(self, style=wx.NO_BORDER | wxdv.DV_ROW_LINES | wxdv.DV_VERT_RULES)
        
        # associate model
        self._list_model = StatsListModel(self._items)
        self._list_ctrl.AssociateModel(self._list_model)
        
        # add columns
        self._list_ctrl.AppendTextColumn("Expander", 0, width=0, mode=wxdv.DATAVIEW_CELL_INERT, align=wx.ALIGN_CENTER)
        self._list_ctrl.AppendTextColumn(self._label, 1, width=170, mode=wxdv.DATAVIEW_CELL_INERT, align=wx.ALIGN_LEFT)
        self._list_ctrl.AppendBitmapColumn("Bar", 2, width=315, mode=wxdv.DATAVIEW_CELL_INERT, align=wx.ALIGN_LEFT)
        self._list_ctrl.AppendTextColumn("Articles", 3, width=60, mode=wxdv.DATAVIEW_CELL_INERT, align=wx.ALIGN_RIGHT)
        self._list_ctrl.AppendTextColumn("%", 4, width=50, mode=wxdv.DATAVIEW_CELL_INERT, align=wx.ALIGN_RIGHT)
        
        # hide some columns
        self._list_ctrl.Columns[0].SetHidden(True)
        
        # set columns properties
        for c in self._list_ctrl.Columns:
            c.Sortable = True
            c.Reorderable = False
            c.GetRenderer().EnableEllipsize(wx.ELLIPSIZE_END)
        
        # add to sizer
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self._list_ctrl, 1, wx.EXPAND | wx.ALL, mwx.LIST_CTRL_SPACE)
        self.SetSizer(sizer)
