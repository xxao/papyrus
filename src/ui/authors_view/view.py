#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

# import modules
import wx

import core
from .. import events
from .. import mwx
from .. ids import *
from .list_ctrl import AuthorsList
from .top_bar import AuthorsTopBar
from .bottom_bar import AuthorsBottomBar
from .edit_dlg import AuthorsEditDlg


class AuthorsView(wx.Dialog):
    """Authors view panel."""
    
    
    def __init__(self, parent, library, query=""):
        """Initializes authors view panel."""
        
        # init panel
        wx.Dialog.__init__(self, parent, -1, size=(470, 400), title="Authors List", style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)
        self.Bind(wx.EVT_CLOSE, self._on_close)
        
        # set library
        self._library = library
        
        # init buffs
        self._authors = []
        self._changed = False
        
        # make UI
        self._make_ui()
        
        # show frame
        self.Layout()
        self.Centre(wx.BOTH)
        self.Show(True)
        
        # set min size
        self.SetMinSize(self.GetSize())
        
        # show authors
        self.SetQuery(query)
        self.ShowAuthors()
    
    
    def SetLibrary(self, library=None):
        """Sets current library."""
        
        self._library = library
        self.ShowAuthors()
    
    
    def SetQuery(self, value):
        """Sets query to top bar."""
        
        self._top_bar.ChangeQuery(value)
    
    
    def SetSelectedAuthors(self, authors):
        """Selects specified authors."""
        
        self._list.SetSelectedAuthors(authors)
    
    
    def ShowAuthors(self):
        """Shows authors according to current query."""
        
        # get current query
        query = self._top_bar.GetQuery()
        
        # shows authors
        self._show_authors(query)
    
    
    def GetSelectedAuthors(self):
        """Gets list of selected authors."""
        
        return self._list.GetSelectedAuthors()
    
    
    def _on_close(self, evt=None):
        """Handles close event."""
        
        if self._changed:
            self.EndModal(wx.ID_OK)
        else:
            self.EndModal(wx.ID_CANCEL)
    
    
    def _on_query_changed(self, evt=None):
        """Handles query changed event."""
        
        self.ShowAuthors()
    
    
    def _on_item_activated(self, evt=None):
        """Handles row activated event."""
        
        self._on_edit()
    
    
    def _on_item_context_menu(self, evt=None):
        """Handles article item context menu event."""
        
        # check library
        if self._library is None:
            return
        
        # get selected authors
        authors = self._list.GetSelectedAuthors()
        
        # init menu
        menu = wx.Menu()
        menu.Append(ID_AUTHORS_EDIT, "Edit...")
        menu.Append(ID_AUTHORS_MERGE, "Merge Selected...")
        menu.AppendSeparator()
        menu.Append(ID_AUTHORS_DELETE, "Delete Orphans")
        
        # enable items
        menu.Enable(ID_AUTHORS_EDIT, len(authors) == 1)
        menu.Enable(ID_AUTHORS_MERGE, len(authors) > 1)
        menu.Enable(ID_AUTHORS_DELETE, all(x.count == 0 for x in authors))
        
        # bind events
        self.Bind(wx.EVT_MENU, self._on_edit, id=ID_AUTHORS_EDIT)
        self.Bind(wx.EVT_MENU, self._on_merge, id=ID_AUTHORS_MERGE)
        self.Bind(wx.EVT_MENU, self._on_delete, id=ID_AUTHORS_DELETE)
        
        # show menu
        self.PopupMenu(menu)
        menu.Destroy()
    
    
    def _on_edit(self, evt=None):
        """Handles edit event."""
        
        # get selected authors
        authors = self._list.GetSelectedAuthors()
        if len(authors) != 1:
            return
        
        # get author
        author = authors[0]
        
        # raise edit dialog
        dlg = AuthorsEditDlg(self, author, "edit")
        response = dlg.ShowModal()
        dlg.Destroy()
        
        # check response
        if response != wx.ID_OK:
            return
        
        # update library
        self._library.update(author)
        self._changed = True
        
        # update authors
        self.ShowAuthors()
        self.SetSelectedAuthors([author])
    
    
    def _on_merge(self, evt=None):
        """Handles merge event."""
        
        # get selected authors
        authors = self._list.GetSelectedAuthors()
        if len(authors) < 2:
            return
        
        # get master
        master = max(authors, key=lambda a: len(a.firstname))
        
        # raise edit dialog
        dlg = AuthorsEditDlg(self, master, "merge")
        response = dlg.ShowModal()
        dlg.Destroy()
        
        # check response
        if response != wx.ID_OK:
            return
        
        # update library
        self._library.update(master)
        self._changed = True
        
        # merge authors
        others = [a for a in authors if a.dbid != master.dbid]
        self._library.merge(master, others)
        
        # update authors
        self.ShowAuthors()
        self.SetSelectedAuthors([master])
    
    
    def _on_delete(self, evt=None):
        """Handles delete event."""
        
        # get selected authors
        authors = self._list.GetSelectedAuthors()
        authors = [a for a in authors if a.count == 0]
        if len(authors) == 0:
            return
        
        # confirm delete
        cancel_butt = mwx.DlgButton(wx.ID_CANCEL, "Cancel", size=(80,-1), default=False, space=15)
        delete_butt = mwx.DlgButton(wx.ID_OK, "Delete", size=(80,-1), default=True, space=0)
        
        dlg = mwx.MessageDlg(self,
            id = -1,
            title = "Delete Authors",
            message = "Do you really want to permanently delete\nselected authors?",
            details = "This operation cannot be undone.",
            buttons = [cancel_butt, delete_butt])
        
        response = dlg.ShowModal()
        dlg.Destroy()
        
        # quit if canceled
        if response != wx.ID_OK:
            return
        
        # delete authors
        for author in authors:
            self._library.delete(author)
        self._changed = True
        
        # update authors
        self.ShowAuthors()
    
    
    def _make_ui(self):
        """Makes panel UI."""
        
        # make items
        self._top_bar = AuthorsTopBar(self)
        self._list = AuthorsList(self)
        self._bottom_bar = AuthorsBottomBar(self)
        
        # bind events
        self.Bind(events.EVT_AUTHORS_QUERY_CHANGED, self._on_query_changed)
        self.Bind(events.EVT_AUTHORS_ITEM_ACTIVATED, self._on_item_activated)
        self.Bind(events.EVT_AUTHORS_ITEM_CONTEXT_MENU, self._on_item_context_menu)
        
        # pack UI
        self.Sizer = wx.BoxSizer(wx.VERTICAL)
        self.Sizer.Add(self._top_bar, 0, wx.EXPAND)
        self.Sizer.Add(self._list, 1, wx.EXPAND)
        self.Sizer.Add(self._bottom_bar, 0, wx.EXPAND)
    
    
    def _show_authors(self, query="", order_by=lambda x:x.lastname, reverse=False):
        """Shows authors according to given query."""
        
        self._authors = []
        
        # set status
        self._bottom_bar.SetLabel("Loading...")
        wx.Yield()
        
        # parse query
        if not isinstance(query, core.Query):
            query = core.Query(query, core.Author.NAME)
        
        # get authors
        if self._library is not None:
            self._authors = self._library.search(query)
            for item in self._authors:
                item.count = self._library.count(item)
        
        # sort authors
        self._authors.sort(key=order_by, reverse=reverse)
        
        # update list
        self._list.SetAuthors(self._authors)
        
        # update bottom bar
        self._update_bottom_bar()
    
    
    def _update_bottom_bar(self):
        """Updates status label in bottom bar."""
        
        # get label
        if not self._authors:
            label = "0 authors found"
        elif len(self._authors) == 1:
            label = "1 author found"
        else:
            label = "%s authors found" % len(self._authors)
        
        # set label
        self._bottom_bar.SetLabel(label)
