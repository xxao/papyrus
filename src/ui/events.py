#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

# import modules
import wx.lib.newevent

# events from collections view
CollectionsSelectionChangedEvent, EVT_COLLECTIONS_SELECTION_CHANGED = wx.lib.newevent.NewCommandEvent()
CollectionsItemActivatedEvent, EVT_COLLECTIONS_ITEM_ACTIVATED = wx.lib.newevent.NewCommandEvent()
CollectionsItemContextMenuEvent, EVT_COLLECTIONS_ITEM_CONTEXT_MENU = wx.lib.newevent.NewCommandEvent()

# events from articles view
ArticlesSetEvent, EVT_ARTICLES_SET = wx.lib.newevent.NewCommandEvent()
ArticlesQueryChangedEvent, EVT_ARTICLES_QUERY_CHANGED = wx.lib.newevent.NewCommandEvent()
ArticlesPubMedEvent, EVT_ARTICLES_PUBMED = wx.lib.newevent.NewCommandEvent()
ArticlesSelectionChangedEvent, EVT_ARTICLES_SELECTION_CHANGED = wx.lib.newevent.NewCommandEvent()
ArticlesItemActivatedEvent, EVT_ARTICLES_ITEM_ACTIVATED = wx.lib.newevent.NewCommandEvent()
ArticlesItemContextMenuEvent, EVT_ARTICLES_ITEM_CONTEXT_MENU = wx.lib.newevent.NewCommandEvent()
ArticlesToCollectionEvent, EVT_ARTICLES_TO_COLLECTION = wx.lib.newevent.NewCommandEvent()

ArticlesDroppedToTrashEvent, EVT_ARTICLES_DROPPED_TO_TRASH = wx.lib.newevent.NewCommandEvent()
ArticlesDroppedToCollectionEvent, EVT_ARTICLES_DROPPED_TO_COLLECTION = wx.lib.newevent.NewCommandEvent()
ArticlesDroppedToLabelEvent, EVT_ARTICLES_DROPPED_TO_LABEL = wx.lib.newevent.NewCommandEvent()

# events from article details view
DetailsNavigatingEvent, EVT_DETAILS_NAVIGATING = wx.lib.newevent.NewCommandEvent()

# events from repository view
RepositorySelectionChangedEvent, EVT_REPOSITORY_SELECTION_CHANGED = wx.lib.newevent.NewCommandEvent()
RepositoryItemActivatedEvent, EVT_REPOSITORY_ITEM_ACTIVATED = wx.lib.newevent.NewCommandEvent()
RepositoryItemContextMenuEvent, EVT_REPOSITORY_ITEM_CONTEXT_MENU = wx.lib.newevent.NewCommandEvent()
RepositoryItemValueChangedEvent, EVT_REPOSITORY_ITEM_VALUE_CHANGED = wx.lib.newevent.NewCommandEvent()
RepositorySearchEvent, EVT_REPOSITORY_SEARCH = wx.lib.newevent.NewCommandEvent()
RepositoryMoreEvent, EVT_REPOSITORY_MORE = wx.lib.newevent.NewCommandEvent()
RepositoryOkEvent, EVT_REPOSITORY_OK = wx.lib.newevent.NewCommandEvent()

# events from labels view
LabelsNewEvent, EVT_LABELS_NEW = wx.lib.newevent.NewCommandEvent()
LabelsTypeEvent, EVT_LABELS_TYPE = wx.lib.newevent.NewCommandEvent()
LabelsAddEvent, EVT_LABELS_ADD = wx.lib.newevent.NewCommandEvent()
LabelsApplyEvent, EVT_LABELS_APPLY = wx.lib.newevent.NewCommandEvent()
