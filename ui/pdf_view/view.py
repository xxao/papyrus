#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

# import modules
import io
import os.path
import wx
from wx.lib.pdfviewer import pdfViewer

from .. import mwx


class PDFView(wx.Panel):
    """PDF view panel."""
    
    
    def __init__(self, parent):
        """Initializes details view panel."""
        
        # init panel
        wx.Panel.__init__(self, parent, -1, style=wx.NO_FULL_REPAINT_ON_RESIZE)
        self.SetOwnBackgroundColour(mwx.PDF_VIEW_BGR)
        self.Bind(wx.EVT_SIZE, self._on_size)
        
        # init buffers
        self._article = None
        self._pdf_data = None
        
        # make UI
        self._make_ui()
        
        # show default page
        self._show_pdf()
    
    
    def SetArticle(self, article):
        """Sets article to display."""
        
        # check for same article
        if self._article is article:
            return
        
        # set article
        self._article = article
        
        # load PDF data
        self._load_pdf()
        
        # show PDF
        self._show_pdf()
    
    
    def _on_size(self, evt):
        
        # skip event to allow viewer to get it
        evt.Skip()
        
        # show article
        self._show_pdf()
    
    
    def _make_ui(self):
        """Makes panel UI."""
        
        # make empty label
        label = wx.StaticText(self, -1, "Article PDF", style=wx.ALIGN_CENTER)
        font = wx.Font(14, wx.DEFAULT, wx.NORMAL, wx.BOLD)
        label.SetFont(font)
        label.SetForegroundColour((190,190,190))
        
        # make viewer
        self._viewer = pdfViewer(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, style=wx.NO_BORDER|wx.ALIGN_CENTER)
        
        # pack UI
        self.Sizer = wx.BoxSizer(wx.VERTICAL)
        self.Sizer.Add(label, 0, wx.EXPAND|wx.TOP, 80)
        self.Sizer.Add(self._viewer, 1, wx.EXPAND)
    
    
    def _load_pdf(self):
        """Loads PDF data from file."""
        
        # reset current data
        self._pdf_data = None
        
        # check article
        if self._article is None or not self._article.pdf:
            return
        
        # get path
        path = self._article.pdf_path
        
        # check file
        if not os.path.exists(path):
            return
        
        # load data
        with open(path, 'rb') as pdf:
            self._pdf_data = io.BytesIO(pdf.read())
    
    
    def _show_pdf(self):
        """Shows current article PDF."""
        
        # show blank site if no PDF data
        if self._pdf_data is None:
            self.Sizer.Show(0)
            self.Sizer.Hide(1)
            self.Sizer.Layout()
            return
        
        # block if panel not visible or too small
        # this is to block a bug in the PDF viewer
        if self.GetClientSize()[1] < 100:
            self.Sizer.Show(0)
            self.Sizer.Hide(1)
            self.Sizer.Layout()
            return
        
        # show viewer
        self.Sizer.Hide(0)
        self.Sizer.Show(1)
        self.Sizer.Layout()
        
        # show PDF
        self._viewer.LoadFile(self._pdf_data)
