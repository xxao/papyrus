#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

# import modules
import wx
import wx.dataview as wxdv

from .. import mwx
from .. import events
from .list_model import AuthorsListModel


class AuthorsList(wx.Panel):
    """Authors list panel."""
    
    
    def __init__(self, parent):
        """Initializes authors list panel."""
        
        # init panel
        wx.Panel.__init__(self, parent, -1, style=wx.NO_FULL_REPAINT_ON_RESIZE)
        
        # init buff
        self._authors = []
        
        # make ui
        self._make_ui()
    
    
    def SetAuthors(self, authors):
        """Sets authors to display."""
        
        # unselect all
        self._list_ctrl.UnselectAll()
        
        # set data
        before = len(self._authors)
        self._authors[:] = authors if authors else []
        after = len(self._authors)
        diff = after - before
        
        # add rows
        if diff > 0:
            for i in range(diff):
                self._list_model.RowAppended()
        
        # remove rows
        elif diff < 0:
            self._list_model.RowsDeleted(range(after, before))
        
        # update list
        self._list_model.Resort()
        
        # post selection changed event
        self._on_selection_changed(None)
    
    
    def SetSelectedAuthors(self, authors):
        """Selects specified authors."""
        
        # get authors IDs
        ids = [x.dbid for x in authors]
        
        # select items
        for row, article in enumerate(self._authors):
            if article.dbid in ids:
                item = self._list_model.GetItem(row)
                self._list_ctrl.Select(item)
    
    
    def GetSelectedAuthors(self):
        """Gets list of selected authors."""
        
        # get selected items
        items = self._list_ctrl.GetSelections()
        rows = [self._list_model.GetRow(x) for x in items]
        
        # get authors
        return [self._authors[x] for x in rows]
    
    
    def _on_selection_changed(self, evt):
        """Handles row selection event."""
        
        event = events.AuthorsSelectionChangedEvent(self.GetId())
        wx.PostEvent(self, event)
    
    
    def _on_item_activated(self, evt):
        """Handles row activation event."""
        
        event = events.AuthorsItemActivatedEvent(self.GetId())
        wx.PostEvent(self, event)
    
    
    def _on_item_context_menu(self, evt):
        """Handles context menu event."""
        
        event = events.AuthorsItemContextMenuEvent(self.GetId())
        wx.PostEvent(self, event)
    
    
    def _make_ui(self):
        """Makes panel UI."""
        
        # init list control
        self._list_ctrl = wxdv.DataViewCtrl(self, style=wx.NO_BORDER | wxdv.DV_ROW_LINES | wxdv.DV_VERT_RULES | wxdv.DV_MULTIPLE)
        
        # associate model
        self._list_model = AuthorsListModel(self._authors)
        self._list_ctrl.AssociateModel(self._list_model)
        
        # add columns
        self._list_ctrl.AppendTextColumn("Expander", 0, width=0, mode=wxdv.DATAVIEW_CELL_INERT, align=wx.ALIGN_CENTER)
        self._list_ctrl.AppendTextColumn("Last Name", 1, width=150, mode=wxdv.DATAVIEW_CELL_INERT, align=wx.ALIGN_LEFT)
        self._list_ctrl.AppendTextColumn("First Name", 2, width=150, mode=wxdv.DATAVIEW_CELL_INERT, align=wx.ALIGN_LEFT)
        self._list_ctrl.AppendTextColumn("Initials", 3, width=80, mode=wxdv.DATAVIEW_CELL_INERT, align=wx.ALIGN_LEFT)
        self._list_ctrl.AppendTextColumn("Articles", 4, width=50, mode=wxdv.DATAVIEW_CELL_INERT, align=wx.ALIGN_LEFT)
        
        # hide some columns
        self._list_ctrl.Columns[0].SetHidden(True)
        
        # set columns properties
        for c in self._list_ctrl.Columns:
            c.Sortable = True
            c.Reorderable = False
            c.GetRenderer().EnableEllipsize(wx.ELLIPSIZE_END)
        
        # bind events
        self._list_ctrl.Bind(wxdv.EVT_DATAVIEW_SELECTION_CHANGED, self._on_selection_changed)
        self._list_ctrl.Bind(wxdv.EVT_DATAVIEW_ITEM_ACTIVATED, self._on_item_activated)
        self._list_ctrl.Bind(wxdv.EVT_DATAVIEW_ITEM_CONTEXT_MENU, self._on_item_context_menu)
        
        # add to sizer
        self.Sizer = wx.BoxSizer(wx.VERTICAL)
        self.Sizer.Add(self._list_ctrl, 1, wx.EXPAND | wx.ALL, mwx.LIST_CTRL_SPACE)
