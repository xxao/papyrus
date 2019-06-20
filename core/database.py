#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

# import modules
import codecs
import os.path
import sqlite3 as sqlite


class Database(object):
    """
    Database is a wrapper around SQLite database providing convenient functions
    to open and close connections.
    
    Attributes:
        path: str (read-only)
            Database file path.
        
        connection: sqlite3.Connection or None (read-only)
            SQLite connection.
        
        cursor: sqlite3.Cursor or None (read-only)
            SQLite connection cursor.
    """
    
    
    def __init__(self, path, new=False, delete_old=False):
        """
        Initializes a new instance of Database.
        
        Args:
            path: str
                Path to an existing or new SQLite database file. You can also
                use in-memory database by providing ':memory:' as a path. In
                that case, each time you open a new connection, new database
                will be created. Therefore you should open a connection before
                you provide the database into any tool.
            
            new: bool
                If set to True, new database will be created. If the file
                already exists it will be deleted or exception raises depending
                on the 'delete_old' parameter.
            
            delete_old: bool
                If set to True and a new file should be created an existing file
                (if any) will be deleted.
        """
        
        super(Database, self).__init__()
        
        self._path = path
        self._connection = None
        self._cursor = None
        
        # use in-memory database
        if path == ':memory:':
            return
        
        # check existing database
        file_exists = os.path.exists(path)
        
        # remove old database
        if file_exists and new and delete_old:
            os.remove(path)
        
        # existing database
        elif file_exists and new:
            message = "Specified database already exists! --> '%s'" % path
            raise IOError(message)
        
        # no database found
        elif not file_exists and not new:
            message = "Specified database does not exist! --> '%s'" % path
            raise IOError(message)
        
        # ensure database file exists
        self.connect()
        self.close()
        
        # check format of existing file
        if not new:
            self._check_db_format()
    
    
    @property
    def path(self):
        """
        Gets database path.
        
        Returns:
            path: str
                Database file path.
        """
        
        return self._path
    
    
    @property
    def connection(self):
        """
        Gets database connection.
        
        Returns:
            connection: sqlite3.Connection or None
                SQLite connection.
        """
        
        return self._connection
    
    
    @property
    def cursor(self):
        """
        Gets connection cursor.
        
        Returns:
            cursor: sqlite3.Cursor or None
                SQLite connection cursor.
        """
        
        return self._cursor
    
    
    def connect(self, row_factory=sqlite.Row):
        """
        Opens a database connection.
        
        If connection is already established nothing happens and the return
        value is False to indicate that the connection will probably be closed
        somewhere else. If new connection is established, the return value is
        True to indicate that you should close the connection if it is no longer
        required.
        
        Args:
            row_factory: callable
                A callable that accepts the cursor and the original row as a
                tuple and returns the real result row. 
        
        Returns:
            flag: bool
                Indicates whether a new connection was established.
        """
        
        # establish new connection if necessary
        if self._connection is None:
            
            self._connection = sqlite.connect(self._path)
            self._connection.row_factory = row_factory
            
            self._cursor = self._connection.cursor()
            self._cursor.execute("PRAGMA foreign_keys = ON")
            
            return True
        
        return False
    
    
    def close(self):
        """Closes current database connection if any."""
        
        if self._connection is not None:
            self._connection.close()
        
        self._connection = None
        self._cursor = None
    
    
    def _check_db_format(self):
        """Checks whether database file is valid SQLite database."""
        
        with open(self._path, "r", encoding="Latin1") as f:
            ima = codecs.encode(str.encode(f.read(16)),'hex_codec')
        
        if ima and ima != b"53514c69746520666f726d6174203300":
            message = "Specified file is not a valid SQLite database."
            raise sqlite.Error(message)
