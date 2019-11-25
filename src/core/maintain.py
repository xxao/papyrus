#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

# import modules
from .library import Library
from .query import Query
from .journal import Journal


def remove_duplicate_journals(library, backup=True, verbose=False):
    """Finds and merges all duplicate journals (by abbreviation)."""
    
    # check library
    if isinstance(library, str):
        library = Library(library, new=False, delete_old=False)
    
    # backup library
    if backup:
        library.backup()
    
    # get all journals
    journals = library.search(Query("", Journal.NAME))
    
    # group by abbreviation
    groups = {}
    for journal in journals:
        if journal.abbreviation not in groups:
            groups[journal.abbreviation] = []
        groups[journal.abbreviation].append(journal)
    
    # merge journals
    for group in groups.values():
        if len(group) > 1:
            if verbose:
                print("Merging: ", group)
            library.merge(group)
