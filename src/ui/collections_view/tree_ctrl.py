#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

# import modules
import wx
import wx.dataview as wxdv

import core
from .. import mwx
from .. import events
from .. import images


class CollectionsTree(wx.Panel):
    """Collections tree panel."""
    
    
    def __init__(self, parent):
        """Initializes articles list panel."""
        
        # init panel
        wx.Panel.__init__(self, parent, -1, style=wx.NO_FULL_REPAINT_ON_RESIZE)
        
        # init buffers
        self._library_collections = []
        self._manual_collections = []
        self._smart_collections = []
        self._labels_collections = []
        
        self._items_data = {}
        
        # make ui
        self._make_ui()
    
    
    def GetSelectedCollection(self):
        """Gets selected collection."""
        
        item = self._tree_ctrl.GetSelection()
        return self._items_data.get(item, None)
    
    
    def SetLibraryCollections(self, collections):
        """Sets library collections to display."""
        
        # set new data
        self._library_collections = collections or []
        
        # update tree
        self._set_collections(collections, self._library_root, images.ICON_COLLECTION_LIBRARY)
    
    
    def SetManualCollections(self, collections):
        """Sets manual collections to display."""
        
        # set new data
        self._manual_collections = collections or []
        
        # update tree
        self._set_collections(collections, self._manual_root, images.ICON_COLLECTION_MANUAL)
    
    
    def SetSmartCollections(self, collections):
        """Sets smart collections to display."""
        
        # get collections
        collections = [x for x in collections if x.query]
        
        # set new data
        self._smart_collections = collections or []
        
        # update tree
        self._set_collections(collections, self._smart_root, images.ICON_COLLECTION_SMART)
    
    
    def SetLabelsCollections(self, collections):
        """Sets labels collections to display."""
        
        # set new data
        self._labels_collections = collections or []
        
        # update tree
        self._set_collections(collections, self._labels_root, images.ICON_COLLECTION_LABEL)
    
    
    def UpdateItemsText(self):
        """Updates text label of each collection."""
        
        # update library collections
        for i in range(self._tree_ctrl.GetChildCount(self._library_root)):
            item = self._tree_ctrl.GetNthChild(self._library_root, i)
            data = self._items_data[item]
            self._tree_ctrl.SetItemText(item, "%s (%d)" % (data.title, data.count))
        
        # update manual collections
        for i in range(self._tree_ctrl.GetChildCount(self._manual_root)):
            item = self._tree_ctrl.GetNthChild(self._manual_root, i)
            data = self._items_data[item]
            self._tree_ctrl.SetItemText(item, "%s (%d)" % (data.title, data.count))
        
        # update smart collections
        for i in range(self._tree_ctrl.GetChildCount(self._smart_root)):
            item = self._tree_ctrl.GetNthChild(self._smart_root, i)
            data = self._items_data[item]
            self._tree_ctrl.SetItemText(item, "%s (%d)" % (data.title, data.count))
        
        # update labels collections
        for i in range(self._tree_ctrl.GetChildCount(self._labels_root)):
            item = self._tree_ctrl.GetNthChild(self._labels_root, i)
            data = self._items_data[item]
            self._tree_ctrl.SetItemText(item, "%s (%d)" % (data.title, data.count))
    
    
    def IsDropPossible(self, x, y):
        """Checks if drop is possible for item at position."""
        
        # get collection
        item, column = self._tree_ctrl.HitTest((x,y))
        collection = self._items_data.get(item, None)
        
        # check collection
        if collection is None:
            return False
        
        # allow drop for trash
        if collection.group == "system" and collection.title == "Trash":
            return True
        
        # allow drop for manual collections
        if collection.group == "custom" and not collection.query:
            return True
        
        # allow drop for labels
        if collection.group == "labels":
            return True
        
        # disallow drop
        return False
    
    
    def DropArticles(self, x, y, ids):
        """Drops articles to item at position."""
        
        # get collection
        item, column = self._tree_ctrl.HitTest((x,y))
        collection = self._items_data.get(item, None)
        
        # check IDs and collection
        if not ids or collection is None:
            return
        
        # drop to trash
        if collection.group == "system" and collection.title == "Trash":
            event = events.ArticlesDroppedToTrashEvent(self.GetId(), articles_dbids=ids)
        
        # drop to manual collections
        elif collection.group == "custom" and not collection.query:
            event = events.ArticlesDroppedToCollectionEvent(self.GetId(), articles_dbids=ids, collection_dbid=collection.dbid)
        
        # drop to label
        elif collection.group == "labels":
            event = events.ArticlesDroppedToLabelEvent(self.GetId(), articles_dbids=ids, label_title=collection.title)
        
        # not allowed
        else:
            return
        
        # raise event
        wx.PostEvent(self, event)
    
    
    def _on_selection_changed(self, evt):
        """Handles item selection event."""
        
        event = events.CollectionsSelectionChangedEvent(self.GetId())
        wx.PostEvent(self, event)
    
    
    def _on_item_activated(self, evt):
        """Handles row activation event."""
        
        event = events.CollectionsItemActivatedEvent(self.GetId())
        wx.PostEvent(self, event)
    
    
    def _on_item_context_menu(self, evt):
        """Handles context menu event."""
        
        event = events.CollectionsItemContextMenuEvent(self.GetId())
        wx.PostEvent(self, event)
    
    
    def _on_item_start_editing(self, evt):
        """Handles item start editing event."""
        
        evt.Veto()
    
    
    def _set_collections(self, collections, root, icon):
        """Sets new collections."""
        
        # get expanded status
        expanded = self._tree_ctrl.IsExpanded(root)
        
        # remove mapping
        for i in range(self._tree_ctrl.GetChildCount(root)):
            item = self._tree_ctrl.GetNthChild(root, i)
            del self._items_data[item]
        
        # remove from tree
        self._tree_ctrl.DeleteChildren(root)
        
        # add new items
        for collection in collections:
            item = self._tree_ctrl.AppendItem(root, "%s (%d)" % (collection.title, collection.count))
            self._tree_ctrl.SetItemIcon(item, icon)
            self._items_data[item] = collection
        
        # expand items
        if expanded:
            self._tree_ctrl.Expand(root)
    
    
    def _make_ui(self):
        """Makes panel UI."""
        
        # init tree control
        self._tree_ctrl = wxdv.DataViewTreeCtrl(self, style=wxdv.DV_SINGLE | wxdv.DV_NO_HEADER | wxdv.DV_VARIABLE_LINE_HEIGHT | wx.NO_BORDER)
        self._tree_ctrl.SetOwnBackgroundColour(mwx.COLLECTIONS_VIEW_BGR)
        
        # enable drop target
        target = mwx.ArticlesIDsDropTarget(self)
        self._tree_ctrl.SetDropTarget(target)
        
        # add roots
        self._library_root = self._tree_ctrl.AppendContainer(wxdv.NullDataViewItem, "LIBRARY")
        self._manual_root = self._tree_ctrl.AppendContainer(wxdv.NullDataViewItem, "COLLECTIONS")
        self._smart_root = self._tree_ctrl.AppendContainer(wxdv.NullDataViewItem, "SMART COLLECTIONS")
        self._labels_root = self._tree_ctrl.AppendContainer(wxdv.NullDataViewItem, "LABELS")
        
        # set icons
        self._tree_ctrl.SetItemIcon(self._library_root, images.ICON_COLLECTION_LIBRARY)
        self._tree_ctrl.SetItemIcon(self._manual_root, images.ICON_COLLECTION_MANUAL)
        self._tree_ctrl.SetItemIcon(self._smart_root, images.ICON_COLLECTION_SMART)
        self._tree_ctrl.SetItemIcon(self._labels_root, images.ICON_COLLECTION_LABEL)
        
        # expand roots
        self._tree_ctrl.Expand(self._library_root)
        self._tree_ctrl.Expand(self._manual_root)
        self._tree_ctrl.Expand(self._smart_root)
        self._tree_ctrl.Expand(self._labels_root)
        
        # bind events
        self._tree_ctrl.Bind(wxdv.EVT_DATAVIEW_SELECTION_CHANGED, self._on_selection_changed)
        self._tree_ctrl.Bind(wxdv.EVT_DATAVIEW_ITEM_ACTIVATED, self._on_item_activated)
        self._tree_ctrl.Bind(wxdv.EVT_DATAVIEW_ITEM_CONTEXT_MENU, self._on_item_context_menu)
        self._tree_ctrl.Bind(wxdv.EVT_DATAVIEW_ITEM_START_EDITING, self._on_item_start_editing)
        
        # add to sizer
        self.Sizer = wx.BoxSizer(wx.VERTICAL)
        self.Sizer.Add(self._tree_ctrl, 1, wx.EXPAND)
