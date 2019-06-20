#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

# import modules
import sys
import platform
import wx

from . import config
from . import mwx


class ErrorDlg(wx.Dialog):
    """Dialog to show exception report."""
    
    
    def __init__(self, parent, exception_text):
        """Initializes error dialog."""
        
        # init dialog
        wx.Dialog.__init__(self, parent, -1, title="Application error", size=(210, 350), style=wx.DEFAULT_DIALOG_STYLE|wx.STAY_ON_TOP)
        self.Bind(wx.EVT_PAINT, self._on_paint)
        
        # makes error message
        self._finalize_error(exception_text)
        
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
    
    
    def _on_quit(self, evt=None):
        """Handles quit button."""
        
        sys.exit()
    
    
    def _on_continue(self, evt=None):
        """Handles continue button."""
        
        self.EndModal(wx.ID_CANCEL)
    
    
    def _finalize_error(self, exception_text):
        """Finalizes the error message."""
        
        # get system information
        self._exception_text = ''
        self._exception_text += exception_text
        self._exception_text += '\n-------------------------'
        self._exception_text += '\nPapyrus: %s' % (config.VERSION,)
        self._exception_text += '\nPython: %s' % str(platform.python_version_tuple())
        self._exception_text += '\nwxPython: %s' % str(wx.version())
        self._exception_text += '\n-------------------------'
        self._exception_text += '\nArchitecture: %s' % str(platform.architecture())
        self._exception_text += '\nMachine: %s' % str(platform.machine())
        self._exception_text += '\nPlatform: %s' % str(platform.platform())
        self._exception_text += '\nProcessor: %s' % str(platform.processor())
        self._exception_text += '\nSystem: %s' % str(platform.system())
        self._exception_text += '\nMac: %s' % str(platform.mac_ver())
        self._exception_text += '\nMSW: %s' % str(platform.win32_ver())
        self._exception_text += '\nLinux: %s' % str(platform.dist())
        self._exception_text += '\n-------------------------\n'
        self._exception_text += 'Add your comments:\n'
    
    
    def _make_ui(self):
        """Makes dialog UI."""
        
        # make items
        self._exception_value = wx.TextCtrl(self, -1, self._exception_text, size=(400,250), style=wx.TE_MULTILINE)
        self._exception_value.SetFont(wx.SMALL_FONT)
        
        message_label = wx.StaticText(self, -1, "Uups, another one...\nUnfortunately, you have probably found another bug in Papyrus.\nPlease send me this error report to papyrus@bymartin.cz and I will try to fix it.\nI apologize for any inconvenience due to this bug.\nI strongly recommend to restart Papyrus now.")
        message_label.SetFont(wx.SMALL_FONT)
        
        quit_butt = wx.Button(self, -1, "Quit")
        continue_butt = wx.Button(self, -1, "Try to Continue")
        
        # bind events
        quit_butt.Bind(wx.EVT_BUTTON, self._on_quit)
        continue_butt.Bind(wx.EVT_BUTTON, self._on_continue)
        
        # pack items
        buttons = wx.BoxSizer(wx.HORIZONTAL)
        buttons.Add(quit_butt, 0, wx.RIGHT, mwx.PANEL_SPACE_MAIN)
        buttons.Add(continue_butt, 0)
        
        self.Sizer = wx.BoxSizer(wx.VERTICAL)
        self.Sizer.Add(self._exception_value, 1, wx.ALL|wx.EXPAND, mwx.PANEL_SPACE_MAIN)
        self.Sizer.Add(message_label, 0, wx.LEFT|wx.RIGHT|wx.BOTTOM, mwx.PANEL_SPACE_MAIN)
        self.Sizer.Add(buttons, 0, wx.LEFT|wx.RIGHT|wx.BOTTOM|wx.ALIGN_RIGHT, mwx.PANEL_SPACE_MAIN)
