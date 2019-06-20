#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

# import modules
import wx
import wx.dataview as wxdv

from .. import mwx
from .. import events
from .list_model import RepositoryListModel


class RepositoryList(wx.Panel):
    """Repository list panel."""
    
    
    def __init__(self, parent, mode):
        """Initializes repository list panel."""
        
        # init panel
        wx.Panel.__init__(self, parent, -1, style=wx.NO_FULL_REPAINT_ON_RESIZE)
        
        self._mode = mode
        self._articles = []
        
        # make ui
        self._make_ui()
    
    
    def SetArticles(self, articles):
        """Sets articles to display."""
        
        # set data
        self._articles[:] = articles if articles else []
        
        # update list
        self._list_model.Reset(len(self._articles))
        self._list_model.Resort()
    
    
    def GetSelectedArticles(self):
        """Gets list of selected articles."""
        
        # get selected items
        items = self._list_ctrl.GetSelections()
        rows = [self._list_model.GetRow(x) for x in items]
        
        # get articles
        return [self._articles[x] for x in rows]
    
    
    def _on_selection_changed(self, evt):
        """Handles row selection event."""
        
        event = events.RepositorySelectionChangedEvent(self.GetId())
        wx.PostEvent(self, event)
    
    
    def _on_item_activated(self, evt):
        """Handles row activation event."""
        
        event = events.RepositoryItemActivatedEvent(self.GetId())
        wx.PostEvent(self, event)
    
    
    def _on_item_context_menu(self, evt):
        """Handles context menu event."""
        
        event = events.RepositoryItemContextMenuEvent(self.GetId())
        wx.PostEvent(self, event)
    
    
    def _on_item_value_changed(self, evt):
        """Handles item value changed event."""
        
        event = events.RepositoryItemValueChangedEvent(self.GetId())
        wx.PostEvent(self, event)
    
    
    def _make_ui(self):
        """Makes panel UI."""
        
        # init list control
        self._list_ctrl = wxdv.DataViewCtrl(self, style=wx.NO_BORDER|wxdv.DV_ROW_LINES|wxdv.DV_VERT_RULES)
        
        # associate model
        self._list_model = RepositoryListModel(self._articles)
        self._list_ctrl.AssociateModel(self._list_model)

        # add columns
        self._list_ctrl.AppendTextColumn("Expander", 0, width=0, mode=wxdv.DATAVIEW_CELL_INERT, align=wx.ALIGN_CENTER)
        self._list_ctrl.AppendBitmapColumn("", 1, width=24, mode=wxdv.DATAVIEW_CELL_INERT, align=wx.ALIGN_CENTER)
        self._list_ctrl.AppendToggleColumn("", 2, width=30, mode=wxdv.DATAVIEW_CELL_ACTIVATABLE, align=wx.ALIGN_CENTER)
        self._list_ctrl.AppendTextColumn("Author", 3, width=190, mode=wxdv.DATAVIEW_CELL_INERT, align=wx.ALIGN_LEFT)
        self._list_ctrl.AppendTextColumn("Title", 4, width=440, mode=wxdv.DATAVIEW_CELL_INERT, align=wx.ALIGN_LEFT)
        self._list_ctrl.AppendTextColumn("Journal", 5, width=160, mode=wxdv.DATAVIEW_CELL_INERT, align=wx.ALIGN_LEFT)
        self._list_ctrl.AppendTextColumn("Year", 6, width=45, mode=wxdv.DATAVIEW_CELL_INERT, align=wx.ALIGN_CENTER)
        self._list_ctrl.AppendTextColumn("Volume", 7, width=60, mode=wxdv.DATAVIEW_CELL_INERT, align=wx.ALIGN_CENTER)
        self._list_ctrl.AppendTextColumn("Issue", 8, width=45, mode=wxdv.DATAVIEW_CELL_INERT, align=wx.ALIGN_CENTER)
        
        # hide some columns
        self._list_ctrl.Columns[0].SetHidden(True)
        self._list_ctrl.Columns[2].SetHidden(self._mode=='match')
        
        # set columns properties
        for c in self._list_ctrl.Columns:
            c.Sortable = True
            c.Reorderable = True
            c.GetRenderer().EnableEllipsize(wx.ELLIPSIZE_END)
        
        # bind events
        self._list_ctrl.Bind(wxdv.EVT_DATAVIEW_SELECTION_CHANGED, self._on_selection_changed)
        self._list_ctrl.Bind(wxdv.EVT_DATAVIEW_ITEM_ACTIVATED, self._on_item_activated)
        self._list_ctrl.Bind(wxdv.EVT_DATAVIEW_ITEM_CONTEXT_MENU, self._on_item_context_menu)
        self._list_ctrl.Bind(wxdv.EVT_DATAVIEW_ITEM_VALUE_CHANGED, self._on_item_value_changed)
        
        # add to sizer
        self.Sizer = wx.BoxSizer(wx.VERTICAL)
        self.Sizer.Add(self._list_ctrl, 1, wx.EXPAND|wx.ALL, mwx.LIST_CTRL_SPACE)
