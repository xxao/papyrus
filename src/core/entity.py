#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.


class Entity(object):
    """Provides a baseclass for all DB entities."""
    
    NAME = None
    
    
    def __init__(self, dbid=None, **attrs):
        """Initializes a new instance of Entity."""
        
        super(Entity, self).__init__()
        
        self._dbid = int(dbid) if dbid else None
        self._attachment = None
        
        # set given attributes
        for name, value in attrs.items():
            if hasattr(self, name):
                setattr(self, name, value)
            else:
                raise AttributeError("Attribute not found! --> %s" % name)
    
    
    def __repr__(self):
        """Gets debug string representation."""
        
        return "%s(%s)" % (self.__class__.__name__, self.__str__())
    
    @property
    def dbid(self):
        """
        Gets database id.
        
        Returns:
            id: int or None
                Unique database ids.
        """
        
        return self._dbid
    
    
    @dbid.setter
    def dbid(self, value):
        """
        Sets database id.
        
        Args:
            value: int or None
                Unique database ids.
        """
        
        self._dbid = int(value) if value else None
    
    
    @property
    def attachment(self):
        """
        Gets attached data.
        
        Returns:
            data: arbitrary type
                Attached data.
        """
        
        return self._attachment
    
    
    @attachment.setter
    def attachment(self, value):
        """
        Sets attachment data.
        
        Args:
            value: arbitrary type
                Data to be attached.
        """
        
        self._attachment = value
