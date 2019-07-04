#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

# import modules
import wx

import core
from .. import mwx
from .. import events

from .list_ctrl import LabelsList
from .top_bar import LabelsTopBar


class LabelsView(wx.Dialog):
    """Labels view panel."""
    
    
    def __init__(self, parent, articles, labels):
        """Initializes labels view panel."""
        
        # init panel
        wx.Dialog.__init__(self, parent, -1, size=(300, 350), title="Labels", style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)
        
        # init buffers
        self._articles = articles
        self._labels = labels
        self._search = None
        
        # make UI
        self._make_ui()
        
        # show frame
        self.Layout()
        self.Centre(wx.BOTH)
        self.Show(True)
        
        # set min size
        self.SetMinSize(self.GetSize())
        
        # update list
        self._show_labels()
    
    
    def _on_search(self, evt=None):
        """Handles search event."""
        
        # get current label
        self._search = self._top_bar.GetLabelValue()
        if not self._search:
            self._search = None
        
        # update list
        self._show_labels()
    
    
    def _on_add(self, evt=None):
        """Handles add label event."""
        
        # check current label
        if not self._search:
            return
        
        # get same labels
        same = [x for x in self._labels if x.title == self._search]
        
        # add as new label
        if not same:
            
            # init new label
            label = core.Label()
            label.checked = True
            label.title = self._search
            
            # add label to buffer
            self._labels.append(label)
        
        # mark as checked
        elif self._articles:
            for label in same:
                label.checked = True
        
        # clean search
        self._search = None
        self._top_bar.SetLabelValue(None)
    
    
    def _on_apply(self, evt=None):
        """Handles apply labels event."""
        
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
        self.Bind(events.EVT_LABELS_TYPE, self._on_search)
        self.Bind(events.EVT_LABELS_ADD, self._on_add)
        self.Bind(events.EVT_LABELS_APPLY, self._on_apply)
        
        # pack UI
        self.Sizer = wx.BoxSizer(wx.VERTICAL)
        self.Sizer.Add(self._top_bar, 0, wx.EXPAND)
        self.Sizer.Add(self._list, 1, wx.EXPAND)
    
    
    def _show_labels(self):
        """Shows labels according to current search."""
        
        # get all labels
        labels = self._labels[:]
        
        # apply search filter
        if self._search:
            
            buff = []
            
            for label in labels:
                if all(map(lambda x: x in label.title.lower(), self._search)):
                    buff.append(label)
            
            labels = buff
        
        # show labels
        self._list.SetLabels(labels)
