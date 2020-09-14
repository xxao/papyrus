#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

# import modules
import time
import tempfile
import os.path
import wx
import wx.html2 as wxweb

from .. import mwx
from .. import events
from .html_template import *


class DetailsView(wx.Panel):
    """Details view panel."""
    
    
    def __init__(self, parent):
        """Initializes details view panel."""
        
        # init panel
        wx.Panel.__init__(self, parent, -1, style=wx.NO_FULL_REPAINT_ON_RESIZE)
        self.SetOwnBackgroundColour(mwx.DETAILS_VIEW_BGR)
        self.Bind(wx.EVT_PAINT, self._on_paint)
        
        # init buffers
        self._article = None
        
        # make UI
        self._make_ui()
        
        # show default page
        self._show_details()
    
    
    def SetArticle(self, article):
        """Sets article to display."""
        
        # check for same article
        if self._article is article:
            return
        
        # set article
        self._article = article
        
        # show page
        self._show_details()
    
    
    def _on_paint(self, evt):
        """Draws background image."""
        
        if mwx.IS_WIN:
            mwx.panel_top_line(self, mwx.DARK_DIVIDER_COLOUR)
    
    
    def _on_context_menu(self, evt):
        """Handles context menu event."""
        
        pass
    
    
    def _on_navigating(self, evt):
        """Handles navigating event."""
        
        # get URL
        url = evt.GetURL()
        
        # veto own links
        if url.startswith("papyrus:"):
            evt.Veto()
            
            # raise event
            event = events.DetailsNavigatingEvent(self.GetId(), url=url)
            wx.PostEvent(self, event)
    
    
    def _make_ui(self):
        """Makes panel UI."""
        
        # make empty label
        label = wx.StaticText(self, -1, "Article Details", style=wx.ALIGN_CENTER)
        font = wx.Font(14, wx.DEFAULT, wx.NORMAL, wx.BOLD)
        label.SetFont(font)
        label.SetForegroundColour((190,190,190))
        
        # make browser
        self._browser = wxweb.WebView.New(self, style=wx.NO_BORDER)
        self._browser.SetEditable(False)
        self._browser.EnableContextMenu(False)
        self._browser.EnableHistory(False)
        
        # bind events
        self.Bind(wx.EVT_RIGHT_UP, self._on_context_menu)
        self.Bind(wxweb.EVT_WEBVIEW_NAVIGATING, self._on_navigating)
        
        # pack UI
        self.Sizer = wx.BoxSizer(wx.VERTICAL)
        self.Sizer.Add(label, 0, wx.EXPAND|wx.TOP, 80)
        self.Sizer.Add(self._browser, 1, wx.EXPAND)
        
        # add top line
        self.Sizer.InsertSpacer(0, 1)
        if not mwx.IS_WIN:
            self.Sizer.Hide(0)
    
    
    def _show_details(self):
        """Shows current article details."""
        
        # check article
        if self._article is None:
            self.Sizer.Show(1)
            self.Sizer.Hide(2)
            self.Sizer.Layout()
            return
        
        # show browser
        self.Sizer.Hide(1)
        self.Sizer.Show(2)
        self.Sizer.Layout()
        
        # make HTML
        html = self._make_html()
        
        # show html
        if wx.Platform == "__WXMAC__":
            self._browser.SetPage(html, "")
            return
        
        # get tmp file path
        temp = tempfile.gettempdir()
        path = os.path.join(temp, 'papyrus_details.html')
        
        # write HTML inside tmp file
        with open(path, 'w', encoding="utf-8") as tmp_file:
            tmp_file.write(html)
        
        # show page
        path = 'file://%s?%s' % (path, time.time())
        self._browser.LoadURL(path)
    
    
    def _make_html(self):
        """Creates HTML for current article."""
        
        # init HTML
        html = HTML_ARTICLE_TOP
        
        # add title
        title = self._article.title if self._article.title else "No Title"
        html += '<h1 id="title">%s</h1>' % title
        
        # add rating
        html += '<div id="rating">'
        for i in range(1,6):
            selected = "selected" if self._article.rating >= i else ""
            html += '<a href="papyrus:?rating=%d" class="%s" title="%s">&#x25CF;</a>' % (i, selected, mwx.RATING_NAMES[i].title())
        html += '</div>'
        
        # add colour
        html += '<div id="colour">'
        for c in mwx.COLOUR_NAMES:
            colour = mwx.rgb_to_hex(mwx.COLOUR_BULLETS[c])
            selected = "selected" if self._article.colour == colour else ""
            html += '<a href="papyrus:?colour=%s" class="%s" style="background-color:#%s;" title="%s">&nbsp;</a>' % (c, selected, colour, c.title())
        html += '</div>'
        
        # add citation
        citation = self._article.citation
        journal = self._article.journal.abbreviation if self._article.journal and self._article.journal.abbreviation else ""
        html += '<p id="citation"><a href="papyrus:?journal=%s" title="Search PubMed by journal">%s</a></p>' % (journal, citation) if citation else ""
        
        # add DOI
        doi = self._article.doi
        html += '<p id="doi">DOI: <a href="papyrus:?doi=%s" title="Show article website">%s</a></p>' % (doi, doi) if doi else ""
        
        # add PMID
        pmid = self._article.pmid
        html += '<p id="pmid">PMID: <a href="papyrus:?pmid=%s" title="Show article PubMed website">%s</a></p>' % (pmid, pmid) if pmid else ""
        
        # add filename
        filename = self._article.filename
        html += '<p id="filename">PDF: <a href="papyrus:?pdf=%s" title="Reveal PDF file">%s</a></p>' % (filename, filename) if self._article.pdf else ""
        
        # add authors
        if self._article.authors:
            html += '<div id="authors"><h2>Authors</h2><ul>'
            for item in self._article.authors:
                html += '<li><a href="papyrus:?author=%s" title="Search PubMed by author">%s</a> ' % (item.shortname, item.longname)
                html += '<a href="papyrus:?authorid=%s" title="Show articles in library" class="author_count">(%d)</a></li> ' % (item.dbid, item.count)
            html += '</ul></div>'
        
        # add labels
        if self._article.labels:
            html += '<div id="labels"><h2>Labels</h2><p>'
            for item in self._article.labels:
                html += '<a href="papyrus:?labelid=%s" title="Show articles in library">%s</a>, ' % (item.dbid, item.title)
            html = html[:-2] + '</p></div>'
        
        # add collections
        if self._article.collections:
            html += '<div id="collections"><h2>Collections</h2><p>'
            for item in self._article.collections:
                html += '<a href="papyrus:?collectionid=%s" title="Show articles in library">%s</a>, ' % (item.dbid, item.title)
            html = html[:-2] + '</p></div>'
        
        # add notes
        if self._article.notes:
            html += '<div id="notes"><h2>Notes</h2>'
            for par in self._article.notes.split("\n\n"):
                html += '<p>%s</p>' % par
            html += '</div>'
        
        # add abstract
        if self._article.abstract:
            html += '<div id="abstract"><h2>Abstract</h2>'
            for par in self._article.abstract.split("\n\n"):
                html += '<p>%s</p>' % par
            html += '</div>'
        
        # finalize html
        html += HTML_BOTTOM
        
        return html
