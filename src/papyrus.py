#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

# import modules
import sys
import wx

from ui import config


class Papyrus(wx.App):
    """Run Papyrus, run..."""
    
    
    def OnInit(self):
        """Initializes application."""

        # fixes some wxPython issues
        self.SetAssertMode(wx.APP_ASSERT_SUPPRESS)

        # init config
        import ui.config
        if not ui.config.load():
            ui.config.save()
        
        # initialize mwx
        import ui.mwx
        ui.mwx.initialize()
        
        # init main frame
        import ui.main_frame
        self._frame = ui.main_frame.MainFrame(None, -1)
        
        # show frame
        self.SetTopWindow(self._frame)
        #wx.Yield()
        
        # open file from command line
        if len(sys.argv) >= 2:
            wx.CallAfter(self._frame.OpenDocuments, paths=sys.argv[1:])
        
        # open file from config
        else:
            wx.CallAfter(self._frame.OpenDocuments, paths=[ui.config.SETTINGS['library']])
        
        return True
    
    
    def MacOpenFile(self, path):
        """"Enable drag/drop on icon under Mac."""
        
        if path != 'papyrus.py':
            wx.CallAfter(self._frame.OpenDocuments, paths=[path])
    
    
    def MacReopenApp(self):
        """Called when the doc icon is clicked."""
        
        try: self.GetTopWindow().Raise()
        except: pass


# start application
if __name__ == '__main__':
    app = Papyrus(0)
    app.MainLoop()
