#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

# import modules
import wx

import core
from .. import mwx
from .. import images
from .. import events
from .. ids import *
from .. hotkeys import *

from .list_ctrl import ArticlesList
from .top_bar import ArticlesTopBar


class ArticlesView(wx.Panel):
    """Articles view panel."""
    
    
    def __init__(self, parent):
        """Initializes articles view panel."""
        
        # init panel
        wx.Panel.__init__(self, parent, -1, style=wx.NO_FULL_REPAINT_ON_RESIZE)
        
        self._library = None
        self._master_query = ""
        self._articles = []
        self._collection_ids = {}
        
        # make UI
        self._make_ui()
    
    
    def GetArticles(self):
        """Gets list of all displayed articles."""
        
        return self._articles
    
    
    def GetSelectedArticles(self):
        """Gets list of selected articles."""
        
        return self._list.GetSelectedArticles()
    
    
    def GetColumnsSettings(self):
        """Gets current column order and settings."""
        
        return self._list.GetColumnsSettings()
    
    
    def SetLibrary(self, library):
        """Sets library database."""
        
        # set library
        self._library = library
        
        # display all articles
        self.ShowAllArticles()
    
    
    def SetQuery(self, value):
        """Sets query to top bar."""
        
        self._top_bar.ChangeQuery(value)
    
    
    def SetMasterQuery(self, value):
        """Sets master query to be added to all queries."""
        
        self._master_query = str(value) if value else ""
    
    
    def SetSelectedArticles(self, articles):
        """Selects specified articles."""
        
        self._list.SetSelectedArticles(articles)
    
    
    def SetFocusToQuery(self):
        """Sets focus on search query field."""
        
        self._top_bar.SetFocusToQuery()
    
    
    def ShowAllArticles(self):
        """Clears query and shows all articles in library."""
        
        # clear query
        self._top_bar.ChangeQuery(None)
        
        # display all articles
        self._show_articles()
    
    
    def ShowArticles(self):
        """Shows articles according to current query."""
        
        # get current query
        query = self._top_bar.GetQuery()
        
        # shows articles
        self._show_articles(query)
    
    
    def _on_query_changed(self, evt):
        """Handles query changed event."""
        
        self.ShowArticles()
    
    
    def _on_item_context_menu(self, evt):
        """Handles article item context menu event."""
        
        # check library
        if self._library is None:
            
            menu = wx.Menu()
            menu.Append(ID_LIBRARY_NEW, "New Library...\t"+HK_LIBRARY_NEW)
            menu.Append(ID_LIBRARY_OPEN, "Open Library...\t"+HK_LIBRARY_OPEN)
            
            self.PopupMenu(menu)
            menu.Destroy()
            return
        
        # get selected articles
        articles = self._list.GetSelectedArticles()
        
        # get trash status
        is_trash = self._master_query == "1[TRASH]"
        if is_trash and not articles:
            return
        
        # init menu
        menu = wx.Menu()
        
        menu.Append(ID_ARTICLES_OPEN_PDF, "Open PDF\t"+HK_ARTICLES_OPEN_PDF)
        menu.Append(ID_ARTICLES_OPEN_DOI, "Open Website\t"+HK_ARTICLES_OPEN_DOI)
        menu.Append(ID_ARTICLES_OPEN_PMID, "Open in PubMed\t"+HK_ARTICLES_OPEN_PMID)
        menu.Append(ID_ARTICLES_REVEAL_PDF, "Reveal PDF File\t"+HK_ARTICLES_REVEAL_PDF)
        
        menu.AppendSeparator()
        menu.Append(ID_ARTICLES_COPY_CITATION, "Copy Citation\t"+HK_ARTICLES_COPY_CITATION)
        menu.Append(ID_ARTICLES_COPY_SUMMARY, "Copy Summary\t"+HK_ARTICLES_COPY_SUMMARY)
        menu.Append(ID_ARTICLES_COPY_LINK, "Copy Link\t"+HK_ARTICLES_COPY_LINK)
        
        # trashed articles
        if is_trash:
            menu.AppendSeparator()
            menu.Append(ID_ARTICLES_RESTORE, "Restore\t"+HK_ARTICLES_RESTORE)
            
            menu.AppendSeparator()
            menu.Append(ID_ARTICLES_DELETE, "Delete Permanently")
            menu.Append(ID_COLLECTIONS_EMPTY_TRASH, "Empty Trash")
        
        # standard article views
        else:
            menu.AppendSeparator()
            menu.Append(ID_ARTICLES_RATING, "Rating", self._make_rating_menu(articles))
            menu.Append(ID_ARTICLES_COLOUR, "Color", self._make_colour_menu(articles))
            menu.Append(ID_ARTICLES_LABELS, "Labels...\t"+HK_ARTICLES_LABELS)
            
            menu.AppendSeparator()
            menu.Append(ID_ARTICLES_COLLECTIONS, "Collections", self._make_collections_menu(articles))
            
            menu.AppendSeparator()
            menu.Append(ID_ARTICLES_EDIT, "Edit...\t"+HK_ARTICLES_EDIT)
            menu.Append(ID_ARTICLES_ATTACH_PDF, "Attach PDF...\t"+HK_ARTICLES_ATTACH_PDF)

            menu.AppendSeparator()
            menu.Append(ID_ARTICLES_MATCH, "Match to PubMed...\t"+HK_ARTICLES_MATCH)
            menu.Append(ID_ARTICLES_UPDATE, "Update by PubMed\t"+HK_ARTICLES_UPDATE)
            
            menu.AppendSeparator()
            menu.Append(ID_ARTICLES_TRASH, "Move to Trash")
        
        # enable items
        menu.Enable(ID_ARTICLES_OPEN_PDF, any(x.pdf for x in articles))
        menu.Enable(ID_ARTICLES_OPEN_DOI, any(x.doi for x in articles))
        menu.Enable(ID_ARTICLES_OPEN_PMID, any(x.pmid for x in articles))
        menu.Enable(ID_ARTICLES_REVEAL_PDF, bool(len(articles) == 1 and articles[0].pdf))
        menu.Enable(ID_ARTICLES_COPY_CITATION, len(articles) != 0)
        menu.Enable(ID_ARTICLES_COPY_SUMMARY, len(articles) != 0)
        menu.Enable(ID_ARTICLES_COPY_LINK, len(articles) != 0)
        
        if is_trash:
            menu.Enable(ID_ARTICLES_RESTORE, len(articles) != 0)
            menu.Enable(ID_ARTICLES_DELETE, len(articles) != 0)
        
        else:
            menu.Enable(ID_ARTICLES_TRASH, len(articles) != 0)
            menu.Enable(ID_ARTICLES_RATING, len(articles) != 0)
            menu.Enable(ID_ARTICLES_COLOUR, len(articles) != 0)
            menu.Enable(ID_ARTICLES_LABELS, len(articles) != 0)
            menu.Enable(ID_ARTICLES_COLLECTIONS, len(articles) != 0)
            menu.Enable(ID_ARTICLES_EDIT, len(articles) == 1)
            menu.Enable(ID_ARTICLES_ATTACH_PDF, len(articles) == 1)
            menu.Enable(ID_ARTICLES_MATCH, len(articles) == 1)
            menu.Enable(ID_ARTICLES_UPDATE, any(x.pmid for x in articles))
        
        # show menu
        self.PopupMenu(menu)
        menu.Destroy()
    
    
    def _on_add_to_collection(self, evt):
        """Handles article add to collection event."""
        
        # get collection ID and status
        dbid, status = self._collection_ids[evt.GetId()]
        
        # post event
        event = events.ArticlesToCollectionEvent(self.GetId(), collection_dbid=dbid, collection_status=status)
        wx.PostEvent(self, event)
    
    
    def _make_ui(self):
        """Makes panel UI."""
        
        # make items
        self._top_bar = ArticlesTopBar(self)
        self._list = ArticlesList(self)
        
        # bind events
        self.Bind(events.EVT_ARTICLES_QUERY_CHANGED, self._on_query_changed)
        self.Bind(events.EVT_ARTICLES_ITEM_CONTEXT_MENU, self._on_item_context_menu)
        
        # pack UI
        self.Sizer = wx.BoxSizer(wx.VERTICAL)
        self.Sizer.Add(self._top_bar, 0, wx.EXPAND)
        self.Sizer.Add(self._list, 1, wx.EXPAND)
    
    
    def _make_rating_menu(self, articles):
        """Makes rating context menu."""
        
        # init menu
        menu = wx.Menu()
        
        # add items
        radius = 5
        space = 2
        outline = wx.Pen(mwx.RATING_OUTLINE_COLOUR, 1, wx.PENSTYLE_SOLID)
        fill_checked = wx.Brush(mwx.RATING_FILL_COLOUR, wx.BRUSHSTYLE_SOLID)
        fill_unchecked = wx.Brush(mwx.RATING_FILL_COLOUR_UNCHECKED, wx.BRUSHSTYLE_SOLID)
        bgr = wx.Brush(mwx.RATING_BGR_COLOUR, wx.BRUSHSTYLE_SOLID)
        
        bullets = (
            (ID_ARTICLES_RATING_0, 0, "None\t"+HK_ARTICLES_RATING_0),
            (ID_ARTICLES_RATING_1, 1, "Bad\t"+HK_ARTICLES_RATING_1),
            (ID_ARTICLES_RATING_2, 2, "Poor\t"+HK_ARTICLES_RATING_2),
            (ID_ARTICLES_RATING_3, 3, "Ok\t"+HK_ARTICLES_RATING_3),
            (ID_ARTICLES_RATING_4, 4, "Good\t"+HK_ARTICLES_RATING_4),
            (ID_ARTICLES_RATING_5, 5, "Excellent\t"+HK_ARTICLES_RATING_5))
        
        for id, value, text in bullets:
            
            item = wx.MenuItem(menu, id, text, kind=wx.ITEM_CHECK)
            bullet = images.rating(value, radius, space, outline, fill_unchecked, bgr)
            bullet_checked = images.rating(value, radius, space, outline, fill_checked, bgr)
            item.SetBitmaps(bullet_checked, bullet)
            menu.Append(item)
        
        # check items
        ratings = list(set(x.rating for x in articles))
        rating = ratings[0] if len(ratings) == 1 else None
        
        menu.Check(ID_ARTICLES_RATING_0, rating == 0)
        menu.Check(ID_ARTICLES_RATING_1, rating == 1)
        menu.Check(ID_ARTICLES_RATING_2, rating == 2)
        menu.Check(ID_ARTICLES_RATING_3, rating == 3)
        menu.Check(ID_ARTICLES_RATING_4, rating == 4)
        menu.Check(ID_ARTICLES_RATING_5, rating == 5)
        
        return menu
    
    
    def _make_colour_menu(self, articles):
        """Makes colour context menu."""
        
        # init menu
        menu = wx.Menu()
        
        # add items
        size = 5
        outline = wx.Pen(mwx.COLOUR_BULLET_OUTLINE_COLOUR, 1, wx.PENSTYLE_SOLID)
        outline_checked = wx.Pen(mwx.COLOUR_BULLET_OUTLINE_COLOUR_CHECKED, 1, wx.PENSTYLE_SOLID)
        
        bullets = (
            (ID_ARTICLES_COLOUR_GRAY, "None", mwx.COLOUR_BULLET_GRAY),
            (ID_ARTICLES_COLOUR_RED, "Red", mwx.COLOUR_BULLET_RED),
            (ID_ARTICLES_COLOUR_ORANGE, "Orange", mwx.COLOUR_BULLET_ORANGE),
            (ID_ARTICLES_COLOUR_YELLOW, "Yellow", mwx.COLOUR_BULLET_YELLOW),
            (ID_ARTICLES_COLOUR_GREEN, "Green", mwx.COLOUR_BULLET_GREEN),
            (ID_ARTICLES_COLOUR_BLUE, "Blue", mwx.COLOUR_BULLET_BLUE),
            (ID_ARTICLES_COLOUR_PURPLE, "Purple", mwx.COLOUR_BULLET_PURPLE))
        
        for id, text, colour in bullets:
            
            item = wx.MenuItem(menu, id, text, kind=wx.ITEM_CHECK)
            bullet = images.bullet(size, outline, wx.Brush(colour, wx.BRUSHSTYLE_SOLID))
            bullet_checked = images.bullet(size, outline_checked, wx.Brush(colour, wx.BRUSHSTYLE_SOLID))
            item.SetBitmaps(bullet_checked, bullet)
            menu.Append(item)
        
        # check items
        colours = list(set(x.colour for x in articles))
        colour = colours[0] if len(colours) == 1 else False
        
        menu.Check(ID_ARTICLES_COLOUR_GRAY, colour is None)
        menu.Check(ID_ARTICLES_COLOUR_RED, colour == mwx.rgb_to_hex(mwx.COLOUR_BULLET_RED))
        menu.Check(ID_ARTICLES_COLOUR_ORANGE, colour == mwx.rgb_to_hex(mwx.COLOUR_BULLET_ORANGE))
        menu.Check(ID_ARTICLES_COLOUR_YELLOW, colour == mwx.rgb_to_hex(mwx.COLOUR_BULLET_YELLOW))
        menu.Check(ID_ARTICLES_COLOUR_GREEN, colour == mwx.rgb_to_hex(mwx.COLOUR_BULLET_GREEN))
        menu.Check(ID_ARTICLES_COLOUR_BLUE, colour == mwx.rgb_to_hex(mwx.COLOUR_BULLET_BLUE))
        menu.Check(ID_ARTICLES_COLOUR_PURPLE, colour == mwx.rgb_to_hex(mwx.COLOUR_BULLET_PURPLE))
        
        return menu
    
    
    def _make_collections_menu(self, articles):
        """Makes collections context menu."""
        
        # clear IDs buffer
        self._collection_ids = {}
        
        # get available collections
        collections = self._library.search(core.Query("", core.Collection.NAME))
        collections = [x for x in collections if not x.query]
        
        # init menu
        menu = wx.Menu()
        menu.Append(ID_COLLECTIONS_NEW_FROM_SELECTION, "New from Selection...")
        
        if collections:
            menu.AppendSeparator()
        
        # add items
        for collection in sorted(collections, key=lambda x:x.title):
            
            # get related articles
            query = "%s[COLLECTIONID]" % collection.dbid
            coll_articles = self._library.search(core.Query(query, core.Article.NAME))
            coll_articles_ids = set(x.dbid for x in coll_articles)
            status = all(x.dbid in coll_articles_ids for x in articles)
            
            # add item
            coll_id = wx.NewIdRef()
            item = menu.Append(coll_id, collection.title, kind=wx.ITEM_CHECK)
            item.Check(status)
            
            # bind event
            self.Bind(wx.EVT_MENU, self._on_add_to_collection, id=coll_id)
            
            # remember dbid and status
            self._collection_ids[coll_id] = (collection.dbid, status)
        
        return menu
    
    
    def _show_articles(self, query="", order_by=lambda x:x.imported, reverse=True):
        """Shows articles according to given query."""
        
        self._articles = []
        
        # parse query
        if not isinstance(query, core.Query):
            query = core.Query(query, core.Article.NAME)
        
        # add master query
        if query.tree is not None and self._master_query:
            query = "(%s) AND (%s)" % (query.query, self._master_query) if query.tree else self._master_query
            query = core.Query(query, core.Article.NAME)
        
        # get articles
        if self._library is not None:
            self._articles = self._library.search(query)
        
        # sort articles
        self._articles.sort(key=order_by, reverse=reverse)
        
        # update list
        self._list.SetArticles(self._articles)
        
        # post event
        event = events.ArticlesSetEvent(self.GetId())
        wx.PostEvent(self, event)
