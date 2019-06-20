#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

# import modules
import wx

import core
from .. import mwx
from .. import events

from .list_ctrl import LabelsList
from .top_bar import LabelsTopBar
from .edit_dlg import LabelsEditDlg


class LabelsView(wx.Dialog):
    """Labels view panel."""
    
    
    def __init__(self, parent, articles, labels):
        """Initializes labels view panel."""
        
        # init panel
        wx.Dialog.__init__(self, parent, -1, size=(213, 350), title="Labels", style=wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER)
        
        # init buffers
        self._articles = articles
        self._labels = labels
        
        # make UI
        self._make_ui()
        
        # show frame
        self.Layout()
        self.Centre(wx.BOTH)
        self.Show(True)
        
        # set min size
        self.SetMinSize(self.GetSize())
        
        # show labels
        self._list.SetLabels(self._labels)
    
    
    def _on_new(self, evt=None):
        """Handles add new label event."""
        
        # init label
        label = core.Label()
        label.checked = True
        
        # get used titles
        used_titles = [x.title for x in self._labels]
        
        # raise dialog
        dlg = LabelsEditDlg(self, label, used_titles=used_titles)
        response = dlg.ShowModal()
        dlg.Destroy()
        
        # check response
        if response != wx.ID_OK:
            return
        
        # add label to buffer
        self._labels.append(label)
        
        # update list
        self._list.SetLabels(self._labels)
    
    
    def _on_apply(self, evt=None):
        """Handles apply event."""
        
        # get checked labels
        labels = [x for x in self._labels if x.checked]
        
        # ensure labels are unique
        buff = []
        unique = set()
        for label in sorted(labels, key=lambda x:x.dbid or -1, reverse=True):
            if label.title not in unique:
                buff.append(label)
                unique.add(label.title)
        
        # set labels to articles
        for article in self._articles:
            article.labels = buff[:]
        
        # end dialog
        self.EndModal(wx.ID_OK)
    
    
    def _make_ui(self):
        """Makes panel UI."""
        
        # make items
        self._top_bar = LabelsTopBar(self)
        self._list = LabelsList(self)
        
        # bind events
        self.Bind(events.EVT_LABELS_NEW, self._on_new)
        self.Bind(events.EVT_LABELS_APPLY, self._on_apply)
        
        # pack UI
        self.Sizer = wx.BoxSizer(wx.VERTICAL)
        self.Sizer.Add(self._top_bar, 0, wx.EXPAND)
        self.Sizer.Add(self._list, 1, wx.EXPAND)
