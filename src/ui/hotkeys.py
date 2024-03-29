#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

# import modules
import wx
from . ids import *

ACCELERATORS = []

# main
HK_QUIT = "Ctrl+Q"
ACCELERATORS.append((wx.ACCEL_CTRL, ord("Q"), ID_QUIT))

# library
HK_LIBRARY_NEW = "Ctrl+Shift+N"
ACCELERATORS.append((wx.ACCEL_CTRL | wx.ACCEL_SHIFT, ord("N"), ID_LIBRARY_NEW))

HK_LIBRARY_OPEN = "Ctrl+O"
ACCELERATORS.append((wx.ACCEL_CTRL, ord("O"), ID_LIBRARY_OPEN))

HK_LIBRARY_BACKUP = "Ctrl+B"
ACCELERATORS.append((wx.ACCEL_CTRL, ord("B"), ID_LIBRARY_BACKUP))

HK_LIBRARY_ANALYZE = "F5"
ACCELERATORS.append((wx.ACCEL_NORMAL, wx.WXK_F5, ID_LIBRARY_ANALYZE))

# collections
HK_COLLECTIONS_NEW_FROM_SELECTION = "Ctrl+G"
ACCELERATORS.append((wx.ACCEL_CTRL, ord("G"), ID_COLLECTIONS_NEW_FROM_SELECTION))

HK_COLLECTIONS_EMPTY_TRASH = ""
ACCELERATORS.append((wx.ACCEL_CTRL | wx.ACCEL_SHIFT, wx.WXK_BACK, ID_COLLECTIONS_EMPTY_TRASH))

# articles
HK_ARTICLES_SEARCH = "Ctrl+F"
ACCELERATORS.append((wx.ACCEL_CTRL, ord("F"), ID_ARTICLES_SEARCH))

HK_ARTICLES_NEW = "Ctrl+N"
ACCELERATORS.append((wx.ACCEL_CTRL, ord("N"), ID_ARTICLES_NEW))

HK_ARTICLES_IMPORT = "Ctrl+I"
ACCELERATORS.append((wx.ACCEL_CTRL, ord("I"), ID_ARTICLES_IMPORT))

HK_ARTICLES_OPEN_PDF = "Ctrl+V"
ACCELERATORS.append((wx.ACCEL_CTRL, ord("O"), ID_ARTICLES_OPEN_PDF))

HK_ARTICLES_OPEN_DOI = "Ctrl+W"
ACCELERATORS.append((wx.ACCEL_CTRL, ord("W"), ID_ARTICLES_OPEN_DOI))

HK_ARTICLES_OPEN_PMID = "Ctrl+P"
ACCELERATORS.append((wx.ACCEL_CTRL, ord("P"), ID_ARTICLES_OPEN_PMID))

HK_ARTICLES_REVEAL_PDF = "Ctrl+R"
ACCELERATORS.append((wx.ACCEL_CTRL, ord("R"), ID_ARTICLES_REVEAL_PDF))

HK_ARTICLES_COPY_CITATION = "Ctrl+C"
ACCELERATORS.append((wx.ACCEL_CTRL, ord("C"), ID_ARTICLES_COPY_CITATION))

HK_ARTICLES_COPY_SUMMARY = "Ctrl+Shift+C"
ACCELERATORS.append((wx.ACCEL_CTRL | wx.ACCEL_SHIFT, ord("C"), ID_ARTICLES_COPY_SUMMARY))

HK_ARTICLES_COPY_LINK = "Ctrl+Shift+L"
ACCELERATORS.append((wx.ACCEL_CTRL | wx.ACCEL_SHIFT, ord("L"), ID_ARTICLES_COPY_LINK))

HK_ARTICLES_RATING_0 = "Ctrl+0"
ACCELERATORS.append((wx.ACCEL_CTRL, ord("0"), ID_ARTICLES_RATING_0))

HK_ARTICLES_RATING_1 = "Ctrl+1"
ACCELERATORS.append((wx.ACCEL_CTRL, ord("1"), ID_ARTICLES_RATING_1))

HK_ARTICLES_RATING_2 = "Ctrl+2"
ACCELERATORS.append((wx.ACCEL_CTRL, ord("2"), ID_ARTICLES_RATING_2))

HK_ARTICLES_RATING_3 = "Ctrl+3"
ACCELERATORS.append((wx.ACCEL_CTRL, ord("3"), ID_ARTICLES_RATING_3))

HK_ARTICLES_RATING_4 = "Ctrl+4"
ACCELERATORS.append((wx.ACCEL_CTRL, ord("4"), ID_ARTICLES_RATING_4))

HK_ARTICLES_RATING_5 = "Ctrl+5"
ACCELERATORS.append((wx.ACCEL_CTRL, ord("5"), ID_ARTICLES_RATING_5))

HK_ARTICLES_LABELS = "Ctrl+L"
ACCELERATORS.append((wx.ACCEL_CTRL, ord("L"), ID_ARTICLES_LABELS))

HK_ARTICLES_EDIT = "Ctrl+E"
ACCELERATORS.append((wx.ACCEL_CTRL, ord("E"), ID_ARTICLES_EDIT))

HK_ARTICLES_ATTACH_PDF = "Ctrl+Shift+A"
ACCELERATORS.append((wx.ACCEL_CTRL | wx.ACCEL_SHIFT, ord("A"), ID_ARTICLES_ATTACH_PDF))

HK_ARTICLES_MATCH = "Ctrl+M"
ACCELERATORS.append((wx.ACCEL_CTRL, ord("M"), ID_ARTICLES_MATCH))

HK_ARTICLES_UPDATE = "Ctrl+U"
ACCELERATORS.append((wx.ACCEL_CTRL, ord("U"), ID_ARTICLES_UPDATE))

HK_ARTICLES_TRASH = ""
ACCELERATORS.append((wx.ACCEL_CTRL, wx.WXK_BACK, ID_ARTICLES_TRASH))

HK_ARTICLES_RESTORE = "Ctrl+Shift+R"
ACCELERATORS.append((wx.ACCEL_CTRL | wx.ACCEL_SHIFT, ord("R"), ID_ARTICLES_RESTORE))

# repository
HK_REPOSITORY_SEARCH = "Ctrl+Shift+F"
ACCELERATORS.append((wx.ACCEL_CTRL | wx.ACCEL_SHIFT, ord("F"), ID_REPOSITORY_SEARCH))

# authors
HK_AUTHORS_LIST = "F6"
ACCELERATORS.append((wx.ACCEL_NORMAL, wx.WXK_F6, ID_AUTHORS_LIST))

# views
HK_VIEW_COLLECTIONS = "F2"
ACCELERATORS.append((wx.ACCEL_NORMAL, wx.WXK_F2, ID_VIEW_COLLECTIONS))

HK_VIEW_PDF = "F3"
ACCELERATORS.append((wx.ACCEL_NORMAL, wx.WXK_F3, ID_VIEW_PDF))

HK_VIEW_DETAILS = "F4"
ACCELERATORS.append((wx.ACCEL_NORMAL, wx.WXK_F4, ID_VIEW_DETAILS))
