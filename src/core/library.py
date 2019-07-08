#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

# import modules
import random
import time
import os
import os.path

from .database import Database
from .schema import Schema
from .article import Article
from .journal import Journal
from .author import Author
from .label import Label
from .collection import Collection
from .query import Query

# set library folder
LIBRARY_FOLDER = "Library"

# set key generator constants
KEY_CHARS = "abcdefghijklmnopqrst0123456789"
KEY_SIZE = 4


class Library(object):
    """Library class provides initialization and access to papyrus library."""
    
    
    def __init__(self, path, new=False, delete_old=False):
        """
        Initializes a new instance of Library.
        
        Args:
            path: str
                Path to an existing or new SQLite database file.
            
            new: bool
                If set to True, new database will be created. If the file
                already exists it will be deleted or exception raises depending
                on the 'delete_old' parameter.
            
            delete_old: bool
                If set to True and a new file should be created an existing file
                (if any) will be deleted.
        """
        
        super(Library, self).__init__()
        
        # make path absolute
        path = os.path.abspath(path)
        
        # init database file
        self._db = Database(path, new, delete_old)
        
        # check database schema
        schema = Schema(self)
        schema.update()
        
        # ensure archive folder is available
        self._library_path = os.path.join(os.path.dirname(path), LIBRARY_FOLDER)
        if not os.path.isdir(self._library_path):
            os.makedirs(self._library_path)
    
    
    @property
    def db(self):
        """
        Gets library database.
        
        Returns:
            database: Database
                Library database.
        """
        
        return self._db
    
    
    @property
    def db_path(self):
        """
        Gets database path.
        
        Returns:
            path: str
                Path to library database.
        """
        
        return self._db.path
    
    
    @property
    def library_path(self):
        """
        Gets library archive path.
        
        Returns:
            path: str
                Path to PDFs folder.
        """
        
        return self._library_path
    
    
    def query(self, sql, values=[]):
        """
        Queries library by given SQL statement.
        
        Args:
            sql: str
                SQL query.
            
            values: list
                SQL query values.
        
        Returns:
            rows: list
                Fetched rows.
        """
        
        # assert connection
        close_db = self._db.connect()
        
        # execute query
        self._db.cursor.execute(sql, values)
        results = self._db.cursor.fetchall()
        
        # close connection
        if close_db:
            self._db.close()
        
        return results
    
    
    def search(self, query):
        """
        Queries library for specified entity type.
        
        Args:
            query: Query
                Query object.
        
        Returns:
            entities: list requested entities
                List if corresponding items.
        """
        
        # check query type
        if not isinstance(query, Query):
            message = "Query must be of type Query! --> '%s" % type(query)
            raise TypeError(message)
        
        # init buffers
        results = []
        items = []
        
        # make query and values
        sql, values = query.select()
        
        # assert connection
        close_db = self._db.connect()
        
        # execute query
        if sql is not None:
            self._db.cursor.execute(sql, values)
            results = self._db.cursor.fetchall()
        
        # make articles
        if query.entity == Article.NAME:
            for data in results:
                article = Article.from_db(data)
                article.journal = self._get_journal(data['journal'])
                article.authors = self._get_authors(data['id'])
                article.labels = self._get_labels(data['id'])
                article.collections = self._get_collections(data['id'])
                article.library_path = self._library_path
                items.append(article)
        
        # make journals
        elif query.entity == Journal.NAME:
            items = [Journal.from_db(x) for x in results]
        
        # make authors
        elif query.entity == Author.NAME:
            items = [Author.from_db(x) for x in results]
        
        # make labels
        elif query.entity == Label.NAME:
            items = [Label.from_db(x) for x in results]
        
        # make collections
        elif query.entity == Collection.NAME:
            items = [Collection.from_db(x) for x in results]
        
        # unknown entity
        else:
            message = "Unsupported entity for query! --> '%s" % query.entity
            raise KeyError(message)
        
        # close connection
        if close_db:
            self._db.close()
        
        return items
    
    
    def insert(self, item, commit=True):
        """
        Inserts given item into library.
        
        Args:
            item: Article, Journal, Author, Label, Collection
                Item to be inserted into library.
            
            commit: bool
                If set to True changes will be committed.
        """
        
        # assert connection
        close_db = self._db.connect()
        
        # insert article
        if isinstance(item, Article):
            self._insert_article(item)
        
        # insert journal
        elif isinstance(item, Journal):
            self._insert_journal(item)
        
        # insert author
        elif isinstance(item, Author):
            self._insert_author(item)
        
        # insert label
        elif isinstance(item, Label):
            self._insert_label(item)
        
        # insert collection
        elif isinstance(item, Collection):
            self._insert_collection(item)
        
        # unknown item type
        else:
            message = "Unsupported item type to be inserted! --> %s" % type(item)
            raise TypeError(message)
        
        # save changes
        if commit:
            self._db.connection.commit()
        
        # close connection
        if close_db:
            self._db.close()
    
    
    def update(self, item, commit=True):
        """
        Updates given item inside library.
        
        Args:
            item: Article, Journal, Author, Label, Collection
                Item to be updated inside library.
            
            commit: bool
                If set to True changes will be committed.
        """
        
        # check DBID
        if not item.dbid:
            raise AttributeError("Cannot update item without dbid!")
        
        # assert connection
        close_db = self._db.connect()
        
        # update article
        if isinstance(item, Article):
            self._update_article(item)
        
        # update journal
        elif isinstance(item, Journal):
            self._update_journal(item)
        
        # update author
        elif isinstance(item, Author):
            self._update_author(item)
        
        # update label
        elif isinstance(item, Label):
            self._update_label(item)
        
        # update collection
        elif isinstance(item, Collection):
            self._update_collection(item)
        
        # unknown item type
        else:
            message = "Unsupported item type to be updated! --> %s" % type(item)
            raise TypeError(message)
        
        # save changes
        if commit:
            self._db.connection.commit()
        
        # close connection
        if close_db:
            self._db.close()
    
    
    def delete(self, item, commit=True):
        """
        Removes given item from database. DBID of given item is set to None.
        
        Args:
            item: Article, Journal, Author, Label, Collection
                Item to be removed from library.
            
            commit: bool
                If set to True changes will be committed.
        """
        
        # check DBID
        if not item.dbid:
            raise AttributeError("Cannot delete item without dbid!")
        
        # remove article
        if isinstance(item, Article):
            query = "DELETE FROM articles WHERE id = ?"
            self._delete_article_pdf(item)
        
        # remove journal
        elif isinstance(item, Journal):
            query = "DELETE FROM journals WHERE id = ?"
        
        # remove author
        elif isinstance(item, Author):
            query = "DELETE FROM authors WHERE id = ?"
        
        # remove label
        elif isinstance(item, Label):
            query = "DELETE FROM labels WHERE id = ?"
        
        # remove collection
        elif isinstance(item, Collection):
            query = "DELETE FROM collections WHERE id = ?"
        
        # unknown item type
        else:
            message = "Unsupported item type to be deleted! --> %s" % type(item)
            raise TypeError(message)
        
        # assert connection
        close_db = self._db.connect()
        
        # execute query
        self._db.cursor.execute(query, (item.dbid,))
        
        # save changes
        if commit:
            self._db.connection.commit()
        
        # close connection
        if close_db:
            self._db.close()
        
        # reset id
        item.dbid = None
    
    
    def trash(self, articles, trash=True, commit=True):
        """
        Marks given articles as deleted.
        
        Args:
            articles: list of Article
                Articles to be trashed/untrashed.
            
            trash: bool
                Specifies whether articles should be trashed or untrashed.
            
            commit: bool
                If set to True changes will be committed.
        """
        
        # check articles
        if not articles:
            return
        
        # check articles
        for article in articles:
            
            # check type
            if not isinstance(article, Article):
                message = "Article must be of type article! --> '%s" % type(article)
                raise TypeError(message)
            
            # check DBID
            if not article.dbid:
                raise AttributeError("Cannot trash article without dbid!")
        
        # assert connection
        close_db = self._db.connect()
        
        # make query
        query = """UPDATE articles SET deleted = ? WHERE id = ?"""
        value = 1 if trash else 0
        values = [(value, x.dbid) for x in articles]
        
        # execute query
        self._db.cursor.executemany(query, values)
        
        # save changes
        if commit:
            self._db.connection.commit()
        
        # close connection
        if close_db:
            self._db.close()
    
    
    def count(self, item):
        """
        Counts articles related to given item.
        
        Args:
            item: Journal, Author, Label, Collection
                Item for which related articles should be counted.
        
        Returns:
            count: int
                Number of related articles.
        """
        
        # count articles for journal
        if isinstance(item, Journal):
            sql = "SELECT COUNT(*) FROM articles WHERE journal = ?"
            values = (item.dbid,)
        
        # count articles for author
        elif isinstance(item, Author):
            sql = "SELECT COUNT(*) FROM articles_authors WHERE author = ?"
            values = (item.dbid,)
        
        # count articles for label
        elif isinstance(item, Label):
            sql = "SELECT COUNT(*) FROM articles_labels WHERE label = ?"
            values = (item.dbid,)
        
        # count articles for manual collection
        elif isinstance(item, Collection) and not item.query:
            sql = "SELECT COUNT(*) FROM articles_collections WHERE collection = ?"
            values = (item.dbid,)
        
        # count articles for smart collection
        elif isinstance(item, Collection):
            sql, values = Query(item.query, Article.NAME).count()
        
        # unknown item type
        else:
            message = "Unsupported item type to be used for count! --> %s" % type(item)
            raise TypeError(message)
        
        # assert connection
        close_db = self._db.connect()
        
        # execute query
        self._db.cursor.execute(sql, values)
        count = int(self._db.cursor.fetchone()[0])
        
        # close connection
        if close_db:
            self._db.close()
        
        return count
    
    
    def merge(self, items, commit=True):
        """
        Merges given items inside database.
        
        Args:
            items: list of Author or Journal
                Items to be merged.
            
            commit: bool
                If set to True changes will be committed.
        """
        
        # check items
        if not items or len(items) < 2:
            return
        
        # check DBID
        for item in items:
            if not item.dbid:
                raise AttributeError("Cannot merge items without dbid!")
        
        # assert connection
        close_db = self._db.connect()
        
        # merge authors
        if isinstance(items[0], Author):
            self._merge_authors(items)
        
        # merge journals
        elif isinstance(items[0], Journal):
            self._merge_journals(items)
        
        # unknown item type
        else:
            message = "Unknown items type to be merged! --> %s" % type(items[0])
            raise TypeError(message)
        
        # save changes
        if commit:
            self._db.connection.commit()
        
        # close connection
        if close_db:
            self._db.close()
    
    
    def collect(self, articles, collection, insert=True, commit=True):
        """
        Adds or removes given articles to/from specific collection.
        
        Args:
            articles: list of Article
                Articles to be set to collection.
            
            collection: Collection
                Collection to be used.
            
            insert: bool
                Specifies whether articles should be added or removed to/from
                collection. If set to True articles will be inserted, if set to
                False they will be removed.
            
            commit: bool
                If set to True changes will be committed.
        """
        
        # check articles
        if not articles:
            return
        
        # check type
        if not isinstance(collection, Collection):
            message = "Collection must be of type Collection! --> '%s" % type(collection)
            raise TypeError(message)
        
        # check articles
        for article in articles:
            
            # check type
            if not isinstance(article, Article):
                message = "Article must be of type Article! --> '%s" % type(article)
                raise TypeError(message)
            
            # check DBID
            if not article.dbid:
                raise AttributeError("Cannot trash article without dbid!")
        
        # assert connection
        close_db = self._db.connect()
        
        # set values
        values = [(collection.dbid, a.dbid) for a in articles]
        
        # remove current connections
        query = "DELETE FROM articles_collections WHERE collection = ? AND article = ?"
        self._db.cursor.executemany(query, values)
        
        # insert new connections
        if insert:
            query = "INSERT INTO articles_collections (collection, article) VALUES (?,?)"
            self._db.cursor.executemany(query, values)
        
        # save changes
        if commit:
            self._db.connection.commit()
        
        # close connection
        if close_db:
            self._db.close()
    
    
    def label(self, articles, label, insert=True, commit=True):
        """
        Adds or removes specific label to/from given articles.
        
        Args:
            articles: list of Article
                Articles to be (un)labeled.
            
            label: Label
                Label to be used.
            
            insert: bool
                Specifies whether articles should be labeled or unlabeled. If
                set to True articles will be labeled, if set to False they will
                be unlabeled.
            
            commit: bool
                If set to True changes will be committed.
        """
        
        # check articles
        if not articles:
            return
        
        # check type
        if not isinstance(label, Label):
            message = "Label must be of type Label! --> '%s" % type(label)
            raise TypeError(message)
        
        # check articles
        for article in articles:
            
            # check type
            if not isinstance(article, Article):
                message = "Article must be of type Article! --> '%s" % type(article)
                raise TypeError(message)
            
            # check DBID
            if not article.dbid:
                raise AttributeError("Cannot trash article without dbid!")
        
        # assert connection
        close_db = self._db.connect()
        
        # try to find matching label
        if not label.dbid:
            self._match_label(label)
        
        # insert new label
        if not label.dbid and insert:
            self._insert_label(label)
        
        # check label
        if not label.dbid:
            return
        
        # set values
        values = [(label.dbid, a.dbid) for a in articles]
        
        # remove current connections
        query = "DELETE FROM articles_labels WHERE label = ? AND article = ?"
        self._db.cursor.executemany(query, values)
        
        # insert new connections
        if insert:
            query = "INSERT INTO articles_labels (label, article) VALUES (?,?)"
            self._db.cursor.executemany(query, values)
        
        # save changes
        if commit:
            self._db.connection.commit()
        
        # close connection
        if close_db:
            self._db.close()
    
    
    def _insert_article(self, article):
        """Inserts new article."""
        
        # set unique key
        if article.key is None:
            article.key = self._generate_article_key()
        
        # set insertion time
        if article.imported is None:
            article.imported = time.time()
        
        # make article query
        query = """INSERT INTO articles (
                    key,
                    imported,
                    doi,
                    pmid,
                    year,
                    volume,
                    issue,
                    pages,
                    title,
                    abstract,
                    notes,
                    pdf,
                    colour,
                    rating
                    ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)"""
        
        values = (
            article.key,
            article.imported,
            article.doi,
            article.pmid,
            article.year,
            article.volume,
            article.issue,
            article.pages,
            article.title,
            article.abstract,
            article.notes,
            int(article.pdf),
            article.colour,
            article.rating)
        
        # execute article query
        self._db.cursor.execute(query, values)
        
        # set assigned article DBID
        article.dbid = self._db.cursor.lastrowid
        
        # set library path
        article.library_path = self._library_path
        
        # insert journal
        self._insert_article_journal(article, article.journal)
        
        # insert authors
        self._insert_article_authors(article, article.authors)
        
        # insert labels
        self._insert_article_labels(article, article.labels)
    
    
    def _insert_journal(self, journal):
        """Inserts new journal."""
        
        # make query
        query = """INSERT INTO journals (
                    title,
                    abbreviation
                    ) VALUES (?,?)"""
        
        values = (
            journal.title,
            journal.abbreviation)
        
        # execute query
        self._db.cursor.execute(query, values)
        
        # set assigned DBID
        journal.dbid = self._db.cursor.lastrowid
    
    
    def _insert_author(self, author):
        """Inserts new author."""
        
        # make query
        query = """INSERT INTO authors (
                    shortname,
                    lastname,
                    firstname,
                    initials
                    ) VALUES (?,?,?,?)"""
        
        values = (
            author.shortname,
            author.lastname,
            author.firstname,
            author.initials)
        
        # execute query
        self._db.cursor.execute(query, values)
        
        # set assigned DBID
        author.dbid = self._db.cursor.lastrowid
    
    
    def _insert_label(self, label):
        """Inserts new label."""
        
        # make query
        query = """INSERT INTO labels (title) VALUES (?)"""
        values = (label.title,)
        
        # execute query
        self._db.cursor.execute(query, values)
        
        # set assigned DBID
        label.dbid = self._db.cursor.lastrowid
    
    
    def _insert_collection(self, collection):
        """Inserts new collection."""
        
        # make query
        query = """INSERT INTO collections (
                    title,
                    query,
                    priority,
                    export
                    ) VALUES (?,?,?,?)"""
        
        values = (
            collection.title,
            collection.query,
            collection.priority,
            collection.export)
        
        # execute query
        self._db.cursor.execute(query, values)
        
        # set assigned DBID
        collection.dbid = self._db.cursor.lastrowid
    
    
    def _insert_article_journal(self, article, journal):
        """Inserts article journal."""
        
        # check journal
        if journal is None:
            return
        
        # try to find matching journal
        if not journal.dbid:
            self._match_journal(journal)
        
        # insert new journal
        if not journal.dbid:
            self._insert_journal(journal)
        
        # update journal ID for article
        query = "UPDATE articles SET journal = ? WHERE id = ?"
        values = (journal.dbid, article.dbid)
        self._db.cursor.execute(query, values)
    
    
    def _insert_article_authors(self, article, authors):
        """Inserts article authors."""
        
        # delete old links
        self._db.cursor.execute("DELETE FROM articles_authors WHERE article = ?", (article.dbid,))
        
        # check authors
        if not authors:
            return
        
        # init values
        values = []
        
        # match authors or insert new ones
        for i, author in enumerate(authors):
            
            # try to find matching author
            if not author.dbid:
                self._match_author(author)
            
            # insert new author
            if not author.dbid:
                self._insert_author(author)
            
            # append link
            values.append((article.dbid, author.dbid, i))
        
        # insert links
        query = """INSERT INTO articles_authors (
                    article,
                    author,
                    priority
                    ) VALUES (?,?,?)"""
        
        self._db.cursor.executemany(query, values)
    
    
    def _insert_article_labels(self, article, labels):
        """Inserts article labels."""
        
        # delete old links
        self._db.cursor.execute("DELETE FROM articles_labels WHERE article = ?", (article.dbid,))
        
        # check labels
        if not labels:
            return
        
        # init values
        values = []
        
        # match labels or insert new ones
        for label in labels:
            
            # try to find matching label
            if not label.dbid:
                self._match_label(label)
            
            # insert new label
            if not label.dbid:
                self._insert_label(label)
            
            # append link
            values.append((article.dbid, label.dbid))
        
        # insert links
        query = """INSERT INTO articles_labels (
                    article,
                    label
                    ) VALUES (?,?)"""
        
        self._db.cursor.executemany(query, values)
    
    
    def _update_article(self, article):
        """Updates existing article."""
        
        # make article query
        query = """UPDATE articles SET
                    doi = ?,
                    pmid = ?,
                    journal = NULL,
                    year = ?,
                    volume = ?,
                    issue = ?,
                    pages = ?,
                    title = ?,
                    abstract = ?,
                    notes = ?,
                    pdf = ?,
                    colour = ?,
                    rating = ?
                    WHERE id = ?"""
        
        values = (
            article.doi,
            article.pmid,
            article.year,
            article.volume,
            article.issue,
            article.pages,
            article.title,
            article.abstract,
            article.notes,
            int(article.pdf),
            article.colour,
            article.rating,
            article.dbid)
        
        # get stored version of this article
        old_article = self._get_article(article.dbid)
        
        # execute article query
        self._db.cursor.execute(query, values)
        
        # insert journal
        self._insert_article_journal(article, article.journal)
        
        # insert authors
        self._insert_article_authors(article, article.authors)
        
        # insert labels
        self._insert_article_labels(article, article.labels)
        
        # update PDF
        self._update_article_pdf(article, old_article)
    
    
    def _update_journal(self, journal):
        """Updates existing journal."""
        
        # make query
        query = """UPDATE journals SET
                    title = ?,
                    abbreviation = ?
                    WHERE id = ?"""
        
        values = (
            journal.title,
            journal.abbreviation,
            journal.dbid)
        
        # execute query
        self._db.cursor.execute(query, values)
    
    
    def _update_author(self, author):
        """Updates existing author."""
        
        # update articles PDF where this is the first author
        self._update_authors_pdf(author, [author])
        
        # make query
        query = """UPDATE authors SET
                    shortname = ?,
                    lastname = ?,
                    firstname = ?,
                    initials = ?
                    WHERE id = ?"""
        
        values = (
            author.shortname,
            author.lastname,
            author.firstname,
            author.initials,
            author.dbid)
        
        # execute query
        self._db.cursor.execute(query, values)
    
    
    def _update_label(self, label):
        """Updates existing label."""
        
        # make query
        query = """UPDATE labels SET
                    title = ?
                    WHERE id = ?"""
        
        values = (
            label.title,
            label.dbid)
        
        # execute query
        self._db.cursor.execute(query, values)
    
    
    def _update_collection(self, collection):
        """Updates existing collection."""
        
        # make query
        query = """UPDATE collections SET
                    title = ?,
                    query = ?,
                    priority = ?,
                    export = ?
                    WHERE id = ?"""
        
        values = (
            collection.title,
            collection.query,
            collection.priority,
            collection.export,
            collection.dbid)
        
        # execute query
        self._db.cursor.execute(query, values)
    
    
    def _update_article_pdf(self, new_article, old_article):
        """Updates PDF filename according to new author name."""
        
        # get PDF paths
        old_path = old_article.pdf_path
        new_path = new_article.pdf_path
        
        # no change necessary
        if not old_path or old_path == new_path or not os.path.exists(old_path):
            return
        
        # rename or remove old PDF
        if not new_article.pdf:
            try: os.remove(old_path)
            except IOError: pass
        else:
            try: os.rename(old_path, new_path)
            except IOError: pass
    
    
    def _update_authors_pdf(self, new_author, old_authors):
        """Updates PDF filename for articles where the first author is changed."""
        
        # get IDs
        old_ids = [x.dbid for x in old_authors]
        placeholders = ",".join("?" * len(old_ids))
        
        # get articles where the first author will be changed
        query = """SELECT article FROM articles_authors
                    WHERE author IN (%s)
                    AND priority = 0""" % placeholders
        
        self._db.cursor.execute(query, old_ids)
        
        # rename PDFs
        for row in self._db.cursor.fetchall():
            
            # make article
            article = self._get_article(row['article'])
            if not article.pdf:
                
                # get paths
                old_path = article.pdf_path
                article.authors = [new_author]
                new_path = article.pdf_path
                
                # rename file
                if old_path != new_path and os.path.exists(old_path):
                    try: os.rename(old_path, new_path)
                    except IOError: pass
    
    
    def _match_journal(self, journal):
        """Updates attributes by matching journal."""
        
        # prepare conditions and values
        conditions = []
        values = []
        
        if journal.title:
            conditions.append("(LOWER(title) = ? OR title = '' OR title IS NULL)")
            values.append(journal.title.lower())
        
        if journal.abbreviation:
            conditions.append("(LOWER(abbreviation) = ? OR abbreviation = '' OR abbreviation IS NULL)")
            values.append(journal.abbreviation.lower())
        
        # check conditions
        if not conditions:
            return
        
        # get matching item
        query = "SELECT * FROM journals WHERE %s" % " AND ".join(conditions)
        self._db.cursor.execute(query, values)
        data = self._db.cursor.fetchone()
        
        # check matching item
        if not data:
            return
        
        # update attributes
        journal.dbid = data['id']
        
        if data['title']:
            journal.title = data['title']
        
        if data['abbreviation']:
            journal.abbreviation = data['abbreviation']
    
    
    def _match_author(self, author):
        """Updates attributes by matching author."""
        
        # prepare conditions and values
        conditions = []
        values = []
        
        if author.firstname:
            conditions.append("(LOWER(firstname) = ? OR firstname = '' OR firstname IS NULL)")
            values.append(author.firstname.lower())
        
        if author.lastname:
            conditions.append("(LOWER(lastname) = ? OR lastname = '' OR lastname IS NULL)")
            values.append(author.lastname.lower())
        
        if author.initials:
            conditions.append("(LOWER(initials) = ? OR initials = '' OR initials IS NULL)")
            values.append(author.initials.lower())
        
        # check conditions
        if not conditions:
            return
        
        # get matching item
        query = "SELECT * FROM authors WHERE %s" % " AND ".join(conditions)
        self._db.cursor.execute(query, values)
        data = self._db.cursor.fetchone()
        
        # check matching item
        if not data:
            return
        
        # update attributes
        author.dbid = data['id']
        
        if data['firstname']:
            author.firstname = data['firstname']
        
        if data['lastname']:
            author.lastname = data['lastname']
        
        if data['initials']:
            author.initials = data['initials']
    
    
    def _match_label(self, label):
        """Updates attributes by matching label."""
        
        # get matching label
        self._db.cursor.execute("SELECT * FROM labels WHERE LOWER(title) = ?", (label.title.lower(),))
        data = self._db.cursor.fetchone()
        
        # check matching item
        if not data:
            return
        
        # update attributes
        label.dbid = data['id']
        label.title = data['title']
    
    
    def _merge_authors(self, authors):
        """Merges authors into single item. This assumes that given authors are
        the same just the first name is incomplete so the one with the longest
        first name is taken."""
        
        # init master and others
        master = authors[0]
        others = []
        
        # get master by longest name
        for author in authors[1:]:
            if len(author.firstname) > len(master.firstname):
                others.append(master)
                master = author
            else:
                others.append(author)
        
        # get IDs
        master_id = master.dbid
        others_ids = [x.dbid for x in others]
        placeholders = ",".join("?" * len(others))
        
        # update articles PDF where the first author will be changed
        self._update_authors_pdf(master, others)
        
        # replace author links to master authors
        query = """UPDATE articles_authors
                    SET author = ?
                    WHERE author IN (%s)""" % placeholders
        
        self._db.cursor.execute(query, [master_id]+others_ids)
        
        # remove merged authors
        query = """DELETE FROM authors
                    WHERE id IN (%s)""" % placeholders
        
        self._db.cursor.execute(query, others_ids)
    
    
    def _merge_journals(self, journals):
        """Merges journals into single item. This assumes that given journals are
        the same just the abbreviation is incomplete so the one with the longest
        abbreviation is taken."""
        
        # init master and others
        master = journals[0]
        others = []
        
        # get master by longest abbreviation
        for journal in journals[1:]:
            if journal.abbreviation and (not master.abbreviation or len(journal.abbreviation) > len(master.abbreviation)):
                others.append(master)
                master = journal
            else:
                others.append(journal)
        
        # get IDs
        master_id = master.dbid
        others_ids = [x.dbid for x in others]
        placeholders = ",".join("?" * len(others))
        
        # replace journal links to master journal
        query = """UPDATE articles
                    SET journal = ?
                    WHERE journal IN (%s)""" % placeholders
        
        self._db.cursor.execute(query, [master_id]+others_ids)
        
        # remove merged journals
        query = """DELETE FROM journals
                    WHERE id IN (%s)""" % placeholders
        
        self._db.cursor.execute(query, others_ids)
    
    
    def _get_article(self, article_id):
        """Gets article by article id."""
        
        self._db.cursor.execute("SELECT * FROM articles WHERE id = ?", (article_id,))
        data = self._db.cursor.fetchone()
        
        if not data:
            return None
        
        article = Article.from_db(data)
        article.journal = self._get_journal(data['journal'])
        article.authors = self._get_authors(data['id'])
        article.labels = self._get_labels(data['id'])
        article.collections = self._get_collections(data['id'])
        article.library_path = self._library_path
        
        return article
    
    
    def _get_journal(self, journal_id):
        """Gets journal by its id."""
        
        self._db.cursor.execute("SELECT * FROM journals WHERE id = ?", (journal_id,))
        data = self._db.cursor.fetchone()
        
        if not data:
            return None
        
        return Journal.from_db(data)
    
    
    def _get_authors(self, article_id):
        """Gets authors by article id."""
        
        authors = []
        
        query = """SELECT * FROM articles_authors
                    LEFT JOIN authors ON articles_authors.author = authors.id 
                    WHERE articles_authors.article = ?
                    ORDER BY articles_authors.priority"""
        
        self._db.cursor.execute(query, (article_id,))
        
        for data in self._db.cursor.fetchall():
            authors.append(Author.from_db(data))
        
        return authors
    
    
    def _get_labels(self, article_id):
        """Gets labels by article id."""
        
        labels = []
        
        query = """SELECT * FROM articles_labels
                    LEFT JOIN labels ON articles_labels.label = labels.id 
                    WHERE articles_labels.article = ?
                    ORDER BY labels.title"""
        
        self._db.cursor.execute(query, (article_id,))
        
        for data in self._db.cursor.fetchall():
            labels.append(Label.from_db(data))
        
        return labels
    
    
    def _get_collections(self, article_id):
        """Gets manual collections by article id."""
        
        collections = []
        
        query = """SELECT * FROM articles_collections
                    LEFT JOIN collections ON articles_collections.collection = collections.id
                    WHERE articles_collections.article = ?
                    ORDER BY collections.title"""
        
        self._db.cursor.execute(query, (article_id,))
        
        for data in self._db.cursor.fetchall():
            collections.append(Collection.from_db(data))
        
        return collections
    
    
    def _generate_article_key(self):
        """Generates unique article key."""
        
        # generate unique key
        while True:
            
            # generate random key
            key = ''.join(random.SystemRandom().choice(KEY_CHARS) for i in range(KEY_SIZE))
            
            # check key
            self._db.cursor.execute("SELECT id FROM articles WHERE key = ?", (key,))
            if not self._db.cursor.fetchone():
                return key
    
    
    def _delete_article_pdf(self, article):
        """Removes article PDF."""
        
        # get path
        path = article.pdf_path
        
        # delete file
        if path and os.path.exists(path):
            try: os.remove(path)
            except IOError: pass
        
        # disable PDF
        article.pdf = False
