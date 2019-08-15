#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

# import modules
import wx

from . import mwx
from . import images
from . import config
from .ids import *
from .hotkeys import *


class MenuBar(wx.MenuBar):
    """Main app menu."""
    
    
    def __init__(self):
        """Initializes main app menu."""
        
        # init menu bar
        super(MenuBar, self).__init__()
        
        # init buffers
        self._library = None
        self._collection = None
        self._articles = []
        
        # init menus
        self._make_file_menu()
        self._make_view_menu()
        self._make_articles_menu()
        self._make_collections_menu()
        
        # update status
        self.SetLibrary()
    
    
    def SetLibrary(self, library=None):
        """Sets library database."""
        
        # set library
        self._library = library
        
        # enable menu items
        self.Enable(ID_COLLECTIONS_EMPTY_TRASH, self._library is not None)
        self.Enable(ID_COLLECTIONS_NEW_MANUAL, self._library is not None)
        self.Enable(ID_COLLECTIONS_NEW_SMART, self._library is not None)
        self.Enable(ID_LABELS_NEW, self._library is not None)
        self.Enable(ID_ARTICLES_NEW, self._library is not None)
        self.Enable(ID_ARTICLES_IMPORT, self._library is not None)
        
        # set others
        self.SetCollection()
        self.SetArticles()
    
    
    def SetArticles(self, articles=None):
        """Sets selected articles."""
        
        # set articles
        self._articles = articles or []
        
        # enable menu items
        self.Enable(ID_ARTICLES_OPEN_PDF, any(x.pdf for x in self._articles))
        self.Enable(ID_ARTICLES_OPEN_DOI, any(x.doi for x in self._articles))
        self.Enable(ID_ARTICLES_OPEN_PMID, any(x.pmid for x in self._articles))
        self.Enable(ID_ARTICLES_REVEAL_PDF, bool(len(self._articles) == 1 and self._articles[0].pdf))
        
        self.Enable(ID_ARTICLES_COPY_CITATION, len(self._articles) != 0)
        self.Enable(ID_ARTICLES_COPY_SUMMARY, len(self._articles) != 0)
        self.Enable(ID_ARTICLES_COPY_LINK, len(self._articles) != 0)
        
        self.Enable(ID_ARTICLES_RATING, len(self._articles) != 0)
        self.Enable(ID_ARTICLES_COLOUR, len(self._articles) != 0)
        self.Enable(ID_ARTICLES_LABELS, len(self._articles) != 0)
        
        self.Enable(ID_ARTICLES_EDIT, len(self._articles) == 1)
        self.Enable(ID_ARTICLES_ATTACH_PDF, len(self._articles) == 1)
        self.Enable(ID_ARTICLES_MATCH, len(self._articles) == 1)
        self.Enable(ID_ARTICLES_UPDATE, any(x.pmid for x in self._articles))
        
        # enable trash
        is_trash = self._collection is not None \
            and self._collection.group == 'system' \
            and self._collection.query == '1[TRASH]'

        self.Enable(ID_ARTICLES_TRASH_MENU, len(self._articles) != 0)
        self.Enable(ID_ARTICLES_TRASH, not is_trash and len(self._articles) != 0)
        self.Enable(ID_ARTICLES_DELETE, is_trash and len(self._articles) != 0)
        self.Enable(ID_ARTICLES_RESTORE, is_trash and len(self._articles) != 0)
        
        # enable menu items in collections
        self.Enable(ID_COLLECTIONS_NEW_FROM_SELECTION, len(self._articles) != 0)
        
        # update sub-menus
        self._update_rating_menu()
        self._update_colour_menu()
    
    
    def SetCollection(self, collection=None):
        """Sets selected collections."""
        
        # set collection
        self._collection = collection
        
        # enable menu items for manual and smart collections
        is_custom = collection is not None and collection.group == "custom"
        self.Enable(ID_COLLECTIONS_EDIT, is_custom)
        self.Enable(ID_COLLECTIONS_DELETE, is_custom)
        
        # enable menu items for labels
        is_label = collection is not None and collection.group == "labels"
        self.Enable(ID_LABELS_EDIT, is_label)
        self.Enable(ID_LABELS_DELETE, is_label)
    
    
    def _make_file_menu(self):
        """Makes file sub-menu."""
        
        # init menu
        menu = wx.Menu()
        
        # add items
        menu.Append(ID_ARTICLES_NEW, "New Article...\t"+HK_ARTICLES_NEW)
        menu.Append(ID_ARTICLES_IMPORT, "Import Articles...\t"+HK_ARTICLES_IMPORT)
        
        menu.AppendSeparator()
        menu.Append(ID_LIBRARY_NEW, "New Library...\t"+HK_LIBRARY_NEW)
        menu.Append(ID_LIBRARY_OPEN, "Open Library...\t"+HK_LIBRARY_OPEN)
        menu.Append(ID_LIBRARY_ANALYZE, "Analyze Library\t"+HK_LIBRARY_ANALYZE)
        
        menu.AppendSeparator()
        menu.Append(ID_QUIT, "Quit Papyrus\t"+HK_QUIT)
        
        # add to menu bar
        self.Append(menu, '&File')
    
    
    def _make_view_menu(self):
        """Makes view sub-menu."""
        
        # init menu
        menu = wx.Menu()
        
        # add items
        menu.Append(ID_VIEW_COLLECTIONS, "Show Collections\t"+HK_VIEW_COLLECTIONS, kind=wx.ITEM_CHECK)
        menu.Append(ID_VIEW_PDF, "Show PDF Preview\t"+HK_VIEW_PDF, kind=wx.ITEM_CHECK)
        menu.Append(ID_VIEW_DETAILS, "Show Article Details\t"+HK_VIEW_DETAILS, kind=wx.ITEM_CHECK)
        
        # add to menu bar
        self.Append(menu, '&View')
        
        # set state
        self.Check(ID_VIEW_COLLECTIONS, config.SETTINGS['collections_view_enabled'])
        self.Check(ID_VIEW_PDF, config.SETTINGS['pdf_view_enabled'])
        self.Check(ID_VIEW_DETAILS, config.SETTINGS['details_view_enabled'])
    
    
    def _make_articles_menu(self):
        """Makes articles sub-menu."""
        
        # init menu
        menu = wx.Menu()
        
        # add items
        menu.Append(ID_ARTICLES_OPEN_PDF, "Open PDF File\t"+HK_ARTICLES_OPEN_PDF)
        menu.Append(ID_ARTICLES_OPEN_DOI, "Open Website\t"+HK_ARTICLES_OPEN_DOI)
        menu.Append(ID_ARTICLES_OPEN_PMID, "Open in PubMed\t"+HK_ARTICLES_OPEN_PMID)
        menu.Append(ID_ARTICLES_REVEAL_PDF, "Reveal PDF File\t"+HK_ARTICLES_REVEAL_PDF)
        
        menu.AppendSeparator()
        menu.Append(ID_ARTICLES_COPY_CITATION, "Copy Citation\t"+HK_ARTICLES_COPY_CITATION)
        menu.Append(ID_ARTICLES_COPY_SUMMARY, "Copy Summary\t"+HK_ARTICLES_COPY_SUMMARY)
        menu.Append(ID_ARTICLES_COPY_LINK, "Copy Link\t"+HK_ARTICLES_COPY_LINK)
        
        menu.AppendSeparator()
        menu.Append(ID_ARTICLES_RATING, "Rating", self._make_rating_menu())
        menu.Append(ID_ARTICLES_COLOUR, "Color", self._make_colour_menu())
        menu.Append(ID_ARTICLES_LABELS, "Labels...\t"+HK_ARTICLES_LABELS)
        
        menu.AppendSeparator()
        menu.Append(ID_ARTICLES_EDIT, "Edit...\t"+HK_ARTICLES_EDIT)
        menu.Append(ID_ARTICLES_ATTACH_PDF, "Attach PDF...\t"+HK_ARTICLES_ATTACH_PDF)
        
        menu.AppendSeparator()
        menu.Append(ID_ARTICLES_MATCH, "Match to PubMed...\t"+HK_ARTICLES_MATCH)
        menu.Append(ID_ARTICLES_UPDATE, "Update by PubMed...\t"+HK_ARTICLES_UPDATE)
        
        trash_menu = wx.Menu()
        trash_menu.Append(ID_ARTICLES_TRASH, "Move to Trash\t"+HK_ARTICLES_TRASH)
        trash_menu.Append(ID_ARTICLES_DELETE, "Delete Permanently")
        trash_menu.AppendSeparator()
        trash_menu.Append(ID_ARTICLES_RESTORE, "Restore from Trash\t"+HK_ARTICLES_RESTORE)
        
        menu.AppendSeparator()
        menu.Append(ID_ARTICLES_TRASH_MENU, "Trash", trash_menu)
        
        # add to menu bar
        self.Append(menu, '&Articles')
    
    
    def _make_collections_menu(self):
        """Makes collections sub-menu."""
        
        # init menu
        menu = wx.Menu()
        
        # add items
        menu.Append(ID_COLLECTIONS_NEW_FROM_SELECTION, "New from Selection...\t"+HK_COLLECTIONS_NEW_FROM_SELECTION)
        
        menu.AppendSeparator()
        menu.Append(ID_COLLECTIONS_NEW_MANUAL, "New Collection...")
        menu.Append(ID_COLLECTIONS_NEW_SMART, "New Smart Collection...")
        menu.Append(ID_LABELS_NEW, "New Label...")
        
        menu.AppendSeparator()
        menu.Append(ID_COLLECTIONS_EDIT, "Edit Collection...")
        menu.Append(ID_COLLECTIONS_DELETE, "Delete Collection")
        
        menu.AppendSeparator()
        menu.Append(ID_LABELS_EDIT, "Edit Label...")
        menu.Append(ID_LABELS_DELETE, "Delete Label")
        
        menu.AppendSeparator()
        menu.Append(ID_COLLECTIONS_EMPTY_TRASH, "Empty Trash")
        
        # add to menu bar
        self.Append(menu, '&Collections')
    
    
    def _make_rating_menu(self):
        """Makes rating sub-menu."""
        
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
        
        return menu
    
    
    def _make_colour_menu(self):
        """Makes colour sub-menu."""
        
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
        
        return menu
        
    
    def _update_rating_menu(self):
        """Updates rating menu according to current state."""
        
        # enable items
        enabled = len(self._articles) > 0
        self.Enable(ID_ARTICLES_RATING_0, enabled)
        self.Enable(ID_ARTICLES_RATING_1, enabled)
        self.Enable(ID_ARTICLES_RATING_2, enabled)
        self.Enable(ID_ARTICLES_RATING_3, enabled)
        self.Enable(ID_ARTICLES_RATING_4, enabled)
        self.Enable(ID_ARTICLES_RATING_5, enabled)
        
        # check items
        ratings = list(set(x.rating for x in self._articles))
        rating = ratings[0] if len(ratings) == 1 else None
        
        self.Check(ID_ARTICLES_RATING_0, rating == 0)
        self.Check(ID_ARTICLES_RATING_1, rating == 1)
        self.Check(ID_ARTICLES_RATING_2, rating == 2)
        self.Check(ID_ARTICLES_RATING_3, rating == 3)
        self.Check(ID_ARTICLES_RATING_4, rating == 4)
        self.Check(ID_ARTICLES_RATING_5, rating == 5)
    
    
    def _update_colour_menu(self):
        """Updates colour menu according to current state."""
        
        # enable items
        enabled = len(self._articles) > 0
        self.Enable(ID_ARTICLES_COLOUR_GRAY, enabled)
        self.Enable(ID_ARTICLES_COLOUR_RED, enabled)
        self.Enable(ID_ARTICLES_COLOUR_ORANGE, enabled)
        self.Enable(ID_ARTICLES_COLOUR_YELLOW, enabled)
        self.Enable(ID_ARTICLES_COLOUR_GREEN, enabled)
        self.Enable(ID_ARTICLES_COLOUR_BLUE, enabled)
        self.Enable(ID_ARTICLES_COLOUR_PURPLE, enabled)
        
        # check items
        colours = list(set(x.colour for x in self._articles))
        colour = colours[0] if len(colours) == 1 else False
        
        self.Check(ID_ARTICLES_COLOUR_GRAY, colour is None)
        self.Check(ID_ARTICLES_COLOUR_RED, colour == mwx.rgb_to_hex(mwx.COLOUR_BULLET_RED))
        self.Check(ID_ARTICLES_COLOUR_ORANGE, colour == mwx.rgb_to_hex(mwx.COLOUR_BULLET_ORANGE))
        self.Check(ID_ARTICLES_COLOUR_YELLOW, colour == mwx.rgb_to_hex(mwx.COLOUR_BULLET_YELLOW))
        self.Check(ID_ARTICLES_COLOUR_GREEN, colour == mwx.rgb_to_hex(mwx.COLOUR_BULLET_GREEN))
        self.Check(ID_ARTICLES_COLOUR_BLUE, colour == mwx.rgb_to_hex(mwx.COLOUR_BULLET_BLUE))
        self.Check(ID_ARTICLES_COLOUR_PURPLE, colour == mwx.rgb_to_hex(mwx.COLOUR_BULLET_PURPLE))
