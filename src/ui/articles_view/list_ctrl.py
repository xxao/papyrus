#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

# import modules
import wx
import wx.dataview as wxdv

from .. import config
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
        self._columns = []
        
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
    
    
    def GetColumnsSettings(self):
        """Gets current column order and settings."""
        
        # init buffer
        columns = [None]*len(self._columns)
        columns[0] = ['expander', False, 0, None]
        
        # get sorting column
        sort_column = self._list_ctrl.GetSortingColumn()
        
        # get settings
        for i in range(1, len(self._columns)):
            
            name = self._columns[i][0]
            col = self._list_ctrl.GetColumn(i)
            pos = self._list_ctrl.GetColumnPosition(col)
            sorting = col.SortOrder if (col is sort_column) else None
            
            columns[pos] = (name, col.Shown, col.Width, sorting)
        
        return columns
    
    
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
        
        # get columns
        self._columns = self._init_columns()
        names = [c[0] for c in self._columns]
        
        # init list control
        self._list_ctrl = wxdv.DataViewCtrl(self, style=wx.NO_BORDER|wxdv.DV_ROW_LINES|wxdv.DV_VERT_RULES|wxdv.DV_MULTIPLE)
        self._list_model = ArticlesListModel(names, self._articles)
        self._list_ctrl.AssociateModel(self._list_model)
        self._list_ctrl.EnableDragSource(mwx.ArticlesIDsDropData().GetFormat())
        
        # add columns
        idx = 0
        for name, header, style, visible, width, align, sorting in self._columns:
            if style == 'bitmap':
                self._list_ctrl.AppendBitmapColumn(header, idx, width=width, mode=wxdv.DATAVIEW_CELL_INERT, align=align)
            else:
                self._list_ctrl.AppendTextColumn(header, idx, width=width, mode=wxdv.DATAVIEW_CELL_INERT, align=align)
            idx += 1
        
        # hide expander column
        self._list_ctrl.Columns[0].SetHidden(not visible)
        
        # set columns properties
        for i, c in enumerate(self._list_ctrl.Columns):
            
            c.Sortable = True
            c.Reorderable = True
            c.GetRenderer().EnableEllipsize(wx.ELLIPSIZE_END)
            
            sort_order = self._columns[i][6]
            if sort_order is not None:
                c.SetSortOrder(sort_order)
        
        # bind events
        self._list_ctrl.Bind(wxdv.EVT_DATAVIEW_SELECTION_CHANGED, self._on_selection_changed)
        self._list_ctrl.Bind(wxdv.EVT_DATAVIEW_ITEM_ACTIVATED, self._on_item_activated)
        self._list_ctrl.Bind(wxdv.EVT_DATAVIEW_ITEM_BEGIN_DRAG, self._on_begin_drag)
        self._list_ctrl.Bind(wxdv.EVT_DATAVIEW_ITEM_CONTEXT_MENU, self._on_item_context_menu)
        self._list_ctrl.Bind(wx.EVT_RIGHT_UP, self._on_item_context_menu)
        
        # add to sizer
        self.Sizer = wx.BoxSizer(wx.VERTICAL)
        self.Sizer.Add(self._list_ctrl, 1, wx.EXPAND|wx.ALL, mwx.LIST_CTRL_SPACE)
    
    
    def _init_columns(self):
        """Initialize visible columns."""
        
        # get columns
        columns = (
            ['expander', "Expander", 'text', False, 0, wx.ALIGN_CENTER, None],
            ['colour', "", 'bitmap', True, 24, wx.ALIGN_CENTER, None],
            ['pdf', "", 'bitmap', True, 24, wx.ALIGN_CENTER, None],
            ['rating', "Rating", 'bitmap', True, 70, wx.ALIGN_CENTER, None],
            ['authors', "Authors", 'text', True, 180, wx.ALIGN_LEFT, None],
            ['title', "Title", 'text', True, 360, wx.ALIGN_LEFT, None],
            ['journal', "Journal", 'text', True, 180, wx.ALIGN_LEFT, None],
            ['year', "Year", 'text', True, 45, wx.ALIGN_CENTER, None],
            ['volume', "Volume", 'text', True, 60, wx.ALIGN_CENTER, None],
            ['issue', "Issue", 'text', True, 45, wx.ALIGN_CENTER, None],
            ['pages', "Pages", 'text', True, 90, wx.ALIGN_CENTER, None],
            ['doi', "DOI", 'text', True, 200, wx.ALIGN_LEFT, None],
            ['key', "Key", 'text', True, 60, wx.ALIGN_CENTER, None],
            ['pmid', "PMID", 'text', True, 70, wx.ALIGN_CENTER, None],
            ['imported', "Imported", 'text', True, 90, wx.ALIGN_CENTER, False],
            ['labels', "Labels", 'text', True, 200, wx.ALIGN_LEFT, None],
        )
        
        # apply user settings
        if config.SETTINGS['articles_view_columns']:
            
            try:
                
                # init lookup
                pos = -len(columns)
                lookup = {c[0]:[i,c] for i,c in enumerate(columns)}
                lookup['expander'][0] = pos - 1
                
                # update columns
                for name, visible, width, sorting in config.SETTINGS['articles_view_columns']:
                    
                    # get column
                    column = lookup.get(name, None)
                    if column is None:
                        continue
                    
                    # update column
                    column[1][3] = bool(visible)
                    column[1][4] = int(width)
                    column[1][6] = sorting
                    
                    # update position
                    column[0] = pos
                    pos += 1
                
                # get final sorted columns
                columns = sorted(lookup.values(), key=lambda c:c[0])
                columns = [c[1] for c in columns]
            
            except:
                pass
        
        return columns
