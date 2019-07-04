#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

# import modules
import wx
import wx.dataview as wxdv

from .. import mwx
from .list_model import LabelsListModel


class LabelsList(wx.Panel):
    """Labels list panel."""
    
    
    def __init__(self, parent):
        """Initializes labels list panel."""
        
        # init panel
        wx.Panel.__init__(self, parent, -1, style=wx.NO_FULL_REPAINT_ON_RESIZE)
        
        self._labels = []
        
        # make ui
        self._make_ui()
    
    
    def SetLabels(self, labels):
        """Sets labels to display."""
        
        # set data
        self._labels[:] = labels if labels else []
        
        # sort data
        self._labels.sort(key=lambda x:x.title)
        
        # update list
        self._list_model.Reset(len(self._labels))
        self._list_model.Resort()
    
    
    def _make_ui(self):
        """Makes panel UI."""
        
        # init list control
        self._list_ctrl = wxdv.DataViewCtrl(self, style=wx.NO_BORDER | wxdv.DV_ROW_LINES | wxdv.DV_VERT_RULES)
        self._list_model = LabelsListModel(self._labels)
        self._list_ctrl.AssociateModel(self._list_model)

        # add columns
        self._list_ctrl.AppendTextColumn("Expander", 0, width=0, mode=wxdv.DATAVIEW_CELL_INERT, align=wx.ALIGN_CENTER)
        self._list_ctrl.AppendToggleColumn("", 1, width=30, mode=wxdv.DATAVIEW_CELL_ACTIVATABLE, align=wx.ALIGN_CENTER)
        self._list_ctrl.AppendTextColumn("Label", 2, width=235, mode=wxdv.DATAVIEW_CELL_INERT, align=wx.ALIGN_LEFT)
        
        # hide expander column
        self._list_ctrl.Columns[0].SetHidden(True)
        
        # set columns properties
        for c in self._list_ctrl.Columns:
            c.Sortable = True
            c.Reorderable = False
            c.GetRenderer().EnableEllipsize(wx.ELLIPSIZE_END)
        
        # set sort column
        self._list_ctrl.GetColumn(2).SetSortOrder(True)
        
        # add to sizer
        self.Sizer = wx.BoxSizer(wx.VERTICAL)
        self.Sizer.Add(self._list_ctrl, 1, wx.EXPAND | wx.ALL, mwx.LIST_CTRL_SPACE)
