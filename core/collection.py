#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

# import modules
from .entity import Entity


class Collection(Entity):
    """Holds information about collection."""
    
    NAME = 'collections'
    
    
    def __init__(self, **attrs):
        """Initializes a new instance of Collection."""
        
        self._title = None
        self._query = None
        self._priority = 0
        self._export = False
        
        self._group = "custom"
        self._count = 0
        
        super(Collection, self).__init__(**attrs)
    
    
    def __str__(self):
        """Gets standard string representation."""
        
        return "#%s %s %s [%s]" % (self.dbid, self.title, self.query, self.group)
    
    
    @staticmethod
    def from_db(data):
        """Creates instance from database data."""
        
        return Collection(
            dbid = data['id'],
            title = data['title'],
            query = data['query'],
            priority = data['priority'],
            export = data['export'])
    
    
    @property
    def title(self):
        """Gets collection title."""
        
        return self._title
    
    
    @title.setter
    def title(self, value):
        """Sets collection title."""
        
        self._title = str(value) if value else None
    
    
    @property
    def query(self):
        """Gets smart collection query."""
        
        return self._query
    
    
    @query.setter
    def query(self, value):
        """Sets smart collection query."""
        
        self._query = str(value) if value else None
    
    
    @property
    def priority(self):
        """Gets collection priority."""
        
        return self._priority
    
    
    @priority.setter
    def priority(self, value):
        """Sets collection priority."""
        
        self._priority = int(value)
    
    
    @property
    def export(self):
        """Gets collection export flag."""
        
        return self._export
    
    
    @export.setter
    def export(self, value):
        """Sets collection export flag."""
        
        self._export = bool(value)
    
    
    @property
    def group(self):
        """Gets collection group."""
        
        return self._group
    
    
    @group.setter
    def group(self, value):
        """Sets collection group."""
        
        self._group = str(value) if value else None
    
    
    @property
    def count(self):
        """Gets related articles count."""
        
        return self._count
    
    
    @count.setter
    def count(self, value):
        """Sets related articles count."""
        
        self._count = int(value)
