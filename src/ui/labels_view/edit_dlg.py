#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

# import modules
import wx

from .. import mwx


class LabelsEditDlg(wx.Dialog):
    """Dialog to add/edit label."""
    
    
    def __init__(self, parent, label, used_titles=[]):
        """Initializes label dialog."""
        
        # init dialog
        wx.Dialog.__init__(self, parent, -1, title="Label", size=(210, 350), style=wx.DEFAULT_DIALOG_STYLE)
        self.Bind(wx.EVT_PAINT, self._on_paint)
        
        # init buffers
        self._label = label
        self._used_titles = used_titles
        
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
        title = self._title_value.GetValue().strip()
        
        # check values
        if not title:
            wx.Bell()
            return
        
        # check title uniqueness
        if title in self._used_titles:
            wx.Bell()
            dlg = mwx.MessageDlg(self, -1, "Label title is not unique!", "A label with the same title already exists.")
            dlg.ShowModal()
            dlg.Destroy()
            return
        
        # update label
        self._label.title = title
        
        # close dialog
        self.EndModal(wx.ID_OK)
    
    
    def _on_cancel(self, evt=None):
        """Handles cancel button."""
        
        self.EndModal(wx.ID_CANCEL)
    
    
    def _make_ui(self):
        """Makes dialog UI."""
        
        # make items
        title_label = wx.StaticText(self, -1, "Title:")
        text = self._label.title if self._label.title else ""
        self._title_value = wx.TextCtrl(self, -1, text, style=wx.TE_PROCESS_ENTER)
        
        cancel_butt = wx.Button(self, wx.ID_CANCEL, "Cancel")
        ok_butt = wx.Button(self, wx.ID_OK, "OK")
        
        # bind events
        self._title_value.Bind(wx.EVT_TEXT_ENTER, self._on_ok)
        cancel_butt.Bind(wx.EVT_BUTTON, self._on_cancel)
        ok_butt.Bind(wx.EVT_BUTTON, self._on_ok)
        
        # pack items
        grid = wx.GridBagSizer(mwx.GRIDBAG_VSPACE, mwx.GRIDBAG_HSPACE)
        grid.Add(title_label, (0,0), flag=wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        grid.Add(self._title_value, (0,1), (1,2), flag=wx.ALIGN_CENTER_VERTICAL | wx.EXPAND)
        grid.AddGrowableCol(1)
        
        buttons = wx.BoxSizer(wx.HORIZONTAL)
        buttons.Add(cancel_butt, 0, wx.RIGHT, mwx.PANEL_SPACE_MAIN)
        buttons.Add(ok_butt, 0)
        
        self.Sizer = wx.BoxSizer(wx.VERTICAL)
        self.Sizer.Add(grid, 0, wx.ALL | wx.EXPAND, mwx.PANEL_SPACE_MAIN)
        self.Sizer.Add(buttons, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM, mwx.PANEL_SPACE_MAIN)
