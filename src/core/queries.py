#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

# import modules
import time


def make_articles_query(value, tag=None):
    """Creates sql and values to query database for articles."""
    
    # init buffers
    sqls = []
    values = []
    
    # init value
    value_lower = value.lower()
    value_like = "%%%s%%" % value_lower
    
    # init colours
    colours = {
        "red": "ff6e64",
        "orange": "ffb941",
        "yellow": "f0e646",
        "green": "b4e646",
        "blue": "64afff",
        "purple": "dc8cf0",
        "gray": "c8c8c8"
        }
    
    bools = {
        "0": 0,
        "1": 1,
        "true": 1,
        "True": 1,
        "TRUE": 1,
        "yes": 1,
        "Yes": 1,
        "YES": 1,
        "false": 0,
        "False": 0,
        "FALSE": 0,
        "no": 0,
        "No": 0,
        "NO": 0,
        }
    
    # search by DBID
    if tag == '[ID]':
        sqls.append("(articles.id = ?)""")
        values.append(value)
    
    # search by key
    elif tag == '[KEY]':
        sqls.append("(articles.key = ?)""")
        values.append(value)
    
    # search by PMID
    elif tag == '[PMID]':
        if value == 'NULL':
            sqls.append("(articles.pmid IS NULL)""")
        else:
            sqls.append("(articles.pmid = ?)""")
            values.append(value)
    
    # search by DOI
    elif tag == '[DOI]':
        sqls.append("(LOWER(articles.doi) LIKE ?)""")
        values.append(value_like)
    
    # search by imported date
    elif tag == '[RECENT]':
        try:
            values.append(time.time() - int(value)*60*60*24)
            sqls.append("(articles.imported >= ?)""")
        except ValueError:
            pass
    
    # search by year
    elif tag == '[PY]':
        sqls.append("(articles.year = ?)""")
        values.append(value)
    
    # search by title
    elif tag == '[TI]':
        sqls.append("(LOWER(articles.title) LIKE ?)""")
        values.append(value_like)
    
    # search by abstract
    elif tag == '[AB]':
        sqls.append("(LOWER(articles.abstract) LIKE ?)""")
        values.append(value_like)
    
    # search by notes
    elif tag == '[NOTE]':
        sqls.append("(LOWER(articles.notes) LIKE ?)""")
        values.append(value_like)
    
    # search by colour
    elif tag == '[COLOUR]' or tag == '[COLOR]':
        sqls.append("LOWER(articles.colour) = ?""")
        values.append(colours.get(value_lower, value_lower))
    
    # search by PDF status
    elif tag == '[PDF]':
        sqls.append("articles.pdf = ?""")
        values.append(bools.get(value, 0))
    
    # search by rating
    elif tag == '[RATING]':
        try:
            sqls.append("articles.rating = ?""")
            values.append(int(value))
        except ValueError:
            pass
    
    # search by rating <=
    elif tag == '[RBE]':
        try:
            sqls.append("articles.rating <= ?""")
            values.append(int(value))
        except ValueError:
            pass
    
    # search by rating >=
    elif tag == '[RAE]':
        try:
            sqls.append("articles.rating >= ?""")
            values.append(int(value))
        except ValueError:
            pass
    
    # search by trash status
    elif tag == '[TRASH]':
        sqls.append("articles.deleted = ?""")
        values.append(bools.get(value, 0))
    
    # search by journal title
    elif tag == '[JT]':
        
        sqls.append("""((
            SELECT COUNT(*) FROM journals
            WHERE articles.journal = journals.id
            AND LOWER(journals.title) LIKE ?) != 0)""")
        
        values.append(value_like)
    
    # search by journal abbreviation
    elif tag == '[JA]':
        
        sqls.append("""((
            SELECT COUNT(*) FROM journals
            WHERE articles.journal = journals.id
            AND LOWER(journals.abbreviation) LIKE ?) != 0)""")
        
        values.append(value_like)
    
    # search by author full name
    elif tag == '[AU]':
        
        sqls.append("""((
            SELECT COUNT(*) FROM articles_authors
            LEFT JOIN authors ON articles_authors.author = authors.id
            WHERE articles_authors.article = articles.id
            AND LOWER(authors.shortname) LIKE ?) != 0)""")
        
        values.append(value_like)
    
    # search by author ID
    elif tag == '[AUID]':
        
        sqls.append("""((
            SELECT COUNT(*) FROM articles_authors
            WHERE articles_authors.article = articles.id
            AND articles_authors.author = ?) != 0)""")
        
        values.append(value)
    
    # search by first author
    elif tag == '[FAU]':
        
        sqls.append("""((
            SELECT COUNT(*) FROM articles_authors
            LEFT JOIN authors ON articles_authors.author = authors.id
            WHERE articles_authors.article = articles.id
            AND articles_authors.priority = 0
            AND LOWER(authors.shortname) LIKE ?) != 0)""")
        
        values.append(value_like)
    
    # search by last author
    elif tag == '[LAU]':
        
        sqls.append("""((
            SELECT COUNT(*) FROM (
                SELECT *
                FROM articles_authors
                LEFT JOIN authors ON articles_authors.author = authors.id
                WHERE articles_authors.article = articles.id
                AND LOWER(authors.shortname) LIKE ?
                AND articles_authors.priority = (
                    SELECT MAX(t1.priority) FROM articles_authors t1
                    WHERE t1.article = articles.id)
                )) != 0)""")
        
        values.append(value_like)
    
    # search by labels
    elif tag == '[LB]':
        
        sqls.append("""((
            SELECT COUNT(*) FROM articles_labels
            LEFT JOIN labels ON articles_labels.label = labels.id
            WHERE articles_labels.article = articles.id
            AND LOWER(labels.title) = ?) != 0)""")
        
        values.append(value_lower)
    
    # search by label ID
    elif tag == '[LABELID]':
        
        sqls.append("""((
            SELECT COUNT(*) FROM articles_labels
            WHERE articles_labels.article = articles.id
            AND articles_labels.label = ?) != 0)""")
        
        values.append(value)
    
    # search by collection ID
    elif tag == '[COLLECTIONID]':
        
        sqls.append("""((
            SELECT COUNT(*) FROM articles_collections
            WHERE articles_collections.article = articles.id
            AND articles_collections.collection = ?) != 0)""")
        
        values.append(value)
    
    # search all fields
    else:
        
        sqls.append("""(
            articles.key = ?
            OR articles.pmid = ?
            OR LOWER(articles.doi) = ?
            OR LOWER(articles.title) LIKE ?
            OR LOWER(articles.abstract) LIKE ?
            OR LOWER(articles.notes) LIKE ?
            
            OR (
                SELECT COUNT(*) FROM journals
                WHERE journals.id = articles.journal
                AND (LOWER(journals.title) LIKE ?
                    OR LOWER(journals.abbreviation) LIKE ?)) != 0
            
            OR (
                SELECT COUNT(*) FROM articles_authors
                LEFT JOIN authors ON articles_authors.author = authors.id
                WHERE articles_authors.article = articles.id
                AND LOWER(authors.shortname) LIKE ?) != 0
            
            OR (
                SELECT COUNT(*) FROM articles_labels
                LEFT JOIN labels ON articles_labels.label = labels.id
                WHERE articles_labels.article = articles.id
                AND LOWER(labels.title) LIKE ?) != 0
            )""")
        
        values += [
            value,
            value,
            value_lower,
            value_like,
            value_like,
            value_like,
            value_like,
            value_like,
            value_like,
            value_like]
    
    return sqls, values


