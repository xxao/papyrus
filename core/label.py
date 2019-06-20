#  Created byMartin.cz
#  Copyright (c) 2014-2019 Martin Strohalm. All rights reserved.

# import modules
from .entity import Entity


class Label(Entity):
    """Holds information about label."""
    
    NAME = 'labels'
    
    
    def __init__(self, **attrs):
        """Initializes a new instance of Label."""
        
        self._title = None
        self._count = 0
        
        super(Label, self).__init__(**attrs)
    
    
    def __str__(self):
        """Gets standard string representation."""
        
        return "#%s %s" % (self.dbid, self.title)
    
    
    @staticmethod
    def from_db(data):
        """Creates instance from database data."""
        
        return Label(
            dbid = data['id'],
            title = data['title'])
    
    
    @property
    def title(self):
        """Gets label title."""
        
        return self._title
    
    
    @title.setter
    def title(self, value):
        """Sets label title."""
        
        self._title = str(value) if value else None
    
    
    @property
    def count(self):
        """Gets related articles count."""
        
        return self._count
    
    
    @count.setter
    def count(self, value):
        """Sets related articles count."""
        
        self._count = int(value)
