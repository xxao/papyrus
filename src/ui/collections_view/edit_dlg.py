#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

# import modules
import wx

from .. import mwx


class CollectionsEditDlg(wx.Dialog):
    """Dialog to add/edit collection."""
    
    
    def __init__(self, parent, collection, used_titles=[], is_smart=False):
        """Initializes collection dialog."""
        
        # init dialog
        wx.Dialog.__init__(self, parent, -1, title="Collection", size=(210, 350), style=wx.DEFAULT_DIALOG_STYLE)
        self.Bind(wx.EVT_PAINT, self._on_paint)
        
        # init buffers
        self._collection = collection
        self._used_titles = used_titles
        self._is_smart = is_smart
        
        # make UI
        self._make_ui()
        
        # display dialog
        self.Layout()
        self.Sizer.Fit(self)
        self.Centre()
    
    
    def _on_paint(self, evt):
        """Draws background image."""
        
        if mwx.IS_WIN:
            mwx.panel_top_line(self)
    
    
    def _on_ok(self, evt=None):
        """Handles OK button."""
        
        # get values
        title = self._title_value.GetValue().strip()
        query = self._query_value.GetValue().strip()
        export = self._export_check.GetValue()
        
        # check values
        if not title or (self._is_smart and not query):
            wx.Bell()
            return
        
        # check title uniqueness
        if title in self._used_titles:
            wx.Bell()
            dlg = mwx.MessageDlg(self, -1, "Collection title is not unique!", "A collection with the same title already exists.")
            dlg.ShowModal()
            dlg.Destroy()
            return
        
        # update collection
        self._collection.title = title
        self._collection.query = query
        self._collection.export = export
        
        # close dialog
        self.EndModal(wx.ID_OK)
    
    
    def _on_cancel(self, evt=None):
        """Handles cancel button."""
        
        self.EndModal(wx.ID_CANCEL)
    
    
    def _make_ui(self):
        """Makes dialog UI."""
        
        # make items
        title_label = wx.StaticText(self, -1, "Title:")
        text = self._collection.title if self._collection.title else ""
        self._title_value = wx.TextCtrl(self, -1, text, size=(300,-1), style=wx.TE_PROCESS_ENTER)
        
        self._query_label = wx.StaticText(self, -1, "Query:")
        text = self._collection.query if self._collection.query else ""
        self._query_value = wx.TextCtrl(self, -1, text, size=(300,-1), style=wx.TE_PROCESS_ENTER)
        
        self._export_check = wx.CheckBox(self, -1, "Enable automatic export to text file")
        self._export_check.SetValue(self._collection.export)
        self._export_check.SetToolTipString("Creates a text export with citations when application quits")
        
        cancel_butt = wx.Button(self, wx.ID_CANCEL, "Cancel")
        ok_butt = wx.Button(self, wx.ID_OK, "OK")
        
        # disable query for manual collections
        if not self._is_smart:
            self._query_value.ChangeValue("")
            self._query_value.Disable()
            self._query_label.Disable()
        
        # bind events
        self._title_value.Bind(wx.EVT_TEXT_ENTER, self._on_ok)
        self._query_value.Bind(wx.EVT_TEXT_ENTER, self._on_ok)
        cancel_butt.Bind(wx.EVT_BUTTON, self._on_cancel)
        ok_butt.Bind(wx.EVT_BUTTON, self._on_ok)
        
        # pack items
        grid = wx.GridBagSizer(mwx.GRIDBAG_VSPACE, mwx.GRIDBAG_HSPACE)
        grid.Add(title_label, (0,0), flag=wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)
        grid.Add(self._title_value, (0,1), (1,2), flag=wx.ALIGN_CENTER_VERTICAL|wx.EXPAND)
        grid.Add(self._query_label, (1,0), flag=wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)
        grid.Add(self._query_value, (1,1), (1,2), flag=wx.ALIGN_CENTER_VERTICAL|wx.EXPAND)
        grid.Add(self._export_check, (2,1), flag=wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL)
        grid.AddGrowableCol(1)
        
        buttons = wx.BoxSizer(wx.HORIZONTAL)
        buttons.Add(cancel_butt, 0, wx.RIGHT, mwx.PANEL_SPACE_MAIN)
        buttons.Add(ok_butt, 0)
        
        self.Sizer = wx.BoxSizer(wx.VERTICAL)
        self.Sizer.Add(grid, 0, wx.ALL|wx.EXPAND, mwx.PANEL_SPACE_MAIN)
        self.Sizer.Add(buttons, 0, wx.LEFT|wx.RIGHT|wx.BOTTOM|wx.ALIGN_RIGHT, mwx.PANEL_SPACE_MAIN)
