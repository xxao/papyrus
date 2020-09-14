#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

# import modules
import wx

import core
from .. import mwx
from .. labels_view import LabelsList


class ArticlesEditDlg(wx.Dialog):
    """Dialog to edit article."""
    
    
    def __init__(self, parent, article, journals=(), labels=()):
        """Initializes article dialog."""
        
        # init dialog
        wx.Dialog.__init__(self, parent, -1, title="Article", size=(400, -1), style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)
        self.Bind(wx.EVT_PAINT, self._on_paint)
        
        # init buffers
        self._article = article
        self._journals = journals
        self._labels = labels
        
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
        
        # get authors
        if self._authors_value.IsModified() or not self._authors_switch_check.GetValue():
            authors = self._get_authors(self._authors_value.GetValue().strip(), self._authors_switch_check.GetValue())
        
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
        
        # get notes
        if self._notes_value.IsModified():
            notes = self._notes_value.GetValue().strip()
        
        # get rating
        rating = self._rating_choice.GetSelection()
        
        # get colour
        colour = mwx.COLOUR_NAMES[self._colour_choice.GetSelection()]
        colour = mwx.rgb_to_hex(mwx.COLOUR_BULLETS[colour]) if colour != "none" else None
        
        # get labels
        labels = [lb for lb in self._labels if lb.checked]
        
        # update article
        self._article.title = title
        self._article.abstract = abstract
        self._article.authors = authors
        self._article.journal = journal
        self._article.doi = doi
        self._article.pmid = pmid
        self._article.volume = volume
        self._article.issue = issue
        self._article.pages = pages
        self._article.year = year
        self._article.notes = notes
        self._article.rating = rating
        self._article.colour = colour
        self._article.labels = labels
        
        # close dialog
        self.EndModal(wx.ID_OK)
    
    
    def _on_cancel(self, evt=None):
        """Handles cancel button."""
        
        self.EndModal(wx.ID_CANCEL)
    
    
    def _on_labels_search(self, evt=None):
        """Handles labels search."""
        
        # update list
        self._show_labels()
    
    
    def _on_labels_add(self, evt=None):
        """Handles labels add new."""
        
        # get label
        query = self._labels_search.GetValue().strip()
        if not query:
            return
        
        # get same labels
        same = [x for x in self._labels if x.title.lower() == query.lower()]
        
        # add as new label
        if not same:
            
            # init new label
            label = core.Label()
            label.checked = True
            label.title = query
            
            # add label to buffer
            self._labels.append(label)
        
        # mark as checked
        else:
            for label in same:
                label.checked = True
        
        # clean search
        self._labels_search.SetValue("")
        
        # update labels
        self._show_labels()
    
    
    def _make_ui(self):
        """Makes dialog UI."""
        
        # make notebook
        notebook = wx.Notebook(self)
        notebook.AddPage(self._make_info_page(notebook), "Info")
        notebook.AddPage(self._make_abstract_page(notebook), "Abstract")
        notebook.AddPage(self._make_notes_page(notebook), "Notes")
        notebook.AddPage(self._make_labels_page(notebook), "Labels")
        
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
        
        self._authors_switch_check = wx.CheckBox(page, -1, "Assume last name first")
        self._authors_switch_check.SetValue(True)
        self._authors_switch_check.SetToolTip(wx.ToolTip("Lastname Firstname I, Lastname Firstname I"))
        
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
        
        grid.Add(title_label, (0,0), flag=wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL)
        grid.Add(self._title_value, (1,0), (1,4), flag=wx.ALIGN_CENTER_VERTICAL | wx.EXPAND)
        
        grid.Add(authors_label, (2,0), flag=wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL)
        grid.Add(self._authors_value, (3,0), (1,4), flag=wx.ALIGN_CENTER_VERTICAL | wx.EXPAND)
        
        grid.Add(self._authors_switch_check, (4,0), (1,4), flag=wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        
        grid.Add(journal_label, (5,0), flag=wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL)
        grid.Add(self._journal_combo, (6,0), (1,4), flag=wx.ALIGN_CENTER_VERTICAL | wx.EXPAND)
        
        grid.Add(year_label, (7,0), flag=wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL)
        grid.Add(self._year_value, (8,0), flag=wx.ALIGN_CENTER_VERTICAL | wx.EXPAND)
        
        grid.Add(volume_label, (7,1), flag=wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL)
        grid.Add(self._volume_value, (8,1), flag=wx.ALIGN_CENTER_VERTICAL | wx.EXPAND)
        
        grid.Add(issue_label, (7,2), flag=wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL)
        grid.Add(self._issue_value, (8,2), flag=wx.ALIGN_CENTER_VERTICAL | wx.EXPAND)
        
        grid.Add(pages_label, (7,3), flag=wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL)
        grid.Add(self._pages_value, (8,3), flag=wx.ALIGN_CENTER_VERTICAL | wx.EXPAND)
        
        grid.Add(doi_label, (9,0), (1,2), flag=wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL)
        grid.Add(self._doi_value, (10,0), (1,2), flag=wx.ALIGN_CENTER_VERTICAL | wx.EXPAND)
        
        grid.Add(pmid_label, (9,2), (1,2), flag=wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL)
        grid.Add(self._pmid_value, (10,2), (1,2), flag=wx.ALIGN_CENTER_VERTICAL | wx.EXPAND)
        
        grid.AddGrowableCol(0)
        grid.AddGrowableCol(1)
        grid.AddGrowableCol(2)
        grid.AddGrowableCol(3)
        grid.AddGrowableRow(1)
        grid.AddGrowableRow(3)
        
        # add to page
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
        
        # add to page
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
        
        rating_label = wx.StaticText(page, -1, "Rating:")
        choices = [n.title() for n in mwx.RATING_NAMES]
        self._rating_choice = wx.Choice(page, -1, choices=choices, size=(200,-1))
        self._rating_choice.SetSelection(self._article.rating)
        
        colour_label = wx.StaticText(page, -1, "Color:")
        choices = [n.title() for n in mwx.COLOUR_NAMES]
        self._colour_choice = wx.Choice(page, -1, choices=choices, size=(200,-1))
        colours = [mwx.rgb_to_hex(mwx.COLOUR_BULLETS[n]) for n in mwx.COLOUR_NAMES]
        self._colour_choice.SetSelection(colours.index(self._article.colour) if self._article.colour else 0)
        
        # pack items
        grid = wx.GridBagSizer(mwx.GRIDBAG_VSPACE, mwx.GRIDBAG_HSPACE)
        
        grid.Add(self._notes_value, (0,0), (1,2), flag=wx.ALIGN_CENTER_VERTICAL | wx.EXPAND)
        
        grid.Add(rating_label, (1,0), flag=wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL)
        grid.Add(self._rating_choice, (2,0), flag=wx.ALIGN_CENTER_VERTICAL | wx.EXPAND)
        
        grid.Add(colour_label, (1,1), flag=wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL)
        grid.Add(self._colour_choice, (2,1), flag=wx.ALIGN_CENTER_VERTICAL | wx.EXPAND)
        
        grid.AddGrowableCol(0)
        grid.AddGrowableCol(1)
        grid.AddGrowableRow(0)
        
        # add to page
        page.Sizer = wx.BoxSizer(wx.VERTICAL)
        page.Sizer.Add(grid, 1, wx.ALL | wx.EXPAND, mwx.PANEL_SPACE_MAIN)
        
        return page
    
    
    def _make_labels_page(self, notebook):
        """Makes labels page."""
        
        # init page
        page = wx.Panel(notebook)
        
        # init items
        self._labels_search = wx.TextCtrl(page, -1, "", style=wx.TE_PROCESS_ENTER)
        self._labels_add_butt = wx.Button(page, label="Add", size=(70, -1))
        self._labels_list = LabelsList(page, style=wx.NO_FULL_REPAINT_ON_RESIZE | wx.SIMPLE_BORDER)
        
        # set checked labels
        article_labels = set(lb.dbid for lb in self._article.labels)
        for label in self._labels:
            label.checked = label.dbid in article_labels
        
        # show available labels
        self._show_labels()
        
        # bind events
        self._labels_search.Bind(wx.EVT_TEXT, self._on_labels_search)
        self._labels_search.Bind(wx.EVT_TEXT_ENTER, self._on_labels_add)
        self._labels_add_butt.Bind(wx.EVT_BUTTON, self._on_labels_add)
        
        # pack items
        search_sizer = wx.BoxSizer(wx.HORIZONTAL)
        search_sizer.Add(self._labels_search, 1, wx.ALIGN_CENTER_VERTICAL)
        search_sizer.Add(self._labels_add_butt, 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT | wx.EXPAND, 10)
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(search_sizer, 0, wx.ALIGN_CENTER_VERTICAL | wx.EXPAND)
        sizer.Add(self._labels_list, 1, wx.ALIGN_CENTER_VERTICAL | wx.TOP | wx.EXPAND, 10)
        
        # pack items
        page.Sizer = wx.BoxSizer(wx.VERTICAL)
        page.Sizer.Add(sizer, 1, wx.ALL | wx.EXPAND, mwx.PANEL_SPACE_MAIN)
        
        return page
    
    
    def _show_labels(self):
        """Shows labels according to current search."""
        
        # get search text
        query = self._labels_search.GetValue().strip().lower()
        
        # get all labels
        labels = self._labels[:]
        
        # apply search filter
        if query:
            
            buff = []
            words = query.split()
            
            for label in labels:
                title = label.title.lower()
                if all(map(lambda w: w in title, words)):
                    buff.append(label)
            
            labels = buff
        
        # show labels
        self._labels_list.SetLabels(labels)
    
    
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
    
    
    def _get_authors(self, value, last_first):
        """Gets individual authors from string."""
        
        authors = []
        
        # check value
        if not value:
            return []
        
        # split to individual authors
        for item in value.split(","):
            
            # get authors
            parts = item.strip().split()
            if last_first:
                lastname = parts[0]
                firstname = " ".join(x for x in parts[1:])
            else:
                lastname = parts[-1]
                firstname = " ".join(x for x in parts[0:-1])
            
            # append author
            authors.append(core.Author(firstname=firstname, lastname=lastname))
            
            # try to replace by current author
            for author in self._article.authors:
                if author.firstname == firstname and author.lastname == lastname:
                    del authors[-1]
                    authors.append(author)
                    break
        
        return authors
