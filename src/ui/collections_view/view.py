#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

# import modules
import wx

import core
from .. import config
from .. import mwx
from .. import images
from .. import events
from .. ids import *
from .tree_ctrl import CollectionsTree


class CollectionsView(wx.Panel):
    """Collections view panel."""
    
    
    def __init__(self, parent):
        """Initializes collections view panel."""
        
        # init panel
        wx.Panel.__init__(self, parent, -1, style=wx.NO_FULL_REPAINT_ON_RESIZE)
        self.Bind(wx.EVT_PAINT, self._on_paint)
        
        # init buffers
        self._library = None
        
        self._library_collections = []
        self._manual_collections = []
        self._smart_collections = []
        self._labels_collections = []
        
        # init library collections
        self._library_collections.append(core.Collection(title="Articles", query="0[TRASH]", group="system"))
        self._library_collections.append(core.Collection(title="Recent", query="%d[RECENT]" % config.SETTINGS['recent_days'], group="system"))
        self._library_collections.append(core.Collection(title="Trash", query="1[TRASH]", group="system"))
        
        # make UI
        self._make_ui()
    
    
    def GetSelectedCollection(self):
        """Gets selected collection."""
        
        return self._tree.GetSelectedCollection()
    
    
    def SetLibrary(self, library):
        """Sets library database."""
        
        # set library
        self._library = library
        
        # update tree
        self.UpdateLibraryCollections()
        self.UpdateManualCollections()
        self.UpdateSmartCollections()
        self.UpdateLabelsCollections()
        
        # OSX hack
        self.Layout()
    
    
    def UpdateLibraryCollections(self):
        """Updates list of system collections."""
        
        # update articles count
        if self._library is not None:
            for collection in self._library_collections:
                collection.count = self._library.count(collection)
        else:
            for collection in self._library_collections:
                collection.count = 0
        
        # update tree
        self._tree.SetLibraryCollections(self._library_collections)
        
        # OSX hack
        self.Layout()
    
    
    def UpdateManualCollections(self):
        """Updates list of manual collections."""
        
        # clear previous
        self._manual_collections = []
        
        # get available collections
        if self._library is not None:
            
            # get collections
            query = core.Query("", core.Collection.NAME)
            collections = sorted(self._library.search(query), key=lambda x:x.title)
            self._manual_collections = [x for x in collections if not x.query]
            
            # update articles count
            for collection in self._manual_collections:
                collection.count = self._library.count(collection)
        
        # update tree
        self._tree.SetManualCollections(self._manual_collections)
        
        # OSX hack
        self.Layout()
    
    
    def UpdateSmartCollections(self):
        """Updates list of smart collections."""
        
        # clear previous
        self._smart_collections = []
        
        # get available collections
        if self._library is not None:
            
            # get collections
            query = core.Query("", core.Collection.NAME)
            collections = sorted(self._library.search(query), key=lambda x:x.title)
            self._smart_collections = [x for x in collections if x.query]
            
            # update articles count
            for collection in self._smart_collections:
                collection.count = self._library.count(collection)
        
        # update tree
        self._tree.SetSmartCollections(self._smart_collections)
        
        # OSX hack
        self.Layout()
    
    
    def UpdateLabelsCollections(self):
        """Updates list of available labels."""
        
        # clear previous
        self._labels_collections = []
        
        # get available labels
        if self._library is not None:
            
            # get labels
            query = core.Query("", core.Label.NAME)
            labels = sorted(self._library.search(query), key=lambda x:x.title)
            
            # convert labels into smart collections
            for label in labels:
                self._labels_collections.append(
                    core.Collection(
                        title = label.title,
                        query = "%s[LABELID]" % label.dbid,
                        group = "labels",
                        attachment = label))
            
            # update articles count
            for collection in self._labels_collections:
                collection.count = self._library.count(collection)
        
        # update tree
        self._tree.SetLabelsCollections(self._labels_collections)
        
        # OSX hack
        self.Layout()
    
    
    def UpdateCounts(self):
        """Updates labels for each collection."""
        
        # update counts for library collections
        for collection in self._library_collections:
            collection.count = self._library.count(collection)
        
        # update counts for manual collections
        for collection in self._manual_collections:
            collection.count = self._library.count(collection)
        
        # update counts for smart collections
        for collection in self._smart_collections:
            collection.count = self._library.count(collection)
        
        # update counts for labels collections
        for collection in self._labels_collections:
            collection.count = self._library.count(collection.attachment)
        
        # update tree
        self._tree.UpdateItemsText()
    
    
    def _on_paint(self, evt):
        """Draws background image."""
        
        if mwx.IS_WIN:
            mwx.panel_top_line(self, mwx.DARK_DIVIDER_COLOUR)
    
    
    def _on_item_context_menu(self, evt):
        """Handles collection item context menu event."""
        
        # check library
        if self._library is None:
            
            menu = wx.Menu()
            menu.Append(ID_LIBRARY_NEW, "New Library...")
            menu.Append(ID_LIBRARY_OPEN, "Open Library...")
            
            self.PopupMenu(menu)
            menu.Destroy()
            return
        
        # get selected collection
        collection = self._tree.GetSelectedCollection()
        
        # make menu
        menu = wx.Menu()
        
        # no specific collection
        if collection is None:
            menu.Append(ID_COLLECTIONS_NEW_MANUAL, "New Collection...")
            menu.Append(ID_COLLECTIONS_NEW_SMART, "New Smart Collection...")
            menu.Append(ID_LABELS_NEW, "New Label...")
            menu.AppendSeparator()
            menu.Append(ID_LIBRARY_NEW, "New Library...")
            menu.Append(ID_LIBRARY_OPEN, "Open Library...")
            menu.AppendSeparator()
            menu.Append(ID_LIBRARY_ANALYZE, "Analyze Library")
        
        # add items for trash
        elif collection.group == "system" and collection.title == "Trash":
            menu.Append(ID_COLLECTIONS_EMPTY_TRASH, "Empty Trash")
        
        # add items for articles
        elif collection.group == "system" and collection.title == "Articles":
            menu.Append(ID_ARTICLES_NEW, "New Article...")
            menu.Append(ID_ARTICLES_IMPORT, "Import PDF...")
        
        # add items for custom collections
        elif collection.group == "custom" and not collection.query:
            menu.Append(ID_COLLECTIONS_NEW_MANUAL, "New Collection...")
            menu.Append(ID_COLLECTIONS_EDIT, "Edit Collection...")
            menu.AppendSeparator()
            menu.Append(ID_COLLECTIONS_DELETE, "Delete Collection")
        
        # add items for custom collections
        elif collection.group == "custom" and collection.query:
            menu.Append(ID_COLLECTIONS_NEW_SMART, "New Smart Collection...")
            menu.Append(ID_COLLECTIONS_EDIT, "Edit Smart Collection...")
            menu.AppendSeparator()
            menu.Append(ID_COLLECTIONS_DELETE, "Delete Smart Collection")
        
        # add items for labels collections
        elif collection.group == "labels":
            menu.Append(ID_LABELS_NEW, "New Label...")
            menu.Append(ID_LABELS_EDIT, "Edit Label...")
            menu.AppendSeparator()
            menu.Append(ID_LABELS_DELETE, "Delete Label")
        
        # show menu
        self.PopupMenu(menu)
        menu.Destroy()
    
    
    def _make_ui(self):
        """Makes panel UI."""
        
        # make items
        self._tree = CollectionsTree(self)
        
        # bind events
        self.Bind(events.EVT_COLLECTIONS_ITEM_CONTEXT_MENU, self._on_item_context_menu)
        
        # pack UI
        self.Sizer = wx.BoxSizer(wx.VERTICAL)
        self.Sizer.Add(self._tree, 1, wx.EXPAND)
        
        # add top line
        if mwx.IS_WIN:
            self.Sizer.InsertSpacer(0, 1)
