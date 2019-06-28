#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

# import modules
from .entity import Entity
from .utils import *


class Author(Entity):
    """Holds information about author."""
    
    NAME = 'authors'
    
    
    def __init__(self, **attrs):
        """Initializes a new instance of Author."""
        
        super(Author, self).__init__()
        
        self._lastname = None
        self._firstname = None
        self._initials = None
        self._count = 0
        
        super(Author, self).__init__(**attrs)
        
        # make initials
        if not self._initials and self._firstname:
            self._initials = "".join(x for x in self._firstname if x.isupper())
    
    
    def __str__(self):
        """Gets standard string representation."""
        
        return "#%s %s %s, %s" % (self.dbid, self.lastname, self.firstname, self.initials)
    
    
    @staticmethod
    def from_db(data):
        """Creates instance from database data."""
        
        return Author(
            dbid = data['id'],
            lastname = data['lastname'],
            firstname = data['firstname'],
            initials = data['initials'])
    
    
    @property
    def lastname(self):
        """Gets author last name."""
        
        return self._lastname
    
    
    @lastname.setter
    def lastname(self, value):
        """Sets author last name."""
        
        value = remove_diacritics(value)
        self._lastname = value if value else None
    
    
    @property
    def firstname(self):
        """Gets author first name(s)."""
        
        return self._firstname
    
    
    @firstname.setter
    def firstname(self, value):
        """Sets author first name(s)."""
        
        value = remove_diacritics(value)
        self._firstname = value if value else None
    
    
    @property
    def initials(self):
        """Gets author first names initials."""
        
        return self._initials
    
    
    @initials.setter
    def initials(self, value):
        """Sets author first names initials."""
        
        value = remove_diacritics(value)
        self._initials = value if value else None
    
    
    @property
    def shortname(self):
        """Gets author last name plus initials."""
        
        if self._lastname and self._initials:
            return "%s %s" % (self._lastname, self._initials)
        
        return self._lastname
    
    
    @property
    def longname(self):
        """Gets author last name plus first name."""
        
        if self._lastname and self.firstname:
            return "%s %s" % (self._lastname, self.firstname)
        
        return self._lastname
    
    
    @property
    def count(self):
        """Gets related articles count."""
        
        return self._count
    
    
    @count.setter
    def count(self, value):
        """Sets related articles count."""
        
        self._count = int(value)
