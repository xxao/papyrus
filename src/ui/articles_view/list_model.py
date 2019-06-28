#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

# import modules
import os.path
import wx
import wx.dataview as wxdv
import datetime

import core
from .. import mwx
from .. import images


class ArticlesListModel(wxdv.DataViewIndexListModel):
    """Articles list data source model."""
    
    
    def __init__(self, data=None):
        """Initializes data source model."""
        
        # init data
        self._data = data if data is not None else []
        self._col_names = [
            'expander',
            'colour',
            'pdf',
            'rating',
            'authors',
            'title',
            'journal',
            'import',
            'year',
            'volume',
            'issue',
            'pages',
            'doi',
            'key',
            'pmid',
            'labels']
        
        wxdv.DataViewIndexListModel.__init__(self, len(self._data))
        
        # init caches
        self._bullets = {}
        self._rating = {}
    
    
    def GetColumnType(self, col):
        """Gets type of specified column."""
        
        # get column name
        name = self._col_names[col]
        
        # return type
        if name == "colour":
            return "bitmap"
        
        if name == "pdf":
            return "bitmap"
        
        if name == "rating":
            return "bitmap"
        
        return "string"
    
    
    def GetValueByRow(self, row, col):
        """Gets value for given row and column."""
        
        # get column name
        name = self._col_names[col]
        
        # get native value
        article = self._data[row]
        value = self.GetItemValue(article, col)
        
        # return values
        if name == "expander":
            return ""
        
        if name == "colour":
            return self._get_bullet(value)
        
        if name == "pdf":
            if not value: return images.SPACER
            elif os.path.exists(value): return images.ICON_PDF 
            else: return images.ICON_PDF_MISSING
        
        if value is None:
            return ""
        
        if name == "rating":
            return self._get_rating(value)
        
        if name == "authors":
            return self._get_authors(value)
        
        if name == "title":
            return value
        
        if name == "journal":
            return value
        
        if name == "import":
            return datetime.datetime.utcfromtimestamp(value).strftime('%Y-%m-%d')
        
        if name == "year":
            return str(value)
        
        if name == "volume":
            return value
        
        if name == "issue":
            return value
        
        if name == "pages":
            return self._get_pages(value)
        
        if name == "doi":
            return value
        
        if name == "key":
            return value
        
        if name == "pmid":
            return value
        
        if name == "labels":
            return value
    
    
    def GetItemValue(self, item, col):
        """Gets native column value from given item."""
        
        # get column name
        name = self._col_names[col]
        
        # return value
        if name == "expander":
            return ""
        
        if name == "colour":
            return item.colour
        
        if name == "pdf":
            return item.pdf_path
        
        if name == "rating":
            return item.rating
        
        if name == "authors":
            return item.authors
        
        if name == "title":
            return item.title
        
        if name == "journal":
            return item.journal.abbreviation if item.journal else None
        
        if name == "import":
            return item.imported
        
        if name == "year":
            return item.year
        
        if name == "volume":
            return item.volume
        
        if name == "issue":
            return item.issue
        
        if name == "pages":
            return item.pages
        
        if name == "doi":
            return item.doi
        
        if name == "key":
            return item.key
        
        if name == "pmid":
            return item.pmid
        
        if name == "labels":
            return ", ".join(x.title for x in item.labels)
    
    
    def GetColumnCount(self):
        """Returns number of available columns."""
        
        return len(self._col_names)
    
    
    def GetCount(self):
        """Returns number of available rows."""
        
        return len(self._data)
    
    
    def GetAttrByRow(self, row, col, attr):
        """Returns specific attributes."""
        
        # mark thrashed articles
        if self._data[row].deleted:
            attr.SetItalic(True)
            attr.SetColour(wx.Colour(mwx.ARTICLE_DELETED_COLOUR))
            return True
        
        return False
    
    
    def Compare(self, item1, item2, col, ascending):
        """Compares given items by specific column."""
        
        # swap sort order
        if not ascending:
            item2, item1 = item1, item2
        
        # get corresponding rows
        row1 = self.GetRow(item1)
        row2 = self.GetRow(item2)
        
        # get native values
        value1 = self.GetItemValue(self._data[row1], col)
        value2 = self.GetItemValue(self._data[row2], col)
        
        # check for None
        if value1 is None:
            return -1
        if value2 is None:
            return 1
        
        # get column name
        name = self._col_names[col]
        
        # convert specific values
        if name == 'authors' and value1 and value2:
            value1 = value1[0].shortname
            value2 = value2[0].shortname
        
        # compare values
        return (value1 > value2) - (value1 < value2)
    
    
    def _get_bullet(self, colour_hex):
        """Gets bullet icon for specific colour."""
        
        # check colour
        if not colour_hex:
            colour_hex = mwx.rgb_to_hex(mwx.COLOUR_BULLET_GRAY)
        
        # check cache
        if colour_hex in self._bullets:
            return self._bullets[colour_hex]
        
        # convert colour
        colour = mwx.hex_to_rgb(colour_hex)
        
        # make bitmap
        bitmap = images.bullet(
            radius = mwx.COLOUR_BULLET_SIZE,
            outline = wx.Pen(mwx.COLOUR_BULLET_OUTLINE_COLOUR, 1, wx.SOLID),
            fill = wx.Brush(colour, wx.SOLID))
        
        # cache bitmap
        self._bullets[colour_hex] = bitmap
        
        return bitmap
    
    
    def _get_rating(self, value):
        """Gets rating icon for specific value."""
        
        # check cache
        if value in self._rating:
            return self._rating[value]
        
        # make bitmap
        bitmap = images.rating(
            value = value,
            radius = mwx.RATING_SIZE,
            space = mwx.RATING_SPACE,
            outline = wx.Pen(mwx.RATING_OUTLINE_COLOUR, 1, wx.SOLID),
            fill = wx.Brush(mwx.RATING_FILL_COLOUR, wx.SOLID),
            bgr = wx.Brush(mwx.RATING_BGR_COLOUR, wx.SOLID))
        
        # cache bitmap
        self._rating[value] = bitmap
        
        return bitmap
    
    
    def _get_authors(self, authors):
        """Formats authors."""
        
        # check authors
        if not authors:
            return ""
        
        # one author only
        if len(authors) == 1:
            return authors[0].shortname
        
        # two authors
        if len(authors) == 2:
            return "%s and %s" % (authors[0].shortname, authors[1].shortname)
        
        # more authors
        return "%s, %s et al." % (authors[0].shortname, authors[-1].shortname)
    
    
    def _get_pages(self, pages):
        """Parses pages string adds the page count."""
        
        # check pages
        if not pages:
            return ""
        
        # parse pages
        count = core.count_pages(pages)
        if count is None:
            return pages
        
        # format pages
        return "%s (%d)" % (pages, count)
