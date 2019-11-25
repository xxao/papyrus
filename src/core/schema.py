#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

# set database schema version
VERSION = 4


class Schema(object):
    """Provides main library schema initialization and updates mechanism."""
    
    
    def __init__(self, library):
        """Initializes a new instance of library Schema"""
        
        super(Schema, self).__init__()
        
        self._library = library
        self._db = library.db
    
    
    def get_version(self):
        """Gets current database version."""
        
        # check table
        self._db.cursor.execute("SELECT * FROM sqlite_master WHERE type='table' AND name='versions'")
        if not self._db.cursor.fetchone():
            return None
        
        # get version
        self._db.cursor.execute("SELECT MAX(version) FROM versions")
        return self._db.cursor.fetchone()[0]
    
    
    def set_version(self, version, description):
        """Adds database version and info."""
        
        query = """INSERT INTO versions(
                    version,
                    description)
                    VALUES (?,?)"""
        
        self._db.cursor.execute(query, (version, description))
    
    
    def initialize(self):
        """Initializes database schema."""
        
        # make schema query
        query = """
                -- table of versions
                
                CREATE TABLE IF NOT EXISTS versions (
                    version         INTEGER PRIMARY KEY NOT NULL,
                    description     TEXT NOT NULL
                );
                
                -- table of articles
                
                CREATE TABLE IF NOT EXISTS articles (
                    id              INTEGER PRIMARY KEY NOT NULL,
                    key             TEXT UNIQUE NOT NULL,
                    imported        TEXT NOT NULL,
                    doi             TEXT,
                    pmid            TEXT,
                    journal         INTEGER REFERENCES journals ON DELETE SET NULL,
                    year            INTEGER,
                    volume          TEXT,
                    issue           TEXT,
                    pages           TEXT,
                    title           TEXT,
                    abstract        TEXT,
                    notes           TEXT,
                    pdf             INTEGER NOT NULL DEFAULT 0,
                    colour          TEXT,
                    rating          INTEGER NOT NULL DEFAULT 0,
                    deleted         INTEGER NOT NULL DEFAULT 0
                );
                
                -- table of journals
                
                CREATE TABLE IF NOT EXISTS journals (
                    id              INTEGER PRIMARY KEY NOT NULL,
                    title           TEXT NOT NULL,
                    abbreviation    TEXT
                );
                
                -- table of authors
                
                CREATE TABLE IF NOT EXISTS authors (
                    id              INTEGER PRIMARY KEY NOT NULL,
                    shortname       TEXT NOT NULL,
                    lastname        TEXT NOT NULL,
                    firstname       TEXT,
                    initials        TEXT
                );
                
                -- table of labels
                
                CREATE TABLE IF NOT EXISTS labels (
                    id              INTEGER PRIMARY KEY NOT NULL,
                    title           TEXT UNIQUE NOT NULL
                );
                
                -- table of collections
                
                CREATE TABLE IF NOT EXISTS collections (
                    id              INTEGER PRIMARY KEY NOT NULL,
                    title           TEXT NOT NULL,
                    query           TEXT,
                    priority        INTEGER NOT NULL DEFAULT 0,
                    export          INTEGER NOT NULL DEFAULT 0
                );
                
                -- table of links between articles and authors
                
                CREATE TABLE IF NOT EXISTS articles_authors (
                    article         INTEGER NOT NULL REFERENCES articles ON DELETE CASCADE,
                    author          INTEGER NOT NULL REFERENCES authors ON DELETE CASCADE,
                    priority        INTEGER NOT NULL
                );
                
                -- table of links between articles and labels
                
                CREATE TABLE IF NOT EXISTS articles_labels (
                    article         INTEGER NOT NULL REFERENCES articles ON DELETE CASCADE,
                    label           INTEGER NOT NULL REFERENCES labels ON DELETE CASCADE
                );
                
                -- table of links between collections and articles
                
                CREATE TABLE IF NOT EXISTS articles_collections (
                    collection      INTEGER NOT NULL REFERENCES collections ON DELETE CASCADE,
                    article         INTEGER NOT NULL REFERENCES articles ON DELETE CASCADE
                );
                """
        
        # init schema
        self._db.cursor.executescript(query)
        
        # insert version info
        self.set_version(VERSION, "Initial version.")
        
        # commit changes
        self._db.connection.commit()
        
        # return current version
        return VERSION
    
    
    def update(self):
        """Checks current schema and applies available updates."""
        
        # assert connection
        close_db = self._db.connect()
        
        # get current version
        version = self.get_version()
        
        # init new database
        if not version:
            version = self.initialize()
        
        # backup library
        if version != VERSION:
            self._library.backup()
        
        # apply updates
        while version < VERSION:
            
            # check update
            name = "_update_{0}_to_{1}".format(version, version+1)
            update = getattr(self, name, None)
            version += 1
            
            # apply update
            if update is not None:
                update()
        
        # close connection
        if close_db:
            self._db.close()
    
    
    def _update_1_to_2(self):
        """Runs schema update to add notes column to articles."""
        
        # add notes column
        self._db.cursor.execute("ALTER TABLE articles ADD COLUMN notes TEXT")
        
        # set version
        self.set_version(2, "Added notes to articles.")
        
        # commit changes
        self._db.connection.commit()
    
    
    def _update_2_to_3(self):
        """Runs schema update to add export column to collections."""
        
        # add notes column
        self._db.cursor.execute("ALTER TABLE collections ADD COLUMN export INTEGER NOT NULL DEFAULT 0")
        
        # set version
        self.set_version(3, "Added export flag to collections.")
        
        # commit changes
        self._db.connection.commit()
    
    
    def _update_3_to_4(self):
        """Runs schema update to allow empty author's first name."""

        self._db.cursor.execute("PRAGMA writable_schema = 1")
        self._db.cursor.execute("UPDATE SQLITE_MASTER SET SQL = replace(SQL, 'firstname       TEXT NOT NULL', 'firstname       TEXT') WHERE NAME = 'authors'")
        self._db.cursor.execute("PRAGMA writable_schema = 0")
        
        # set version
        self.set_version(4, "Allow empty author's first name.")
        
        # commit changes
        self._db.connection.commit()
        
        # refresh
        self._db.cursor.execute("VACUUM")