def make_journals_query(value, tag=None):
    """Creates sql and values to query database for journals."""
    
    # init buffers
    sqls = []
    values = []
    
    # init value
    value_like = "%%%s%%" % value.lower()
    
    # search by DBID
    if tag == '[ID]':
        sqls.append("(id = ?)""")
        values.append(value)
    
    # search all fields
    else:
        
        sqls.append("""(
            LOWER(title) LIKE ?
            OR LOWER(abbreviation) LIKE ?)""")
        
        values += [
            value_like,
            value_like]
    
    return sqls, values


def make_authors_query(value, tag=None):
    """Creates sql and values to query database for authors."""
    
    # init buffers
    sqls = []
    values = []
    
    # init value
    value_like = "%%%s%%" % value.lower()
    
    # search by DBID
    if tag == '[ID]':
        sqls.append("(id = ?)""")
        values.append(value)
    
    # search all fields
    else:
        
        sqls.append("""(
            LOWER(shortname) LIKE ?
            OR LOWER(lastname) LIKE ?
            OR LOWER(firstname) LIKE ?)""")
        
        values += [
            value_like,
            value_like,
            value_like]
    
    return sqls, values


def make_labels_query(value, tag=None):
    """Creates sql and values to query database for labels."""
    
    # init buffers
    sqls = []
    values = []
    
    # init value
    value_like = "%%%s%%" % value.lower()
    
    # search by DBID
    if tag == '[ID]':
        sqls.append("(id = ?)""")
        values.append(value)
    
    # search all fields
    else:
        sqls.append("(LOWER(title) LIKE ?)")
        values.append(value_like)
    
    return sqls, values


def make_collections_query(value, tag=None):
    """Creates sql and values to query database for collections."""
    
    # init buffers
    sqls = []
    values = []
    
    # init value
    value_like = "%%%s%%" % value.lower()
    
    # search by DBID
    if tag == '[ID]':
        sqls.append("(id = ?)""")
        values.append(value)
    
    # search all fields
    else:
        sqls.append("(LOWER(title) LIKE ?)")
        values.append(value_like)
    
    return sqls, values
