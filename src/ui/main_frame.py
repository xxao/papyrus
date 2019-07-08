#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

# import modules
import sys
import traceback
import os
import os.path
import threading
import time
import re
import shutil
import subprocess
import webbrowser
import wx
import wx.aui

import core

from . import config
from . import mwx
from . import images

from .ids import *
from .hotkeys import ACCELERATORS
from . import events

from .error_dlg import ErrorDlg
from .menu_bar import MenuBar
from .bottom_bar import BottomBar
from .articles_view import ArticlesView, ArticlesEditDlg
from .details_view import DetailsView
from .pdf_view import PDFView
from .collections_view import CollectionsView, CollectionsEditDlg
from .repository_view import RepositoryView
from .labels_view import LabelsView, LabelsEditDlg

# compile patterns
DETAILS_URL_PATTERN = re.compile("papyrus:\?(?P<parameter>[a-z]+)=(?P<value>.+)")
EXPORT_PATTERN = re.compile("^_export_.+\.txt$")


class MainFrame(wx.Frame):
    """Main application frame."""
    
    
    def __init__(self, parent, id):
        """Initializes main application frame."""
        
        # init frame
        wx.Frame.__init__(self, parent, -1, "Papyrus", size=(800, 500), style=wx.DEFAULT_FRAME_STYLE | wx.NO_FULL_REPAINT_ON_RESIZE)
        
        # init error handler
        sys.excepthook = self._on_error
        
        # init library
        self._library = None
        
        # set icon
        icons = wx.IconBundle()
        icons.AddIcon(images.APP_ICON_16)
        icons.AddIcon(images.APP_ICON_32)
        icons.AddIcon(images.APP_ICON_48)
        icons.AddIcon(images.APP_ICON_128)
        icons.AddIcon(images.APP_ICON_256)
        self.SetIcons(icons)
        
        # init menu bar
        self._menu_bar = MenuBar()
        if config.SETTINGS['menu_bar_enabled']:
            self.SetMenuBar(self._menu_bar)
        
        # init main ui
        self._make_ui()
        
        # set size
        self.SetSize((config.SETTINGS['app_width'], config.SETTINGS['app_height']))
        self.SetMinSize((800, 500))
        
        # maximize
        if config.SETTINGS['app_maximized']:
            print(config.SETTINGS)
            self.Maximize()
        
        # bind events
        self._bind_events()
        
        # set hot keys
        self.SetAcceleratorTable(wx.AcceleratorTable(ACCELERATORS))
        
        # show frame
        self.Layout()
        self.Centre(wx.BOTH)
        self.Show(True)
    
    
    def OnClose(self, evt):
        """Closes the app window."""
        
        try:
            
            # save config
            self._update_config()
            config.save()
            
            # export collections
            self._on_collections_export()
        
        except:
            pass
        
        # safe destroy
        self.AUIManager.UnInit()
        self.Destroy()
    
    
    def OpenDocuments(self, paths):
        """Opens specified documents."""
        
        libraries = []
        pdfs = []
        
        # check paths
        for path in paths:
            
            # get absolute path
            path = os.path.abspath(path)
           
            # get extension
            dirname, filename = os.path.split(path)
            basename, extension = os.path.splitext(filename)
            extension = extension.lower()
            
            # get pdf
            if extension == '.pdf':
                pdfs.append(path)
            
            # get libraries
            elif extension == '.papyrus':
                libraries.append(path)
        
        # open library
        if libraries:
            
            try:
                self._library = core.Library(libraries[0])
                self._menu_bar.SetLibrary(self._library)
                self._collections_view.SetLibrary(self._library)
                self._articles_view.SetMasterQuery("0[TRASH]")
                self._articles_view.SetLibrary(self._library)
                self.SetTitle("Papyrus - %s" % self._library.db_path)
                config.SETTINGS['library'] = self._library.db_path
            
            except IOError:
                wx.Bell()
                dlg = mwx.MessageDlg(self, -1, "Cannot open the library.", "Specified file may not exist or is not a valid library format.", "Error")
                dlg.ShowModal()
                dlg.Destroy()
                return
        
        # check PDFs
        if not pdfs:
            return
        
        # check library
        if self._library is None:
            wx.Bell()
            dlg = mwx.MessageDlg(self, -1, "No library opened.", "Before you can import any article please open an existing library\nor create a new one.", "Error")
            dlg.ShowModal()
            dlg.Destroy()
            return
        
        # import PDFs
        self._pdf_import_async(pdfs)
    
    
    def _on_error(self, type, value, tb):
        """Catches exception and shows error report."""
        
        # get exception
        exception = traceback.format_exception(type, value, tb)
        exception = '\n'.join(exception)
        
        # show error message
        dlg = ErrorDlg(self, exception)
        dlg.ShowModal()
        dlg.Destroy()
    
    
    def _on_documents_dropped(self, evt):
        """Handles dropped documents."""
        
        evt.Skip()
        wx.CallAfter(self.OpenDocuments, evt.GetFiles())
    
    
    def _on_library_new(self, evt=None):
        """Handles new library create event."""
        
        # raise save dialog
        wildcard = "Papyrus library format|*.papyrus"
        dlg = wx.FileDialog(self, "New Papyrus Library", "", "library.papyrus", wildcard=wildcard, style=wx.FD_SAVE)
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            dlg.Destroy()
        else:
            dlg.Destroy()
            return
        
        # init library
        try:
            core.Library(path, new=True)
        except:
            wx.Bell()
            dlg = mwx.MessageDlg(self, -1, "Cannot create the library.", "Please check access permissions.", "Error")
            dlg.ShowModal()
            dlg.Destroy()
            return
        
        # open library
        self.OpenDocuments([path])
    
    
    def _on_library_open(self, evt=None):
        """Handles open library event."""
        
        # raise open dialog
        wildcard = "Papyrus library format|*.papyrus"
        dlg = wx.FileDialog(self, "Open Papyrus Library", "", "", wildcard=wildcard, style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            dlg.Destroy()
        else:
            dlg.Destroy()
            return
        
        # open library
        self.OpenDocuments([path])
    
    
    def _on_collections_selection_changed(self, evt=None):
        """Handles collection selection changed event."""
        
        # get selected collection
        collection = self._collections_view.GetSelectedCollection()
        
        # update menu bar
        self._menu_bar.SetCollection(collection)
        
        # check collection
        if collection is None:
            return
        
        # init query
        query = ""
        
        # handle system collections
        if collection.group == "system":
            query = collection.query
        
        # handle manual collection
        elif collection.group == "custom" and not collection.query:
            query = "%s[COLLECTIONID]" % collection.dbid
        
        # handle smart collection
        elif collection.group == "custom" and collection.query:
            query = collection.query
        
        # handle labels collection
        elif collection.group == "labels":
            query = collection.query
        
        # set queries to articles view
        self._articles_view.SetQuery(None)
        self._articles_view.SetMasterQuery(query)
        
        # show articles
        self._articles_view.ShowAllArticles()
    
    
    def _on_collections_item_activated(self, evt=None):
        """Handles collection item activated event."""
        
        # get selected collection
        collection = self._collections_view.GetSelectedCollection()
        
        # invalid collection
        if collection is None:
            return
        
        # edit custom collection
        elif collection.group == "custom":
            self._on_collections_edit()
        
        # edit label
        elif collection.group == "labels":
            self._on_labels_edit()
    
    
    def _on_collections_new(self, evt):
        """Creates new collection."""
        
        # init new collection
        collection = core.Collection(group="custom")
        
        # get used titles
        collections = self._library.search(core.Query("", core.Collection.NAME))
        used_titles = [x.title for x in collections]
        
        # get collection type
        is_smart = evt.GetId() == ID_COLLECTIONS_NEW_SMART
        
        # raise dialog
        dlg = CollectionsEditDlg(self, collection, used_titles=used_titles, is_smart=is_smart)
        response = dlg.ShowModal()
        dlg.Destroy()
        
        # check response
        if response != wx.ID_OK:
            return
        
        # insert collection into library
        self._library.insert(collection)
        
        # include selected articles
        if evt.GetId() == ID_COLLECTIONS_NEW_FROM_SELECTION:
            articles = self._articles_view.GetSelectedArticles()
            self._library.collect(articles, collection)
        
        # refresh collections view
        self._collections_view.UpdateManualCollections()
        self._collections_view.UpdateSmartCollections()
        
        # refresh articles view
        self._articles_view.ShowArticles()
    
    
    def _on_collections_edit(self, evt=None):
        """Edits selected collection."""
        
        # get selected collection
        collection = self._collections_view.GetSelectedCollection()
        
        # check collection
        if collection is None or collection.group != "custom":
            return
        
        # get used titles
        collections = self._library.search(core.Query("", core.Collection.NAME))
        used_titles = [x.title for x in collections if x.dbid != collection.dbid]
        
        # raise dialog
        dlg = CollectionsEditDlg(self, collection, used_titles=used_titles, is_smart=bool(collection.query))
        response = dlg.ShowModal()
        dlg.Destroy()
        
        # check response
        if response != wx.ID_OK:
            return
        
        # update library
        self._library.update(collection)
        
        # refresh collections view
        self._collections_view.UpdateManualCollections()
        self._collections_view.UpdateSmartCollections()
        
        # refresh articles view
        self._articles_view.ShowArticles()
    
    
    def _on_collections_delete(self, evt=None):
        """Deletes selected collection."""
        
        # get selected collection
        collection = self._collections_view.GetSelectedCollection()
        
        # check collection
        if collection is None or collection.group != "custom":
            return
        
        # confirm delete
        cancel_butt = mwx.DlgButton(wx.ID_CANCEL, "Cancel", size=(80,-1), default=False, space=15)
        delete_butt = mwx.DlgButton(wx.ID_OK, "Delete", size=(80,-1), default=True, space=0)
        
        dlg = mwx.MessageDlg(self,
            id = -1,
            title = "Delete Collection",
            message = "Do you really want to delete selected collection?",
            details = "Related articles will not be removed.",
            buttons = [cancel_butt, delete_butt])
        
        response = dlg.ShowModal()
        dlg.Destroy()
        
        # check response
        if response != wx.ID_OK:
            return
        
        # delete collection from database
        self._library.delete(collection)
        
        # refresh collections view
        self._collections_view.UpdateManualCollections()
        self._collections_view.UpdateSmartCollections()
        
        # refresh articles view
        self._articles_view.ShowArticles()
    
    
    def _on_collections_empty_trash(self, evt=None):
        """Permanently deletes all articles in trash."""
        
        # confirm delete
        cancel_butt = mwx.DlgButton(wx.ID_CANCEL, "Cancel", size=(80,-1), default=False, space=15)
        delete_butt = mwx.DlgButton(wx.ID_OK, "Delete All", size=(80,-1), default=True, space=0)
        
        dlg = mwx.MessageDlg(self,
            id = -1,
            title = "Empty Trash",
            message = "Do you really want to permanently delete all\narticles in trash?",
            details = "This operation cannot be undone.",
            buttons = [cancel_butt, delete_butt])
        
        response = dlg.ShowModal()
        dlg.Destroy()
        
        # check response
        if response != wx.ID_OK:
            return
        
        # get articles in trash
        articles = self._library.search(core.Query("1[TRASH]", core.Article.NAME))
        
        # remove articles from library
        for article in articles:
            self._library.delete(article)
        
        # refresh collections view
        self._collections_view.UpdateCounts() 
        
        # refresh articles view
        self._articles_view.ShowArticles()
    
    
    def _on_collections_export(self, evt=None):
        """Exports all marked collections."""
        
        # remove old exports
        for name in os.listdir(self._library.library_path):
            if EXPORT_PATTERN.match(name):
                os.remove(os.path.join(self._library.library_path, name))
        
        # get collections
        collections = self._library.search(core.Query("", core.Collection.NAME))
        collections = [c for c in collections if c.export]
        
        # export collections
        for collection in collections:
            
            # get articles
            query = core.Query("%s[COLLECTIONID]" % collection.dbid, core.Article.NAME)
            articles = self._library.search(query)
            
            # make export
            text = ""
            for article in articles:
                text += article.format("PDF: [PDF]\n[TI]\n[AU]\n[CI]\n\n")
            
            # init filename and path
            filename = "_export_"
            filename += collection.title.replace(" ", "_")
            filename += ".txt"
            path = os.path.join(self._library.library_path, filename)
            
            # save to file
            with open(path, 'w', encoding="utf-8") as export:
                export.write(text)
    
    
    def _on_labels_new(self, evt):
        """Creates new label."""
        
        # init new label
        label = core.Label()
        
        # get used titles
        labels = self._library.search(core.Query("", core.Label.NAME))
        used_titles = [x.title for x in labels]
        
        # raise dialog
        dlg = LabelsEditDlg(self, label, used_titles=used_titles)
        response = dlg.ShowModal()
        dlg.Destroy()
        
        # check response
        if response != wx.ID_OK:
            return
        
        # insert label into library
        self._library.insert(label)
        
        # refresh collections view
        self._collections_view.UpdateLabelsCollections()
    
    
    def _on_labels_edit(self, evt=None):
        """Edits selected label."""
        
        # get selected collection
        collection = self._collections_view.GetSelectedCollection()
        
        # check collection
        if collection is None or collection.group != "labels":
            return
        
        # get label
        label = collection.attachment
        
        # get used titles
        labels = self._library.search(core.Query("", core.Label.NAME))
        used_titles = [x.title for x in labels if x.dbid != label.dbid]
        
        # raise dialog
        dlg = LabelsEditDlg(self, label, used_titles=used_titles)
        response = dlg.ShowModal()
        dlg.Destroy()
        
        # check response
        if response != wx.ID_OK:
            return
        
        # update library
        self._library.update(label)
        
        # refresh collections view
        self._collections_view.UpdateLabelsCollections() 
        self._collections_view.UpdateCounts()
        
        # refresh articles view
        self._articles_view.ShowArticles()
    
    
    def _on_labels_delete(self, evt=None):
        """Deletes selected label."""
        
        # get selected collection
        collection = self._collections_view.GetSelectedCollection()
        
        # check collection
        if collection is None or collection.group != "labels":
            return
        
        # confirm delete
        cancel_butt = mwx.DlgButton(wx.ID_CANCEL, "Cancel", size=(80,-1), default=False, space=15)
        delete_butt = mwx.DlgButton(wx.ID_OK, "Delete", size=(80,-1), default=True, space=0)
        
        dlg = mwx.MessageDlg(self,
            id = -1,
            title = "Delete Label",
            message = "Do you really want to delete selected label?",
            details = "Related articles will not be removed.",
            buttons = [cancel_butt, delete_butt])
        
        response = dlg.ShowModal()
        dlg.Destroy()
        
        # check response
        if response != wx.ID_OK:
            return
        
        # delete label
        self._library.delete(collection.attachment)
        
        # refresh collections view
        self._collections_view.UpdateLabelsCollections()
        self._collections_view.UpdateCounts()
        
        # refresh articles view
        self._articles_view.ShowArticles()
    
    
    def _on_articles_set(self, evt=None):
        """Handles articles set event."""
        
        # get articles
        articles = self._articles_view.GetArticles()
        
        # init label
        label = "1 article found" if len(articles) == 1 else "%s articles found" % len(articles)
        
        # add selected collection to label
        collection = self._collections_view.GetSelectedCollection()
        if collection is not None and collection.title:
            label = "%s in [%s]" % (label, collection.title)
        
        # update bottom bar
        self._bottom_bar.SetLabel(label)
    
    
    def _on_articles_selection_changed(self, evt=None):
        """Handles articles selection changed event."""
        
        # get selected articles
        articles = self._articles_view.GetSelectedArticles()

        # update menu bar
        self._menu_bar.SetArticles(articles)
        
        # none or multiple articles selected
        if len(articles) != 1:
            self._details_view.SetArticle(None)
            self._pdf_view.SetArticle(None)
            return
        
        # get article
        article = articles[0]
        
        # get authors articles count
        for author in article.authors:
            author.count = self._library.count(author)
        
        # show article details
        self._details_view.SetArticle(article)
        self._pdf_view.SetArticle(article)
    
    
    def _on_articles_item_activated(self, evt=None):
        """Opens article PDF or website."""
        
        # get selected articles
        articles = self._articles_view.GetSelectedArticles()
        if not articles:
            return
        
        # open article PDF or website
        if articles[0].pdf:
            self._on_articles_open_pdf()
        elif articles[0].doi:
            self._on_articles_open_doi()
        elif articles[0].pmid:
            self._on_articles_open_pmid()
    
    
    def _on_articles_search(self, evt=None):
        """Set focus to search field."""
        
        # set focus
        self._articles_view.SetFocusToQuery()
    
    
    def _on_articles_open_pdf(self, evt=None):
        """Opens article PDF in default viewer."""
        
        # get selected articles
        articles = self._articles_view.GetSelectedArticles()
        if not articles:
            return
        
        # init statuses
        unavailable = []
        
        # open PDFs
        for article in articles:
            if article.pdf:
                
                # get path
                path = article.pdf_path
                
                # check path
                if not os.path.exists(path):
                    unavailable.append(path)
                    continue
                
                # try to open PDF
                try:
                    if wx.Platform == '__WXMSW__':
                        os.startfile(path)
                    else:
                        try: subprocess.Popen(['xdg-open', path])
                        except: subprocess.Popen(['open', path])
                except:
                    wx.Bell()
                    dlg = mwx.MessageDlg(self, -1, "Unable to open article's PDF.", "Please make sure you have an application associated\nwith a PDF format.")
                    dlg.ShowModal()
                    dlg.Destroy()
                    return
        
        # some PDFs are missing
        if unavailable:
            dlg = mwx.MessageDlg(self, -1, "Some of the PDFs are not available.", "\n".join(unavailable))
            dlg.ShowModal()
            dlg.Destroy()
    
    
    def _on_articles_open_doi(self, evt=None):
        """Opens article website in default browser."""
        
        # get selected articles
        articles = self._articles_view.GetSelectedArticles()
        if not articles:
            return
        
        # open web
        for article in articles:
            if article.doi:
                link = "https://dx.doi.org/%s" % article.doi
                try: webbrowser.open(link, autoraise=1)
                except: pass
    
    
    def _on_articles_open_pmid(self, evt=None):
        """Opens article PubMed page in default browser."""
        
        # get selected articles
        articles = self._articles_view.GetSelectedArticles()
        if not articles:
            return
        
        # open web
        for article in articles:
            if article.pmid:
                link = "https://ncbi.nlm.nih.gov/pubmed/%s" % article.pmid
                try: webbrowser.open(link, autoraise=1)
                except: pass
    
    
    def _on_articles_reveal_pdf(self, evt=None, path=None):
        """Reveals article PDF in default file viewer."""
        
        # get path from selection
        if not path:
            
            # get selected articles
            articles = self._articles_view.GetSelectedArticles()
            if not articles:
                return
            
            # get PDF path
            path = articles[0].pdf_path
        
        # check path
        if not path or not os.path.exists(path):
            wx.Bell()
            dlg = mwx.MessageDlg(self, -1, "PDF file is not available.", path)
            dlg.ShowModal()
            dlg.Destroy()
            return
        
        # try to reveal PDF
        try:
            if wx.Platform == '__WXMAC__':
                subprocess.Popen(["open", "-R", path])
            elif wx.Platform == '__WXMSW__':
                subprocess.Popen('explorer /select, "%s"' % path)
            else:
                pass
        except:
            pass
    
    
    def _on_articles_copy_citation(self, evt=None):
        """Copies article citation into clipboard."""
        
        # get selected articles
        articles = self._articles_view.GetSelectedArticles()
        if not articles:
            return
        
        # format citations
        text = ""
        for article in articles:
            text += article.format("[TI]\n[AU]\n[CI]\n[DOIX]\n\n")
        
        # make text object for data
        obj = wx.TextDataObject()
        obj.SetText(text.strip())
        
        # paste to clipboard
        if wx.TheClipboard.Open():
            wx.TheClipboard.SetData(obj)
            wx.TheClipboard.Close()
    
    
    def _on_articles_copy_summary(self, evt=None):
        """Copies article summary into clipboard."""
        
        # get selected articles
        articles = self._articles_view.GetSelectedArticles()
        if not articles:
            return
        
        # format citations
        text = ""
        for article in articles:
            text += article.format("[TI]\n[AU]\n[CI]\n[DOIX]\n\n[AB]\n\n")
        
        # make text object for data
        obj = wx.TextDataObject()
        obj.SetText(text.strip())
        
        # paste to clipboard
        if wx.TheClipboard.Open():
            wx.TheClipboard.SetData(obj)
            wx.TheClipboard.Close()
    
    
    def _on_articles_copy_link(self, evt=None):
        """Copies article link into clipboard."""
        
        # get selected articles
        articles = self._articles_view.GetSelectedArticles()
        if not articles:
            return
        
        # format links
        text = ""
        for article in articles:
            if article.doi:
                text += "http://dx.doi.org/%s\n" % article.doi
        
        # make text object for data
        obj = wx.TextDataObject()
        obj.SetText(text.strip())
        
        # paste to clipboard
        if wx.TheClipboard.Open():
            wx.TheClipboard.SetData(obj)
            wx.TheClipboard.Close()
    
    
    def _on_articles_import(self, evt=None):
        """Imports articles PDFs."""
        
        # raise open dialog
        wildcard =  "Adobe PDF Files (*.pdf)|*.pdf"
        dlg = wx.FileDialog(self, "Import PDFs", "", "", wildcard=wildcard, style=wx.FD_OPEN|wx.FD_MULTIPLE|wx.FD_FILE_MUST_EXIST)
        if dlg.ShowModal() == wx.ID_OK:
            paths = dlg.GetPaths()
            dlg.Destroy()
        else:
            dlg.Destroy()
            return
        
        # import PDFs
        self.OpenDocuments(paths)
    
    
    def _on_articles_new(self, evt=None):
        """Creates a new blank article."""
        
        # init article
        article = core.Article()
        
        # get available journals
        journals = self._library.search(core.Query("", core.Journal.NAME))
        
        # raise edit dialog
        dlg = ArticlesEditDlg(self, article, journals)
        response = dlg.ShowModal()
        dlg.Destroy()
        
        # quit if canceled
        if response != wx.ID_OK:
            return
        
        # insert into library
        self._library.insert(article)
        
        # refresh collections view
        self._collections_view.UpdateCounts()
        
        # refresh articles view
        self._articles_view.ShowArticles()
        self._articles_view.SetSelectedArticles([article])
    
    
    def _on_articles_edit(self, evt=None):
        """Edits selected article."""
        
        # get selected articles
        articles = self._articles_view.GetSelectedArticles()
        if not articles or len(articles) > 1:
            return
        
        # select article
        article = articles[0]
        
        # get available journals
        journals = self._library.search(core.Query("", core.Journal.NAME))
        
        # raise edit dialog
        dlg = ArticlesEditDlg(self, article, journals)
        response = dlg.ShowModal()
        dlg.Destroy()
        
        # quit if canceled
        if response != wx.ID_OK:
            return
        
        # update library
        self._library.update(article)
        
        # refresh collections view
        self._collections_view.UpdateCounts()
        
        # refresh articles view
        self._articles_view.ShowArticles()
        self._articles_view.SetSelectedArticles([article])
    
    
    def _on_articles_delete(self, evt=None):
        """Removes selected articles from library."""
        
        # get selected articles
        articles = self._articles_view.GetSelectedArticles()
        if not articles:
            return
        
        # confirm delete
        cancel_butt = mwx.DlgButton(wx.ID_CANCEL, "Cancel", size=(80,-1), default=False, space=15)
        delete_butt = mwx.DlgButton(wx.ID_OK, "Delete", size=(80,-1), default=True, space=0)
        
        dlg = mwx.MessageDlg(self,
            id = -1,
            title = "Delete Articles",
            message = "Do you really want to permanently delete\nselected articles?",
            details = "This operation cannot be undone.",
            buttons = [cancel_butt, delete_butt])
        
        response = dlg.ShowModal()
        dlg.Destroy()
        
        # quit if canceled
        if response != wx.ID_OK:
            return
        
        # remove articles from library
        for article in articles:
            self._library.delete(article)
        
        # refresh collections view
        self._collections_view.UpdateCounts() 
        
        # refresh articles view
        self._articles_view.ShowArticles()
    
    
    def _on_articles_trash(self, evt=None):
        """Marks selected articles as deleted."""
        
        # get selected articles
        articles = self._articles_view.GetSelectedArticles()
        if not articles:
            return
        
        # update library
        self._library.trash(articles, True)
        
        # refresh collections view
        self._collections_view.UpdateCounts() 
        
        # refresh articles view
        self._articles_view.ShowArticles()
    
    
    def _on_articles_restore(self, evt=None):
        """Marks selected articles as not deleted."""
        
        # get selected articles
        articles = self._articles_view.GetSelectedArticles()
        if not articles:
            return
        
        # update library
        self._library.trash(articles, False)
        
        # refresh collections view
        self._collections_view.UpdateCounts() 
        
        # refresh articles view
        self._articles_view.ShowArticles()
    
    
    def _on_articles_rating(self, evt=None, rating=None):
        """Sets new rating to selected articles."""
        
        # get selected articles
        articles = self._articles_view.GetSelectedArticles()
        if not articles:
            return
        
        # get rating from event
        if evt is not None:
            evt_id = evt.GetId()
            
            if evt_id == ID_ARTICLES_RATING_0:
                rating = 0
            elif evt_id == ID_ARTICLES_RATING_1:
                rating = 1
            elif evt_id == ID_ARTICLES_RATING_2:
                rating = 2
            elif evt_id == ID_ARTICLES_RATING_3:
                rating = 3
            elif evt_id == ID_ARTICLES_RATING_4:
                rating = 4
            elif evt_id == ID_ARTICLES_RATING_5:
                rating = 5
            else:
                return
        
        # check rating
        if rating is None:
            return
        
        # set rating and update library
        for article in articles:
            article.rating = rating
            self._library.update(article)
        
        # refresh collections view
        self._collections_view.UpdateCounts() 
        
        # refresh articles view
        self._articles_view.ShowArticles()
        
        # re-select article
        if len(articles) == 1:
            self._articles_view.SetSelectedArticles([articles[0]])
    
    
    def _on_articles_colour(self, evt=None, colour=None):
        """Sets new colour to selected articles."""
        
        # get selected articles
        articles = self._articles_view.GetSelectedArticles()
        if not articles:
            return
        
        # get colour from event
        if evt is not None:
            evt_id = evt.GetId()
            
            if evt_id == ID_ARTICLES_COLOUR_GRAY:
                colour = mwx.COLOUR_BULLET_GRAY
            elif evt_id == ID_ARTICLES_COLOUR_RED:
                colour = mwx.COLOUR_BULLET_RED
            elif evt_id == ID_ARTICLES_COLOUR_ORANGE:
                colour = mwx.COLOUR_BULLET_ORANGE
            elif evt_id == ID_ARTICLES_COLOUR_YELLOW:
                colour = mwx.COLOUR_BULLET_YELLOW
            elif evt_id == ID_ARTICLES_COLOUR_GREEN:
                colour = mwx.COLOUR_BULLET_GREEN
            elif evt_id == ID_ARTICLES_COLOUR_BLUE:
                colour = mwx.COLOUR_BULLET_BLUE
            elif evt_id == ID_ARTICLES_COLOUR_PURPLE:
                colour = mwx.COLOUR_BULLET_PURPLE
            else:
                return
        
        # remove gray
        if colour == mwx.COLOUR_BULLET_GRAY:
            colour = None
        
        # set colour and update library
        for article in articles:
            article.colour = mwx.rgb_to_hex(colour) if colour else None
            self._library.update(article)
        
        # refresh collections view
        self._collections_view.UpdateCounts() 
        
        # refresh articles view
        self._articles_view.ShowArticles()
        
        # re-select article
        if len(articles) == 1:
            self._articles_view.SetSelectedArticles([articles[0]])
    
    
    def _on_articles_labels(self, evt=None):
        """Sets new labels to selected articles."""
        
        # get selected articles
        articles = self._articles_view.GetSelectedArticles()
        if not articles:
            return
        
        # get available labels
        labels = self._library.search(core.Query("", core.Label.NAME))
        
        # set checked value
        for label in labels:
            label.checked = all(label.dbid in (y.dbid for y in x.labels) for x in articles) 
        
        # set labels
        dlg = LabelsView(self, articles, labels)
        response = dlg.ShowModal()
        dlg.Destroy()
        
        # check response
        if response != wx.ID_OK:
            return
        
        # update library
        for article in articles:
            self._library.update(article)
        
        # refresh collections view
        self._collections_view.UpdateLabelsCollections()
        self._collections_view.UpdateCounts() 
        
        # refresh articles view
        self._articles_view.ShowArticles()
        
        # re-select article
        if len(articles) == 1:
            self._articles_view.SetSelectedArticles([articles[0]])
    
    
    def _on_articles_match(self, evt=None):
        """Finds and updates article by on-line match."""
        
        # get selected articles
        articles = self._articles_view.GetSelectedArticles()
        if not articles:
            return
        
        # select master article
        article = articles[0]
        
        # raise repository search dialog
        dlg = RepositoryView(self, self._library, article=article)
        response = dlg.ShowModal()
        matches = dlg.GetSelectedArticles()
        dlg.Destroy()
        
        # check response
        if response != wx.ID_OK or not matches:
            return
        
        # get match
        match = matches[0]
        
        # update article attributes
        if match.doi:
            article.doi = match.doi
        if match.pmid:
            article.pmid = match.pmid
        if match.year:
            article.year = match.year
        if match.volume:
            article.volume = match.volume
        if match.issue:
            article.issue = match.issue
        if match.pages:
            article.pages = match.pages
        if match.title:
            article.title = match.title
        if match.abstract:
            article.abstract = match.abstract
        if match.journal:
            article.journal = match.journal
        if match.authors:
            article.authors = match.authors
        
        # update library
        self._library.update(article)
        
        # refresh collections view
        self._collections_view.UpdateCounts() 
        
        # refresh articles view
        self._articles_view.ShowArticles()
        self._articles_view.SetSelectedArticles([article])
    
    
    def _on_articles_update(self, evt=None):
        """Updates articles by on-line match."""
        
        # get selected articles with PubMed ID
        articles = self._articles_view.GetSelectedArticles()
        articles = [a for a in articles if a.pmid is not None]
        if not articles:
            return
        
        # update articles by PubMed
        self._articles_update_async(articles)
        
        # refresh collections view
        self._collections_view.UpdateLabelsCollections()
        self._collections_view.UpdateCounts()
        
        # refresh articles view
        self._articles_view.ShowArticles()
        
        # re-select article
        if len(articles) == 1:
            self._articles_view.SetSelectedArticles([articles[0]])
    
    
    def _on_articles_attach_pdf(self, evt=None):
        """Attaches PDF to selected article."""
        
        # get selected articles
        articles = self._articles_view.GetSelectedArticles()
        if not articles:
            return
        
        # select master article
        article = articles[0]
        
        # raise open dialog
        wildcard = "Adobe PDF File (*.pdf)|*.pdf"
        dlg = wx.FileDialog(self, "Attach PDF", "", "", wildcard=wildcard, style=wx.FD_OPEN|wx.FD_FILE_MUST_EXIST)
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            dlg.Destroy()
        else:
            dlg.Destroy()
            return
        
        # set PDF to article
        article.pdf = True
        
        # copy PDF into library folder
        shutil.copy(path, article.pdf_path)
        
        # update library
        self._library.update(article)
        
        # refresh collections view
        self._collections_view.UpdateCounts() 
        
        # refresh articles view
        self._articles_view.ShowArticles()
        self._articles_view.SetSelectedArticles([article])
    
    
    def _on_articles_to_collection(self, evt):
        """Adds or removes articles to/from manual collection."""
        
        # get selected articles
        articles = self._articles_view.GetSelectedArticles()
        if not articles:
            return
        
        # set direction
        insert = not evt.collection_status
        
        # create collection
        collection = core.Collection(dbid=evt.collection_dbid)
        
        # set articles collection
        self._library.collect(articles, collection, insert)
        
        # refresh collections view
        self._collections_view.UpdateCounts()
        
        # refresh articles view
        self._articles_view.ShowArticles()
    
    
    def _on_articles_dropped_to_trash(self, evt):
        """Removes articles dropped to trash collection."""
        
        # get articles
        articles = [core.Article(dbid=i) for i in evt.articles_dbids]
        
        # update library
        self._library.trash(articles, True)
        
        # refresh collections view
        self._collections_view.UpdateCounts()
        
        # refresh articles view
        self._articles_view.ShowArticles()
    
    
    def _on_articles_dropped_to_collection(self, evt):
        """Adds articles to dropped manual collection."""
        
        # get articles
        articles = [core.Article(dbid=i) for i in evt.articles_dbids]
        
        # create collection
        collection = core.Collection(dbid=evt.collection_dbid)
        
        # set articles collection
        self._library.collect(articles, collection, True)
        
        # refresh collections view
        self._collections_view.UpdateCounts()
        
        # refresh articles view
        self._articles_view.ShowArticles()
    
    
    def _on_articles_dropped_to_label(self, evt):
        
        # get articles
        articles = [core.Article(dbid=i) for i in evt.articles_dbids]
        
        # create label
        label = core.Label(title=evt.label_title)
        
        # set articles label
        self._library.label(articles, label, True)
        
        # refresh collections view
        self._collections_view.UpdateCounts()
        
        # refresh articles view
        self._articles_view.ShowArticles()
    
    
    def _on_details_navigating(self, evt):
        """Handles details navigating event."""
        
        # get URL
        url = evt.url
        
        # parse URL
        match = DETAILS_URL_PATTERN.search(url)
        if not match:
            return
        
        # get match
        parameter = match.group('parameter')
        value = match.group('value').replace("%20", " ")
        
        # check value
        if not value:
            return
        
        # show article by DOI
        if parameter == 'doi':
            link = "https://dx.doi.org/%s" % value
            try: webbrowser.open(link, autoraise=1)
            except: pass
        
        # show article by PMID (in PubMed)
        elif parameter == 'pmid':
            link = "https://ncbi.nlm.nih.gov/pubmed/%s" % value
            try: webbrowser.open(link, autoraise=1)
            except: pass
        
        # search by author (in PubMed)
        elif parameter == 'author':
            query = "%s[AU]" % value
            self._search_repository(query)
        
        # search by journal (in PubMed)
        elif parameter == 'journal':
            query = "%s[JT]" % value
            self._search_repository(query)
        
        # show articles by author (in library)
        elif parameter == 'authorid':
            query = "%s[AUID]" % value
            self._articles_view.SetMasterQuery(None)
            self._articles_view.SetQuery(query)
            self._articles_view.ShowArticles()
        
        # show articles by label (in library)
        elif parameter == 'labelid':
            query = "%s[LABELID]" % value
            self._articles_view.SetMasterQuery(None)
            self._articles_view.SetQuery(query)
            self._articles_view.ShowArticles()
        
        # show articles by collection (in library)
        elif parameter == 'collectionid':
            query = "%s[COLLECTIONID]" % value
            self._articles_view.SetMasterQuery(None)
            self._articles_view.SetQuery(query)
            self._articles_view.ShowArticles()
        
        # set article rating
        elif parameter == 'rating':
            if value in "012345":
                self._on_articles_rating(rating=int(value))
        
        # set article colour
        elif parameter == 'colour':
            colour = mwx.COLOUR_BULLETS_NAMES.get(value, None)
            if colour is not None:
                self._on_articles_colour(colour=colour)
        
        # reveal PDF file
        elif parameter == 'pdf':
            path = os.path.join(self._library.library_path, value+".pdf")
            self._on_articles_reveal_pdf(path=path)
    
    
    def _on_repository_search(self, evt):
        """Searches on-line repository and imports selected articles."""
        
        # init query
        query = getattr(evt, "query", "")
        
        # get selected articles
        articles = self._articles_view.GetSelectedArticles()
        
        # make requested query from first article
        if articles:
            article = articles[0]
            
            if evt.GetId() == ID_REPOSITORY_RECENT_FIRST_AUTHOR and article.authors:
                query = "%s[AU]" % article.authors[0].shortname
            
            elif evt.GetId() == ID_REPOSITORY_RECENT_LAST_AUTHOR and article.authors:
                query = "%s[AU]" % article.authors[-1].shortname
            
            elif evt.GetId() == ID_REPOSITORY_RECENT_JOURNAL and article.journal:
                query = "%s[JT]" % article.journal.abbreviation
        
        # search repository
        self._search_repository(query)
    
    
    def _on_view_pane(self, evt):
        """Handles view event."""
        
        # get pane
        if evt.GetId() == ID_VIEW_COLLECTIONS:
            pane = self.AUIManager.GetPane(self._collections_view)
        
        elif evt.GetId() == ID_VIEW_PDF:
            pane = self.AUIManager.GetPane(self._pdf_view)
        
        elif evt.GetId() == ID_VIEW_DETAILS:
            pane = self.AUIManager.GetPane(self._details_view)
        
        # toggle pane
        pane.Show(not pane.IsShown())
        
        # update frame
        self.AUIManager.Update()
    
    
    def _make_ui(self):
        """Makes main UI."""
        
        # init main views
        self._collections_view = CollectionsView(self)
        self._articles_view = ArticlesView(self)
        self._details_view = DetailsView(self)
        self._pdf_view = PDFView(self)
        self._bottom_bar = BottomBar(self)
        
        # enable file drop
        target = mwx.FileDropTarget(self.OpenDocuments)
        self._articles_view.SetDropTarget(target)
        
        # manage frames
        self.AUIManager = wx.aui.AuiManager()
        self.AUIManager.SetManagedWindow(self)
        self.AUIManager.SetDockSizeConstraint(0.5, 0.5)
        
        unlock_ui = config.SETTINGS['unlock_ui'] == True
        
        self.AUIManager.AddPane(self._articles_view, wx.aui.AuiPaneInfo().Name("articles").
            CentrePane().MinSize((400,300)).
            Caption("Articles").CaptionVisible(False).PaneBorder(False))
        
        self.AUIManager.AddPane(self._pdf_view, wx.aui.AuiPaneInfo().Name("pdf").
            Layer(1).Bottom().MinSize((200, config.SETTINGS['pdf_view_height'])).BestSize((200, config.SETTINGS['pdf_view_height'])).
            Caption("Article PDF").CaptionVisible(False).CloseButton(False).PaneBorder(False).
            Gripper(unlock_ui).GripperTop())
        
        self.AUIManager.AddPane(self._collections_view, wx.aui.AuiPaneInfo().Name("collections").
            Layer(2).Left().MinSize((200,200)).BestSize((config.SETTINGS['collections_view_width'], 200)).
            Caption("Collections").CaptionVisible(False).CloseButton(False).PaneBorder(False).
            Gripper(unlock_ui).GripperTop())
        
        self.AUIManager.AddPane(self._details_view, wx.aui.AuiPaneInfo().Name("details").
            Layer(2).Right().MinSize((200,200)).BestSize((config.SETTINGS['details_view_width'], 200)).
            Caption("Article Details").CaptionVisible(False).CloseButton(False).PaneBorder(False).
            Gripper(unlock_ui).GripperTop())
        
        self.AUIManager.AddPane(self._bottom_bar, wx.aui.AuiPaneInfo().Name("bottombar").
            Layer(2).Bottom().MinSize((250,mwx.BOTTOM_BAR_HEIGHT)).DockFixed(True).
            CaptionVisible(False).PaneBorder(False).
            Gripper(False))
        
        # disable views
        if not config.SETTINGS['collections_view_enabled']:
            self.AUIManager.GetPane(self._collections_view).Hide()
        
        if not config.SETTINGS['pdf_view_enabled']:
            self.AUIManager.GetPane(self._pdf_view).Hide()
        
        if not config.SETTINGS['details_view_enabled']:
            self.AUIManager.GetPane(self._details_view).Hide()
        
        # set frame manager properties
        art_provider = self.AUIManager.GetArtProvider()
        art_provider.SetColour(wx.aui.AUI_DOCKART_SASH_COLOUR, mwx.SASH_COLOUR)
        art_provider.SetColour(wx.aui.AUI_DOCKART_INACTIVE_CAPTION_COLOUR, mwx.CAPTION_COLOUR)
        art_provider.SetMetric(wx.aui.AUI_DOCKART_SASH_SIZE, mwx.SASH_SIZE)
        art_provider.SetMetric(wx.aui.AUI_DOCKART_GRIPPER_SIZE, mwx.GRIPPER_SIZE)
        art_provider.SetMetric(wx.aui.AUI_DOCKART_GRADIENT_TYPE, wx.aui.AUI_GRADIENT_NONE)
        #art_provider.SetMetric(wx.aui.AUI_DOCKART_DRAW_SASH_GRIP, False)
        self.SetOwnBackgroundColour(mwx.SASH_COLOUR)
        
        # update frame manager
        self.AUIManager.Update()
        
        # reset min size
        self.AUIManager.GetPane(self._pdf_view).MinSize((200,200))
    
    
    def _bind_events(self):
        """Binds all recognizable events."""
        
        # main
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        
        # drag files
        self.DragAcceptFiles(True)
        self.Bind(wx.EVT_DROP_FILES, self._on_documents_dropped)
        
        # collections view events
        self.Bind(events.EVT_COLLECTIONS_SELECTION_CHANGED, self._on_collections_selection_changed)
        self.Bind(events.EVT_COLLECTIONS_ITEM_ACTIVATED, self._on_collections_item_activated)
        
        # articles view events
        self.Bind(events.EVT_ARTICLES_SET, self._on_articles_set)
        self.Bind(events.EVT_ARTICLES_SELECTION_CHANGED, self._on_articles_selection_changed)
        self.Bind(events.EVT_ARTICLES_ITEM_ACTIVATED, self._on_articles_item_activated)
        self.Bind(events.EVT_ARTICLES_TO_COLLECTION, self._on_articles_to_collection)
        self.Bind(events.EVT_ARTICLES_PUBMED, self._on_repository_search)
        
        self.Bind(events.EVT_ARTICLES_DROPPED_TO_TRASH, self._on_articles_dropped_to_trash)
        self.Bind(events.EVT_ARTICLES_DROPPED_TO_COLLECTION, self._on_articles_dropped_to_collection)
        self.Bind(events.EVT_ARTICLES_DROPPED_TO_LABEL, self._on_articles_dropped_to_label)
        
        # details view
        self.Bind(events.EVT_DETAILS_NAVIGATING, self._on_details_navigating)
        
        # menu events
        self.Bind(wx.EVT_MENU, self.OnClose, id=ID_QUIT)
        
        self.Bind(wx.EVT_MENU, self._on_library_new, id=ID_LIBRARY_NEW)
        self.Bind(wx.EVT_MENU, self._on_library_open, id=ID_LIBRARY_OPEN)

        self.Bind(wx.EVT_MENU, self._on_articles_search, id=ID_ARTICLES_SEARCH)
        self.Bind(wx.EVT_MENU, self._on_articles_open_pdf, id=ID_ARTICLES_OPEN_PDF)
        self.Bind(wx.EVT_MENU, self._on_articles_open_doi, id=ID_ARTICLES_OPEN_DOI)
        self.Bind(wx.EVT_MENU, self._on_articles_open_pmid, id=ID_ARTICLES_OPEN_PMID)
        self.Bind(wx.EVT_MENU, self._on_articles_reveal_pdf, id=ID_ARTICLES_REVEAL_PDF)
        self.Bind(wx.EVT_MENU, self._on_articles_copy_citation, id=ID_ARTICLES_COPY_CITATION)
        self.Bind(wx.EVT_MENU, self._on_articles_copy_summary, id=ID_ARTICLES_COPY_SUMMARY)
        self.Bind(wx.EVT_MENU, self._on_articles_copy_link, id=ID_ARTICLES_COPY_LINK)
        self.Bind(wx.EVT_MENU, self._on_articles_new, id=ID_ARTICLES_NEW)
        self.Bind(wx.EVT_MENU, self._on_articles_import, id=ID_ARTICLES_IMPORT)
        self.Bind(wx.EVT_MENU, self._on_articles_edit, id=ID_ARTICLES_EDIT)
        self.Bind(wx.EVT_MENU, self._on_articles_delete, id=ID_ARTICLES_DELETE)
        self.Bind(wx.EVT_MENU, self._on_articles_trash, id=ID_ARTICLES_TRASH)
        self.Bind(wx.EVT_MENU, self._on_articles_restore, id=ID_ARTICLES_RESTORE)
        self.Bind(wx.EVT_MENU, self._on_articles_colour, id=ID_ARTICLES_COLOUR_GRAY)
        self.Bind(wx.EVT_MENU, self._on_articles_colour, id=ID_ARTICLES_COLOUR_RED)
        self.Bind(wx.EVT_MENU, self._on_articles_colour, id=ID_ARTICLES_COLOUR_ORANGE)
        self.Bind(wx.EVT_MENU, self._on_articles_colour, id=ID_ARTICLES_COLOUR_YELLOW)
        self.Bind(wx.EVT_MENU, self._on_articles_colour, id=ID_ARTICLES_COLOUR_GREEN)
        self.Bind(wx.EVT_MENU, self._on_articles_colour, id=ID_ARTICLES_COLOUR_BLUE)
        self.Bind(wx.EVT_MENU, self._on_articles_colour, id=ID_ARTICLES_COLOUR_PURPLE)
        self.Bind(wx.EVT_MENU, self._on_articles_rating, id=ID_ARTICLES_RATING_0)
        self.Bind(wx.EVT_MENU, self._on_articles_rating, id=ID_ARTICLES_RATING_1)
        self.Bind(wx.EVT_MENU, self._on_articles_rating, id=ID_ARTICLES_RATING_2)
        self.Bind(wx.EVT_MENU, self._on_articles_rating, id=ID_ARTICLES_RATING_3)
        self.Bind(wx.EVT_MENU, self._on_articles_rating, id=ID_ARTICLES_RATING_4)
        self.Bind(wx.EVT_MENU, self._on_articles_rating, id=ID_ARTICLES_RATING_5)
        self.Bind(wx.EVT_MENU, self._on_articles_labels, id=ID_ARTICLES_LABELS)
        self.Bind(wx.EVT_MENU, self._on_articles_match, id=ID_ARTICLES_MATCH)
        self.Bind(wx.EVT_MENU, self._on_articles_update, id=ID_ARTICLES_UPDATE)
        self.Bind(wx.EVT_MENU, self._on_articles_attach_pdf, id=ID_ARTICLES_ATTACH_PDF)
        self.Bind(wx.EVT_MENU, self._on_articles_to_collection, id=ID_ARTICLES_COLLECTIONS)
        
        self.Bind(wx.EVT_MENU, self._on_collections_new, id=ID_COLLECTIONS_NEW_MANUAL)
        self.Bind(wx.EVT_MENU, self._on_collections_new, id=ID_COLLECTIONS_NEW_SMART)
        self.Bind(wx.EVT_MENU, self._on_collections_new, id=ID_COLLECTIONS_NEW_FROM_SELECTION)
        self.Bind(wx.EVT_MENU, self._on_collections_edit, id=ID_COLLECTIONS_EDIT)
        self.Bind(wx.EVT_MENU, self._on_collections_delete, id=ID_COLLECTIONS_DELETE)
        self.Bind(wx.EVT_MENU, self._on_collections_empty_trash, id=ID_COLLECTIONS_EMPTY_TRASH)
        
        self.Bind(wx.EVT_MENU, self._on_labels_new, id=ID_LABELS_NEW)
        self.Bind(wx.EVT_MENU, self._on_labels_edit, id=ID_LABELS_EDIT)
        self.Bind(wx.EVT_MENU, self._on_labels_delete, id=ID_LABELS_DELETE)
        
        self.Bind(wx.EVT_MENU, self._on_repository_search, id=ID_REPOSITORY_SEARCH)
        self.Bind(wx.EVT_MENU, self._on_repository_search, id=ID_REPOSITORY_RECENT_FIRST_AUTHOR)
        self.Bind(wx.EVT_MENU, self._on_repository_search, id=ID_REPOSITORY_RECENT_LAST_AUTHOR)
        self.Bind(wx.EVT_MENU, self._on_repository_search, id=ID_REPOSITORY_RECENT_JOURNAL)
        
        self.Bind(wx.EVT_MENU, self._on_view_pane, id=ID_VIEW_COLLECTIONS)
        self.Bind(wx.EVT_MENU, self._on_view_pane, id=ID_VIEW_PDF)
        self.Bind(wx.EVT_MENU, self._on_view_pane, id=ID_VIEW_DETAILS)
    
    
    def _update_config(self):
        """Updates config according to current state."""
        
        # app size
        if self.IsMaximized():
            config.SETTINGS['app_maximized'] = True
        else:
            size = self.GetSize()
            config.SETTINGS['app_width'] = size[0]
            config.SETTINGS['app_height'] = size[1]
            config.SETTINGS['app_maximized'] = False
        
        # panes
        pane = self.AUIManager.GetPane(self._collections_view)
        config.SETTINGS['collections_view_enabled'] = pane.IsShown()
        if pane.IsShown():
            config.SETTINGS['collections_view_width'] = pane.window.GetClientSize()[0]
        
        pane = self.AUIManager.GetPane(self._pdf_view)
        config.SETTINGS['pdf_view_enabled'] = pane.IsShown()
        if pane.IsShown():
            config.SETTINGS['pdf_view_height'] = pane.window.GetClientSize()[1]
        
        pane = self.AUIManager.GetPane(self._details_view)
        config.SETTINGS['details_view_enabled'] = pane.IsShown()
        if pane.IsShown():
            config.SETTINGS['details_view_width'] = pane.window.GetClientSize()[0]
    
    
    def _search_repository(self, query):
        """Searches on-line repository and imports selected articles."""
        
        # raise repository search dialog
        dlg = RepositoryView(self, self._library, query=query)
        response = dlg.ShowModal()
        articles = dlg.GetArticles()
        dlg.Destroy()
        
        # check response
        if response != wx.ID_OK or not articles:
            return
        
        # insert articles
        for article in articles:
            if article.checked:
                self._library.insert(article)
        
        # refresh collections view
        self._collections_view.UpdateCounts() 
        
        # refresh articles view
        self._articles_view.ShowArticles()
    
    
    def _pdf_import_async(self, paths, auto_match=True):
        """Imports specified PDF in another thread."""
        
        # init progress
        self._progress = 0
        self._progress_max = len(paths)
        self._progress_message = "Importing PDFs..."
        
        # show gauge panel
        gauge = mwx.GaugeDlg(self, -1, self._progress_message, "Import")
        gauge.SetRange(self._progress_max)
        gauge.Show()
        
        # start processing
        task = threading.Thread(target=self._pdf_import_task, args=(paths, auto_match))
        task.start()
        
        # update gauge while working
        while task and task.isAlive():
            gauge.SetMessage(self._progress_message)
            gauge.SetRange(self._progress_max)
            gauge.SetValue(self._progress)
            wx.Yield()
            time.sleep(0.1)
        
        # refresh collections view
        self._collections_view.UpdateCounts()
        
        # refresh articles view
        self._articles_view.ShowAllArticles()
        
        # close gauge
        gauge.Close()
    
    
    def _pdf_import_task(self, paths, auto_match):
        """Imports specified PDFs into library."""
        
        # remember articles to match later
        articles_to_match = []
        
        # import PDFs
        for path in paths:
            
            # get filename
            dirname, filename = os.path.split(path)
            
            # init article
            article = core.Article(pdf=True, title=filename)
            
            # get DOI from PDF
            article.doi = core.doi_from_pdf(path)
            
            # insert article into library
            self._library.insert(article)
            
            # copy PDF into library folder
            shutil.copy(path, article.pdf_path)
            
            # (re)move cover page
            if config.SETTINGS['cover_remove_mode']:
                core.move_cover_page(
                    path = article.pdf_path,
                    query = config.SETTINGS['cover_remove_tag'],
                    delete = config.SETTINGS['cover_remove_mode']==2)
            
            # remember articles to match
            if article.doi:
                articles_to_match.append(article)
            
            # increase progress
            self._progress += 1
        
        # skip matching
        if not auto_match:
            return
        
        # reset progress info
        self._progress = 0
        self._progress_max = len(articles_to_match)
        self._progress_message = "Matching PDFs..."
        
        # init PubMed
        pubmed = core.PubMed(exsafe=True)
        
        # try to match article to library or PubMed
        for article in articles_to_match:
            
            # match to existing article
            query = "%s[DOI] AND NOT %s[ID]" % (article.doi, article.dbid)
            matches = self._library.search(core.Query(query, core.Article.NAME))
            
            if len(matches) == 1 and article.doi == matches[0].doi:
                match = matches[0]
                
                # make a copy of imported PDF
                match.pdf = True
                shutil.copy(article.pdf_path, match.pdf_path)
                
                # update library
                self._library.update(match)
                self._library.delete(article)
                
                # increase progress
                self._progress += 1
                continue
            
            # update by matching PubMed article
            query = "%s[DOI]" % article.doi
            matches = pubmed.search(query).articles
            
            if len(matches) == 1 and article.doi == matches[0].doi:
                match = matches[0]
                
                # update article
                article.pmid = match.pmid
                article.year = match.year
                article.volume = match.volume
                article.issue = match.issue
                article.pages = match.pages
                article.title = match.title
                article.abstract = match.abstract
                article.journal = match.journal
                article.authors = match.authors
                
                # update library
                self._library.update(article)
            
            # increase progress
            self._progress += 1
    
    
    def _articles_update_async(self, articles):
        """Updates given articles using PubMed."""
        
        # init progress
        self._progress = 0
        self._progress_max = len(articles)
        self._progress_message = "Updating articles..."
        
        # show gauge panel
        gauge = mwx.GaugeDlg(self, -1, self._progress_message, "Update")
        gauge.SetRange(self._progress_max)
        gauge.Show()
        
        # start processing
        task = threading.Thread(target=self._articles_update_task, args=(articles,))
        task.start()
        
        # update gauge while working
        while task and task.isAlive():
            gauge.SetMessage(self._progress_message)
            gauge.SetRange(self._progress_max)
            gauge.SetValue(self._progress)
            wx.Yield()
            time.sleep(0.1)
        
        # refresh collections view
        self._collections_view.UpdateCounts()
        
        # refresh articles view
        self._articles_view.ShowAllArticles()
        
        # close gauge
        gauge.Close()
    
    
    def _articles_update_task(self, articles):
        """Updates given articles using PubMed."""
        
        # init PubMed
        pubmed = core.PubMed(exsafe=True)
        
        # try to match article to PubMed
        for article in articles:
            
            # find matching PubMed article
            query = "%s[PMID]" % article.pmid
            results = pubmed.search(query)
            matches = results.articles
            
            # update article if single match found
            if len(matches) == 1 and article.pmid == matches[0].pmid:
                match = matches[0]
                
                # update article attributes
                if match.doi:
                    article.doi = match.doi
                if match.year:
                    article.year = match.year
                if match.volume:
                    article.volume = match.volume
                if match.issue:
                    article.issue = match.issue
                if match.pages:
                    article.pages = match.pages
                if match.title:
                    article.title = match.title
                if match.abstract:
                    article.abstract = match.abstract
                if match.journal:
                    article.journal = match.journal
                if match.authors:
                    article.authors = match.authors
                
                # update library
                self._library.update(article)
            
            # increase progress
            self._progress += 1
