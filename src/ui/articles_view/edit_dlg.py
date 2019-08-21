#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

# import modules
import wx

import core
from .. import mwx


class ArticlesEditDlg(wx.Dialog):
    """Dialog to edit article."""
    
    
    def __init__(self, parent, article, journals=[]):
        """Initializes article dialog."""
        
        # init dialog
        wx.Dialog.__init__(self, parent, -1, title="Article", size=(400, -1), style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)
        self.Bind(wx.EVT_PAINT, self._on_paint)
        
        # init buffers
        self._article = article
        self._journals = journals
        
        # make UI
        self._make_ui()
        
        # display dialog
        self.Layout()
        self.Sizer.Fit(self)
        self.SetMinSize(self.GetSize())
        self.Centre()
    
    
    def _on_paint(self, evt):
        """Draws background image."""
        
        if mwx.IS_WIN:
            mwx.panel_top_line(self, mwx.DARK_DIVIDER_COLOUR)
    
    
    def _on_ok(self, evt=None):
        """Handles OK button."""
        
        # get original values
        title = self._article.title
        abstract = self._article.abstract
        notes = self._article.notes
        authors = self._article.authors
        journal = self._article.journal
        doi = self._article.doi
        pmid = self._article.pmid
        volume = self._article.volume
        issue = self._article.issue
        pages = self._article.pages
        year = self._article.year
        
        # get title
        if self._title_value.IsModified():
            title = self._title_value.GetValue().strip()
        
        # get abstract
        if self._abstract_value.IsModified():
            abstract = self._abstract_value.GetValue().strip()
        
        # get notes
        if self._notes_value.IsModified():
            notes = self._notes_value.GetValue().strip()
        
        # get authors
        if self._authors_value.IsModified():
            authors = self._get_authors(self._authors_value.GetValue().strip())
        
        # get journal
        journal = self._get_journal(self._journal_combo.GetValue().strip())
        
        # get DOI
        if self._doi_value.IsModified():
            doi = self._doi_value.GetValue().strip()
        
        # get PMID
        if self._pmid_value.IsModified():
            pmid = self._pmid_value.GetValue().strip()
        
        # get volume
        if self._volume_value.IsModified():
            volume = self._volume_value.GetValue().strip()
        
        # get issue
        if self._issue_value.IsModified():
            issue = self._issue_value.GetValue().strip()
        
        # get pages
        if self._pages_value.IsModified():
            pages = self._pages_value.GetValue().strip()
        
        # get year
        if self._year_value.IsModified():
            year = self._year_value.GetValue().strip()
            try:
                year = int(year) if year else None
            except ValueError:
                wx.Bell()
                return
        
        # update article
        self._article.title = title
        self._article.abstract = abstract
        self._article.notes = notes
        self._article.authors = authors
        self._article.journal = journal
        self._article.doi = doi
        self._article.pmid = pmid
        self._article.volume = volume
        self._article.issue = issue
        self._article.pages = pages
        self._article.year = year
        
        # close dialog
        self.EndModal(wx.ID_OK)
    
    
    def _on_cancel(self, evt=None):
        """Handles cancel button."""
        
        self.EndModal(wx.ID_CANCEL)
    
    
    def _make_ui(self):
        """Makes dialog UI."""
        
        # make notebook
        notebook = wx.Notebook(self)
        notebook.AddPage(self._make_info_page(notebook), "Info")
        notebook.AddPage(self._make_abstract_page(notebook), "Abstract")
        notebook.AddPage(self._make_notes_page(notebook), "Notes")
        
        # make buttons
        cancel_butt = wx.Button(self, wx.ID_CANCEL, "Cancel")
        ok_butt = wx.Button(self, wx.ID_OK, "OK")
        
        # bind events
        cancel_butt.Bind(wx.EVT_BUTTON, self._on_cancel)
        ok_butt.Bind(wx.EVT_BUTTON, self._on_ok)
        
        # pack items
        buttons = wx.BoxSizer(wx.HORIZONTAL)
        buttons.Add(cancel_butt, 0, wx.RIGHT, mwx.PANEL_SPACE_MAIN)
        buttons.Add(ok_butt, 0)
        
        self.Sizer = wx.BoxSizer(wx.VERTICAL)
        self.Sizer.Add(notebook, 1, wx.ALL | wx.EXPAND, mwx.PANEL_SPACE_MAIN)
        self.Sizer.Add(buttons, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.ALIGN_RIGHT, mwx.PANEL_SPACE_MAIN)
    
    
    def _make_info_page(self, notebook):
        """Makes info page."""
        
        # init page
        page = wx.Panel(notebook)
        
        # make items
        title_label = wx.StaticText(page, -1, "Title:")
        text = self._article.title if self._article.title else ""
        self._title_value = wx.TextCtrl(page, -1, text, size=(400,100), style=wx.TE_MULTILINE)
        
        authors_label = wx.StaticText(page, -1, "Authors:")
        text = ", ".join(x.longname for x in self._article.authors)
        self._authors_value = wx.TextCtrl(page, -1, text, size=(400,100), style=wx.TE_MULTILINE)
        self._authors_value.SetToolTip(wx.ToolTip("Lastname Firstname I, Lastname Firstname I"))
        
        journal_label = wx.StaticText(page, -1, "Journal:")
        text = self._article.journal.abbreviation if self._article.journal else ""
        choices = [x.abbreviation for x in self._journals]
        choices.sort()
        self._journal_combo = wx.ComboBox(page, -1, text, choices=choices, size=(400,-1), style=wx.CB_DROPDOWN)
        
        year_label = wx.StaticText(page, -1, "Year:")
        text = str(self._article.year) if self._article.year else ""
        self._year_value = wx.TextCtrl(page, -1, text, size=(-1,-1))
        
        volume_label = wx.StaticText(page, -1, "Volume:")
        text = self._article.volume if self._article.volume else ""
        self._volume_value = wx.TextCtrl(page, -1, text, size=(-1,-1))
        
        issue_label = wx.StaticText(page, -1, "Issue:")
        text = self._article.issue if self._article.issue else ""
        self._issue_value = wx.TextCtrl(page, -1, text, size=(-1,-1))
        
        pages_label = wx.StaticText(page, -1, "Pages:")
        text = self._article.pages if self._article.pages else ""
        self._pages_value = wx.TextCtrl(page, -1, text, size=(-1,-1))
        
        doi_label = wx.StaticText(page, -1, "DOI:")
        text = self._article.doi if self._article.doi else ""
        self._doi_value = wx.TextCtrl(page, -1, text, size=(-1,-1))
        
        pmid_label = wx.StaticText(page, -1, "PMID:")
        text = self._article.pmid if self._article.pmid else ""
        self._pmid_value = wx.TextCtrl(page, -1, text, size=(-1,-1))
        
        # pack items
        grid = wx.GridBagSizer(mwx.GRIDBAG_VSPACE, mwx.GRIDBAG_HSPACE)
        
        grid.Add(title_label, (0,0), flag=wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL)
        grid.Add(self._title_value, (1,0), (1,4), flag=wx.ALIGN_CENTER_VERTICAL|wx.EXPAND)
        
        grid.Add(authors_label, (2,0), flag=wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL)
        grid.Add(self._authors_value, (3,0), (1,4), flag=wx.ALIGN_CENTER_VERTICAL|wx.EXPAND)
        
        grid.Add(journal_label, (4,0), flag=wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL)
        grid.Add(self._journal_combo, (5,0), (1,4), flag=wx.ALIGN_CENTER_VERTICAL|wx.EXPAND)
        
        grid.Add(year_label, (6,0), flag=wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL)
        grid.Add(self._year_value, (7,0), flag=wx.ALIGN_CENTER_VERTICAL|wx.EXPAND)
        
        grid.Add(volume_label, (6,1), flag=wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL)
        grid.Add(self._volume_value, (7,1), flag=wx.ALIGN_CENTER_VERTICAL|wx.EXPAND)
        
        grid.Add(issue_label, (6,2), flag=wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL)
        grid.Add(self._issue_value, (7,2), flag=wx.ALIGN_CENTER_VERTICAL|wx.EXPAND)
        
        grid.Add(pages_label, (6,3), flag=wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL)
        grid.Add(self._pages_value, (7,3), flag=wx.ALIGN_CENTER_VERTICAL|wx.EXPAND)
        
        grid.Add(doi_label, (8,0), (1,2), flag=wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL)
        grid.Add(self._doi_value, (9,0), (1,2), flag=wx.ALIGN_CENTER_VERTICAL|wx.EXPAND)
        
        grid.Add(pmid_label, (8,2), (1,2), flag=wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL)
        grid.Add(self._pmid_value, (9,2), (1,2), flag=wx.ALIGN_CENTER_VERTICAL|wx.EXPAND)
        
        grid.AddGrowableCol(0)
        grid.AddGrowableCol(1)
        grid.AddGrowableCol(2)
        grid.AddGrowableCol(3)
        grid.AddGrowableRow(1)
        grid.AddGrowableRow(3)
        
        # pack items
        page.Sizer = wx.BoxSizer(wx.VERTICAL)
        page.Sizer.Add(grid, 1, wx.ALL | wx.EXPAND, mwx.PANEL_SPACE_MAIN)
        
        return page
    
    
    def _make_abstract_page(self, notebook):
        """Makes abstract page."""
        
        # init page
        page = wx.Panel(notebook)
        
        # init items
        text = self._article.abstract if self._article.abstract else ""
        self._abstract_value = wx.TextCtrl(page, -1, text, size=(400,100), style=wx.TE_MULTILINE)
        
        # pack items
        page.Sizer = wx.BoxSizer(wx.VERTICAL)
        page.Sizer.Add(self._abstract_value, 1, wx.ALL | wx.EXPAND, mwx.PANEL_SPACE_MAIN)
        
        return page
    
    
    def _make_notes_page(self, notebook):
        """Makes notes page."""
        
        # init page
        page = wx.Panel(notebook)
        
        # init items
        text = self._article.notes if self._article.notes else ""
        self._notes_value = wx.TextCtrl(page, -1, text, size=(400,100), style=wx.TE_MULTILINE)
        
        # pack items
        page.Sizer = wx.BoxSizer(wx.VERTICAL)
        page.Sizer.Add(self._notes_value, 1, wx.ALL | wx.EXPAND, mwx.PANEL_SPACE_MAIN)
        
        return page
    
    
    def _get_journal(self, value):
        """Gets journal from string."""
        
        # check value
        if not value:
            return None
        
        # try to get the same journal
        for journal in self._journals:
            if journal.title == value or journal.abbreviation == value:
                return journal
        
        # make new journal
        return core.Journal(title=value, abbreviation=value)
    
    
    def _get_authors(self, value):
        """Gets individual authors from string."""
        
        authors = []
        
        # check value
        if not value:
            return []
        
        # split to individual authors
        for item in value.split(","):
            
            # get authors
            parts = item.strip().split()
            lastname = parts[0]
            firstname = " ".join(x for x in parts[1:])
            
            # append author
            authors.append(core.Author(firstname=firstname, lastname=lastname))
            
            # try to replace by current author
            for author in self._article.authors:
                if author.firstname == firstname and author.lastname == lastname:
                    del authors[-1]
                    authors.append(author)
                    break
        
        return authors
