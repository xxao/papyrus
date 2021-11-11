#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

# import modules
import wx

from .. import mwx


class AuthorsEditDlg(wx.Dialog):
    """Dialog to add/edit author."""
    
    
    def __init__(self, parent, author, mode):
        """Initializes author dialog."""
        
        # init dialog
        wx.Dialog.__init__(self, parent, -1, title="Author", size=(300, -1), style=wx.DEFAULT_DIALOG_STYLE)
        self.Bind(wx.EVT_PAINT, self._on_paint)
        
        # init buffers
        self._author = author
        self._mode = mode
        
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
        """Handles ok button."""
        
        # get values
        lastname = self._lastname_value.GetValue().strip()
        firstname = self._firstname_value.GetValue().strip()
        initials = self._initials_value.GetValue().strip()
        
        # check values
        if not lastname:
            wx.Bell()
            return
        
        # update author
        self._author.lastname = lastname
        self._author.firstname = firstname
        self._author.initials = initials
        
        # close dialog
        self.EndModal(wx.ID_OK)
    
    
    def _on_cancel(self, evt=None):
        """Handles cancel button."""
        
        self.EndModal(wx.ID_CANCEL)
    
    
    def _make_ui(self):
        """Makes dialog UI."""
        
        # make items
        lastname_label = wx.StaticText(self, -1, "Last Name:")
        text = self._author.lastname if self._author.lastname else ""
        self._lastname_value = wx.TextCtrl(self, -1, text, size=(200, -1), style=wx.TE_PROCESS_ENTER)
        
        firstname_label = wx.StaticText(self, -1, "First Name:")
        text = self._author.firstname if self._author.firstname else ""
        self._firstname_value = wx.TextCtrl(self, -1, text, size=(200, -1), style=wx.TE_PROCESS_ENTER)
        
        initials_label = wx.StaticText(self, -1, "Initials:")
        text = self._author.initials if self._author.initials else ""
        self._initials_value = wx.TextCtrl(self, -1, text, size=(200, -1), style=wx.TE_PROCESS_ENTER)
        
        cancel_butt = wx.Button(self, wx.ID_CANCEL, "Cancel")
        ok_butt = wx.Button(self, wx.ID_OK, "Merge" if self._mode == "merge" else "Update")
        
        # bind events
        self._lastname_value.Bind(wx.EVT_TEXT_ENTER, self._on_ok)
        self._firstname_value.Bind(wx.EVT_TEXT_ENTER, self._on_ok)
        self._initials_value.Bind(wx.EVT_TEXT_ENTER, self._on_ok)
        
        cancel_butt.Bind(wx.EVT_BUTTON, self._on_cancel)
        ok_butt.Bind(wx.EVT_BUTTON, self._on_ok)
        
        # pack items
        grid = wx.GridBagSizer(mwx.GRIDBAG_VSPACE, mwx.GRIDBAG_HSPACE)
        grid.Add(lastname_label, (0,0), flag=wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        grid.Add(self._lastname_value, (0,1), (1,2), flag=wx.ALIGN_CENTER_VERTICAL | wx.EXPAND)
        grid.Add(firstname_label, (1,0), flag=wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        grid.Add(self._firstname_value, (1,1), (1,2), flag=wx.ALIGN_CENTER_VERTICAL | wx.EXPAND)
        grid.Add(initials_label, (2,0), flag=wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        grid.Add(self._initials_value, (2,1), (1,2), flag=wx.ALIGN_CENTER_VERTICAL | wx.EXPAND)
        grid.AddGrowableCol(1)
        
        buttons = wx.BoxSizer(wx.HORIZONTAL)
        buttons.Add(cancel_butt, 0, wx.RIGHT, mwx.PANEL_SPACE_MAIN)
        buttons.Add(ok_butt, 0)
        
        self.Sizer = wx.BoxSizer(wx.VERTICAL)
        self.Sizer.Add(grid, 1, wx.ALL | wx.EXPAND, mwx.PANEL_SPACE_MAIN)
        self.Sizer.Add(buttons, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.ALIGN_RIGHT, mwx.PANEL_SPACE_MAIN)
