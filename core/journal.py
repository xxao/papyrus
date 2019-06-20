#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

# import modules
from .entity import Entity
from .utils import *


class Journal(Entity):
    """Holds information about journal."""
    
    NAME = 'journals'
    
    
    def __init__(self, **attrs):
        """Initializes a new instance of Journal."""
        
        self._title = None
        self._abbreviation = None
        self._count = 0
        
        super(Journal, self).__init__(**attrs)
    
    
    def __str__(self):
        """Gets standard string representation."""
        
        return "#%s %s" % (self.dbid, self.title)
    
    
    @staticmethod
    def from_db(data):
        """Creates instance from database data."""
        
        return Journal(
            dbid = data['id'],
            title = data['title'],
            abbreviation = data['abbreviation'])
    
    
    @property
    def title(self):
        """Gets journal title."""
        
        return self._title
    
    
    @title.setter
    def title(self, value):
        """Sets journal title."""
        
        value = remove_diacritics(value)
        self._title = value if value else None
    
    
    @property
    def abbreviation(self):
        """Gets journal abbreviation."""
        
        return self._abbreviation
    
    
    @abbreviation.setter
    def abbreviation(self, value):
        """Sets journal abbreviation."""
        
        value = remove_diacritics(value)
        
        if value:
            value = value.replace(".", "")
        
        self._abbreviation = value if value else None
    
    
    @property
    def count(self):
        """Gets related articles count."""
        
        return self._count
    
    
    @count.setter
    def count(self, value):
        """Sets related articles count."""
        
        self._count = int(value)
