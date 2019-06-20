#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

# import modules
import webbrowser
import wx
from urllib.error import URLError

import core
from .. import events
from .list_ctrl import RepositoryList
from .top_bar import RepositoryTopBar
from .bottom_bar import RepositoryBottomBar


class RepositoryView(wx.Dialog):
    """Repository view panel."""
    
    
    def __init__(self, parent, library, query="", article=None):
        """Initializes repository view panel."""
        
        # get mode
        self._mode = 'match' if article is not None else 'search'
        
        # init panel
        width = 1027
        width -= 30 if self._mode == 'match' else 0
        title = "Match Article to PubMed" if self._mode == 'match' else "Search PubMed"
        wx.Dialog.__init__(self, parent, -1, size=(width, 580), title=title, style=wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER)
        
        self._library = library
        self._article = article
        self._articles = []
        self._results = None
        self._dois = []
        self._pmids = []
        
        # make UI
        self._make_ui()
        self._set_ids()
        
        # set current query
        query = self._set_query(query)
        
        # show frame
        self.Layout()
        self.Centre(wx.BOTH)
        self.Show(True)
        
        # set min size
        self.SetMinSize(self.GetSize())
        
        # start search
        if query:
            self._on_search()
    
    
    def GetArticles(self):
        """Gets list of all displayed articles."""
        
        return self._articles
    
    
    def GetSelectedArticles(self):
        """Gets list of selected articles."""
        
        return self._list.GetSelectedArticles()
    
    
    def _on_search(self, evt=None):
        """Handles search event."""
        
        query = self._top_bar.GetQuery()
        self._search(query)
    
    
    def _on_more(self, evt=None):
        """Handles more items event."""
        
        # check current results
        if self._results is None:
            self._on_search()
            return
        
        # run search
        self._search(self._results.query, self._results.retstop)
    
    
    def _on_ok(self, evt=None):
        """Handles OK event."""
        
        # get selected articles
        articles = self._list.GetSelectedArticles()
        if self._mode != 'search' and not articles:
            return
        
        # end dialog
        self.EndModal(wx.ID_OK)
    
    
    def _on_selection_changed(self, evt=None):
        """Handles row selection changed event."""
        
        # ignore for non-match mode
        if self._mode != 'match':
            return
        
        # enable or disable OK button
        self._top_bar.EnableOkButton(self._list.GetSelectedArticles())
    
    
    def _on_item_activated(self, evt=None):
        """Handles row activated event."""
        
        # get selected articles
        articles = self._list.GetSelectedArticles()
        if not articles:
            return
        
        # open web
        for article in articles:
            if article.pmid:
                link = "https://ncbi.nlm.nih.gov/pubmed/%s" % article.pmid
                try: webbrowser.open(link, autoraise=1)
                except: pass
    
    
    def _on_item_value_changed(self, evt):
        """Handles item value changed event."""
        
        # ignore for non-search mode
        if self._mode != 'search':
            return
        
        # enable or disable OK button
        self._top_bar.EnableOkButton(any(x.checked for x in self._articles))
        
        # update bottom bar
        self._update_bottom_bar()
    
    
    def _make_ui(self):
        """Makes panel UI."""
        
        # make items
        self._top_bar = RepositoryTopBar(self, self._mode)
        self._list = RepositoryList(self, self._mode)
        self._bottom_bar = RepositoryBottomBar(self)
        
        # bind events
        self.Bind(events.EVT_REPOSITORY_SEARCH, self._on_search)
        self.Bind(events.EVT_REPOSITORY_MORE, self._on_more)
        self.Bind(events.EVT_REPOSITORY_OK, self._on_ok)
        self.Bind(events.EVT_REPOSITORY_SELECTION_CHANGED, self._on_selection_changed)
        self.Bind(events.EVT_REPOSITORY_ITEM_ACTIVATED, self._on_item_activated)
        self.Bind(events.EVT_REPOSITORY_ITEM_VALUE_CHANGED, self._on_item_value_changed)
        
        # pack UI
        self.Sizer = wx.BoxSizer(wx.VERTICAL)
        self.Sizer.Add(self._top_bar, 0, wx.EXPAND)
        self.Sizer.Add(self._list, 1, wx.EXPAND)
        self.Sizer.Add(self._bottom_bar, 0, wx.EXPAND)
    
    
    def _set_ids(self):
        """Gets DOIs of all available articles."""
        
        # get ids
        data = self._library.query("SELECT doi, pmid FROM articles")
        
        # set ids
        self._dois = [x['doi'] for x in data if x['doi']]
        self._pmids = [x['pmid'] for x in data if x['pmid']]
    
    
    def _set_query(self, query):
        """Sets starting query based on current article."""
        
        # set given query
        if query:
            self._top_bar.ChangeQuery(query)
        
        # check article
        elif self._article is None:
            query = ""
            self._top_bar.ChangeQuery(query)
        
        # use PMID
        elif self._article.pmid:
            query = "%s[UID]" % self._article.pmid
            self._top_bar.ChangeQuery(query)
        
        # use DOI
        elif self._article.doi:
            query = "%s[DOI]" % self._article.doi
            self._top_bar.ChangeQuery(query)
        
        # use title
        elif self._article.title:
            query = "%s" % self._article.title
            self._top_bar.ChangeQuery(query)
        
        return query
    
    
    def _search(self, query, retstart=0):
        """Runs PubMed query and displays articles."""
        
        # disable buttons
        self._top_bar.EnableSearchButton(False, "Searching...")
        self._top_bar.EnableSearchQuery(False)
        self._top_bar.EnableMoreButton(False)
        self._top_bar.EnableOkButton(False)
        
        # check query
        if not query:
            self._results = None
            self._articles = []
            self._top_bar.EnableSearchButton(True)
            self._top_bar.EnableSearchQuery(True)
            self._list.SetArticles(self._articles)
            self._bottom_bar.SetLabel("No query specified")
            return
        
        # update bottom bar
        self._bottom_bar.SetLabel("Searching...")
        wx.Yield()
        
        # search PubMed
        old_results = self._results
        
        try:
            pubmed = core.PubMed(exsafe=False)
            self._results = pubmed.search(query, retstart=retstart, retmax=20)
        
        except URLError:
            self._results = old_results
            self._top_bar.EnableSearchButton(True)
            self._top_bar.EnableSearchQuery(True)
            self._bottom_bar.SetLabel("An error occurred")
            return
        
        # get articles
        articles = self._results.articles
        self._articles = self._articles + articles if retstart else articles
        
        # set in-library and checked status
        for article in articles:
            
            article.in_library = False
            article.checked = False
            
            if article.pmid is not None and article.pmid in self._pmids:
                article.in_library = True
            elif article.doi is not None and article.doi in self._dois:
                article.in_library = True
        
        # show articles
        self._list.SetArticles(self._articles)
        
        # enable buttons
        self._top_bar.EnableSearchQuery(True)
        self._top_bar.EnableSearchButton(True)
        self._top_bar.EnableMoreButton(self._results.retstop < self._results.total)
        self._top_bar.EnableOkButton(self._mode=='search' and any(x.checked for x in self._articles))
        
        # update bottom bar
        self._update_bottom_bar()
    
    
    def _update_bottom_bar(self):
        """Updates status label in bottom bar."""
        
        # get main label
        if self._results is None:
            label = "0 articles found"
        elif self._results.total == 1:
            label = "1 article found"
        elif self._results.total == self._results.count:
            label = "%s articles found" % self._results.total
        else:
            label = "1 to %s of %s articles found" % (self._results.retstop, self._results.total)
        
        # count checked articles
        if self._mode == 'search' and self._results is not None and self._results.total:
            label += " (%s checked)" % sum(1 for x in self._articles if x.checked)
        
        # set label
        self._bottom_bar.SetLabel(label)
