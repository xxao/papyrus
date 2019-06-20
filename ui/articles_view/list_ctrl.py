#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

# import modules
import wx
import wx.dataview as wxdv

from .. import mwx
from .. import events
from . list_model import ArticlesListModel


class ArticlesList(wx.Panel):
    """Articles list panel."""
    
    
    def __init__(self, parent):
        """Initializes articles list panel."""
        
        # init panel
        wx.Panel.__init__(self, parent, -1, style=wx.NO_FULL_REPAINT_ON_RESIZE)
        
        # init buffers
        self._articles = []
        
        # make ui
        self._make_ui()
    
    
    def SetArticles(self, articles):
        """Sets articles to display."""
        
        # unselect all
        self._list_ctrl.UnselectAll()
        
        # set data
        self._articles[:] = articles if articles else []
        
        # update list
        self._list_model.Reset(len(self._articles))
        self._list_model.Resort()
        
        # post selection changed event
        self._on_selection_changed(None)
    
    
    def GetSelectedArticles(self):
        """Gets list of selected articles."""
        
        # get selected items
        items = self._list_ctrl.GetSelections()
        rows = [self._list_model.GetRow(x) for x in items]
        
        # get articles
        return [self._articles[x] for x in rows]
    
    
    def SetSelectedArticles(self, articles):
        """Selects specified articles."""
        
        # get articles IDs
        ids = [x.dbid for x in articles]
        
        # select items
        for row, article in enumerate(self._articles):
            if article.dbid in ids:
                item = self._list_model.GetItem(row)
                self._list_ctrl.Select(item)
    
    
    def _on_selection_changed(self, evt):
        """Handles row selection event."""
        
        event = events.ArticlesSelectionChangedEvent(self.GetId())
        wx.PostEvent(self, event)
    
    
    def _on_item_activated(self, evt):
        """Handles row activation event."""
        
        event = events.ArticlesItemActivatedEvent(self.GetId())
        wx.PostEvent(self, event)
    
    
    def _on_item_context_menu(self, evt):
        """Handles context menu event."""
        
        event = events.ArticlesItemContextMenuEvent(self.GetId())
        wx.PostEvent(self, event)
    
    
    def _on_begin_drag(self, evt):
        """Handles items dragging event."""
        
        # get articles
        articles = self.GetSelectedArticles()
        if not articles:
            evt.Skip()
            return
        
        # make articles IDs data
        data = mwx.ArticlesIDsDropData()
        data.SetIDs([a.dbid for a in articles])
        
        # make drop source
        source = wx.DropSource(self)
        source.SetData(data)
        source.DoDragDrop(wx.Drag_DefaultMove)
        
        # skip event
        evt.Skip()
    
    
    def _make_ui(self):
        """Makes panel UI."""
        
        # init list control
        self._list_ctrl = wxdv.DataViewCtrl(self, style=wx.NO_BORDER|wxdv.DV_ROW_LINES|wxdv.DV_VERT_RULES|wxdv.DV_MULTIPLE)
        self._list_model = ArticlesListModel(self._articles)
        self._list_ctrl.AssociateModel(self._list_model)
        self._list_ctrl.EnableDragSource(mwx.ArticlesIDsDropData().GetFormat())
        
        # add columns
        self._list_ctrl.AppendTextColumn("Expander", 0, width=0, mode=wxdv.DATAVIEW_CELL_INERT, align=wx.ALIGN_CENTER)
        self._list_ctrl.AppendBitmapColumn("", 1, width=24, mode=wxdv.DATAVIEW_CELL_INERT, align=wx.ALIGN_CENTER)
        self._list_ctrl.AppendBitmapColumn("", 2, width=24, mode=wxdv.DATAVIEW_CELL_INERT, align=wx.ALIGN_CENTER)
        self._list_ctrl.AppendBitmapColumn("Rating", 3, width=70, mode=wxdv.DATAVIEW_CELL_INERT, align=wx.ALIGN_CENTER)
        self._list_ctrl.AppendTextColumn("Author", 4, width=180, mode=wxdv.DATAVIEW_CELL_INERT, align=wx.ALIGN_LEFT)
        self._list_ctrl.AppendTextColumn("Title", 5, width=360, mode=wxdv.DATAVIEW_CELL_INERT, align=wx.ALIGN_LEFT)
        self._list_ctrl.AppendTextColumn("Journal", 6, width=180, mode=wxdv.DATAVIEW_CELL_INERT, align=wx.ALIGN_LEFT)
        self._list_ctrl.AppendTextColumn("Imported", 7, width=90, mode=wxdv.DATAVIEW_CELL_INERT, align=wx.ALIGN_CENTER)
        self._list_ctrl.AppendTextColumn("Year", 8, width=45, mode=wxdv.DATAVIEW_CELL_INERT, align=wx.ALIGN_CENTER)
        self._list_ctrl.AppendTextColumn("Volume", 9, width=60, mode=wxdv.DATAVIEW_CELL_INERT, align=wx.ALIGN_CENTER)
        self._list_ctrl.AppendTextColumn("Issue", 10, width=45, mode=wxdv.DATAVIEW_CELL_INERT, align=wx.ALIGN_CENTER)
        self._list_ctrl.AppendTextColumn("Pages", 11, width=90, mode=wxdv.DATAVIEW_CELL_INERT, align=wx.ALIGN_CENTER)
        self._list_ctrl.AppendTextColumn("DOI", 12, width=200, mode=wxdv.DATAVIEW_CELL_INERT, align=wx.ALIGN_LEFT)
        self._list_ctrl.AppendTextColumn("Key", 13, width=60, mode=wxdv.DATAVIEW_CELL_INERT, align=wx.ALIGN_CENTER)
        self._list_ctrl.AppendTextColumn("PMID", 14, width=70, mode=wxdv.DATAVIEW_CELL_INERT, align=wx.ALIGN_CENTER)
        self._list_ctrl.AppendTextColumn("Labels", 15, width=200, mode=wxdv.DATAVIEW_CELL_INERT, align=wx.ALIGN_LEFT)
        
        # hide expander column
        self._list_ctrl.Columns[0].SetHidden(True)
        
        # set columns properties
        for c in self._list_ctrl.Columns:
            c.Sortable = True
            c.Reorderable = True
            c.GetRenderer().EnableEllipsize(wx.ELLIPSIZE_END)
        
        # bind events
        self._list_ctrl.Bind(wxdv.EVT_DATAVIEW_SELECTION_CHANGED, self._on_selection_changed)
        self._list_ctrl.Bind(wxdv.EVT_DATAVIEW_ITEM_ACTIVATED, self._on_item_activated)
        self._list_ctrl.Bind(wxdv.EVT_DATAVIEW_ITEM_BEGIN_DRAG, self._on_begin_drag)
        self._list_ctrl.Bind(wxdv.EVT_DATAVIEW_ITEM_CONTEXT_MENU, self._on_item_context_menu)
        self._list_ctrl.Bind(wx.EVT_RIGHT_UP, self._on_item_context_menu)
        
        # add to sizer
        self.Sizer = wx.BoxSizer(wx.VERTICAL)
        self.Sizer.Add(self._list_ctrl, 1, wx.EXPAND|wx.ALL, mwx.LIST_CTRL_SPACE)
