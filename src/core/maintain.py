#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

# import modules
from .library import Library
from .query import Query
from .journal import Journal
from .author import Author


def merge_duplicate_journals(library, backup=True, verbose=False):
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
        
        # check group
        if len(group) < 2:
            continue
        
        # init master and others
        master = group[0]
        others = []
        
        # get master by longest abbreviation
        for journal in groups[1:]:
            if journal.abbreviation and (not master.abbreviation or len(journal.abbreviation) > len(master.abbreviation)):
                others.append(master)
                master = journal
            else:
                others.append(journal)
        
        # merge group
        if verbose:
            print("Merging: %s to %s" % (others, master))
        library.merge(master, others)


def merge_duplicate_authors(library, backup=True, verbose=False):
    """Finds suspected author duplicates."""
    
    # check library
    if isinstance(library, str):
        library = Library(library, new=False, delete_old=False)
    
    # backup library
    if backup:
        library.backup()
    
    # get all authors
    authors = library.search(Query("", Author.NAME))
    
    # group by last name
    groups = {}
    for author in authors:
        if author.lastname not in groups:
            groups[author.lastname] = []
        groups[author.lastname].append(author)
    
    # find duplicates
    duplicates = {}
    for group in groups.values():
        
        if len(group) < 2:
            continue
        
        # longest name as master
        master = max(group, key=lambda a: len(a.firstname))
        duplicates[master] = []
        
        # get suspected duplicates
        for author in group:
            
            # check master
            if author.dbid == master.dbid:
                continue
            
            # check initials
            if author.initials[0] != master.initials[0]:
                continue
            
            # check first name
            if not master.firstname.startswith(author.firstname.split()[0]):
                continue
            
            # add as duplicate
            duplicates[master].append(author)
        
        # check duplicates
        if not duplicates[master]:
            del duplicates[master]
    
    # merge authors
    for master, others in duplicates.items():
        
        if verbose:
            print("Merging: %s to %s" % (others, master))
        
        library.merge(master, others)
