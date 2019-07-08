#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

# import modules
import os.path
import unicodedata

from .entity import Entity
from .journal import Journal
from .author import Author
from .label import Label
from .collection import Collection


# define constants
FORMAT_TAGS = {
    '[PMID]',
    '[DOI]',
    '[DOIX]',
    '[PDF]',
    
    '[TI]',
    '[AB]',
    '[NOTE]',
    '[LB]',
    
    '[JT]',
    '[JA]',
    '[PY]',
    '[VOL]',
    '[ISS]',
    '[PAGE]',
    '[CI]',
    
    '[AU]',
    '[FAU]',
    '[LAU]'}


class Article(Entity):
    """Holds information about article."""
    
    NAME = 'articles'
    
    
    def __init__(self, **attrs):
        """Initializes a new instance of Article."""
        
        self._key = None
        self._imported = None
        
        self._pmid = None
        self._doi = None
        
        self._published = None
        self._submitted = None
        
        self._journal = None
        self._year = None
        self._volume = None
        self._issue = None
        self._pages = None
        
        self._title = None
        self._abstract = None
        self._notes = None
        self._authors = []
        self._labels = []
        self._collections = []
        
        self._has_pdf = False
        self._colour = None
        self._rating = 0
        self._library_path = ""
        self._deleted = False
        
        super(Article, self).__init__(**attrs)
    
    
    def __str__(self):
        """Gets standard string representation."""
        
        # get citation
        citation = "%s " % self.journal.abbreviation if self.journal is not None else ""
        citation += "%s/%s, %s (%s)" % (self.volume, self.issue, self.pages, self.year)
        
        # get authors
        authors = "%s %s" % (self.authors[0].lastname, self.authors[0].initials) if self.authors else ""
        authors += " et al." if len(self.authors) > 1 else ""
        
        return "#%s|%s %s, %s DOI:%s PMID:%s" % (self.dbid, self.key, authors, citation, self.doi, self.pmid)
    
    
    @staticmethod
    def from_db(data):
        """Creates instance from database data."""
        
        return Article(
            dbid = data['id'],
            key = data['key'],
            imported = data['imported'],
            doi = data['doi'],
            pmid = data['pmid'],
            year = data['year'],
            volume = data['volume'],
            issue = data['issue'],
            pages = data['pages'],
            title = data['title'],
            abstract = data['abstract'],
            notes = data['notes'],
            pdf = data['pdf'],
            colour = data['colour'],
            rating = data['rating'],
            deleted = data['deleted'])
    
    
    @property
    def key(self):
        """Gets unique key."""
        
        return self._key
    
    
    @key.setter
    def key(self, value):
        """Sets unique key."""
        
        self._key = str(value) if value else None
    
    
    @property
    def imported(self):
        """Gets time of import as unix timestemp."""
        
        return self._imported
    
    
    @imported.setter
    def imported(self, value):
        """Sets time of import as unix timestemp."""
        
        self._imported = int(value) if value else None
    
    
    @property
    def pmid(self):
        """Gets PubMed id."""
        
        return self._pmid
    
    
    @pmid.setter
    def pmid(self, value):
        """Sets PubMed id."""
        
        self._pmid = str(value) if value else None
    
    
    @property
    def doi(self):
        """Gets article DOI."""
        
        return self._doi
    
    
    @doi.setter
    def doi(self, value):
        """Sets article DOI."""
        
        self._doi = str(value) if value else None
    
    
    @property
    def published(self):
        """Gets publication date."""
        
        return self._published
    
    
    @published.setter
    def published(self, value):
        """Sets publication date."""
        
        self._published = str(value) if value else None
    
    
    @property
    def submitted(self):
        """Gets submitted date."""
        
        return self._submitted
    
    
    @submitted.setter
    def submitted(self, value):
        """Sets submitted date."""
        
        self._submitted = str(value) if value else None
    
    
    @property
    def journal(self):
        """Gets connected journal."""
        
        return self._journal
    
    
    @journal.setter
    def journal(self, value):
        """Sets connected journal."""
        
        if value is not None and not isinstance(value, Journal):
            message = "Journal must be of type Journal! --> '%s'" % type(value)
            raise TypeError(message)
        
        self._journal = value
    
    
    @property
    def year(self):
        """Gets article year."""
        
        return self._year
    
    
    @year.setter
    def year(self, value):
        """Sets article year."""
        
        self._year = int(value) if value else None
    
    
    @property
    def volume(self):
        """Gets article volume."""
        
        return self._volume
    
    
    @volume.setter
    def volume(self, value):
        """Sets article volume."""
        
        self._volume = str(value) if value else None
    
    
    @property
    def issue(self):
        """Gets article issue."""
        
        return self._issue
    
    
    @issue.setter
    def issue(self, value):
        """Sets article issue."""
        
        self._issue = str(value) if value else None
    
    
    @property
    def pages(self):
        """Gets article pages."""
        
        return self._pages
    
    
    @pages.setter
    def pages(self, value):
        """Sets article pages."""
        
        self._pages = str(value) if value else None
    
    
    @property
    def title(self):
        """Gets article title."""
        
        return self._title
    
    
    @title.setter
    def title(self, value):
        """Sets article title."""
        
        self._title = str(value) if value else None
    
    
    @property
    def abstract(self):
        """Gets abstract text."""
        
        return self._abstract
    
    
    @abstract.setter
    def abstract(self, value):
        """Sets abstract text."""
        
        self._abstract = str(value) if value else None
    
    
    @property
    def notes(self):
        """Gets notes text."""
        
        return self._notes
    
    
    @notes.setter
    def notes(self, value):
        """Sets notes text."""
        
        self._notes = str(value) if value else None
    
    
    @property
    def authors(self):
        """Gets connected authors."""
        
        return self._authors
    
    
    @authors.setter
    def authors(self, value):
        """Sets connected authors."""
        
        if value is not None:
            for item in value:
                if not isinstance(item, Author):
                    message = "Author must be of type Author! --> '%s'" % type(item)
                    raise TypeError(message)
        
        self._authors = value if value else []
    
    
    @property
    def labels(self):
        """Gets connected labels."""
        
        return self._labels
    
    
    @labels.setter
    def labels(self, value):
        """Sets connected labels."""
        
        if value is not None:
            for item in value:
                if not isinstance(item, Label):
                    message = "Label must be of type Label! --> '%s'" % type(item)
                    raise TypeError(message)
        
        self._labels = value if value else []
    
    
    @property
    def collections(self):
        """Gets connected collections."""
        
        return self._collections
    
    
    @collections.setter
    def collections(self, value):
        """Sets connected collections."""
        
        if value is not None:
            for item in value:
                if not isinstance(item, Collection):
                    message = "Collection must be of type Collection! --> '%s'" % type(item)
                    raise TypeError(message)
        
        self._collections = value if value else []
    
    
    @property
    def pdf(self):
        """Gets value indicating if PDF should be available."""
        
        return self._has_pdf
    
    
    @pdf.setter
    def pdf(self, value):
        """Sets value indicating if PDF should be available."""
        
        self._has_pdf = bool(value)
    
    
    @property
    def colour(self):
        """Gets colour as hex code."""
        
        return self._colour
    
    
    @colour.setter
    def colour(self, value):
        """Sets colour as hex code."""
        
        self._colour = str(value) if value else None
    
    
    @property
    def rating(self):
        """Gets number of stars for rating."""
        
        return self._rating
    
    
    @rating.setter
    def rating(self, value):
        """Sets number of stars for rating."""
        
        self._rating = int(value) if value else 0
    
    
    @property
    def deleted(self):
        """Gets deleted state."""
        
        return self._deleted
    
    
    @deleted.setter
    def deleted(self, value):
        """Sets deleted state."""
        
        self._deleted = bool(value)
    
    
    @property
    def library_path(self):
        """Gets library path."""
        
        return self._library_path
    
    
    @library_path.setter
    def library_path(self, value):
        """Sets library path."""
        
        self._library_path = str(value) if value else ""
    
    
    @property
    def filename(self):
        """Gets file basename."""
        
        name = ""
        
        # add first author
        if self._authors and self._authors[0].lastname:
            name += "%s_" % self._authors[0].lastname.lower().replace(" ", "_")
        
        # add year
        if self._year:
            name += "%s_" % self._year
        
        # add unique key
        name += self._key
        
        # normalize
        name = unicodedata.normalize('NFKD', name).encode('ascii', 'ignore').decode('ascii')
        
        return name
    
    
    @property
    def pdf_path(self):
        """Gets PDF path."""
        
        # check PDF availability
        if not self._has_pdf:
            return None
        
        # make path
        return os.path.join(self._library_path, "%s.pdf" % self.filename)
    
    
    @property
    def citation(self):
        """Gets citation string."""
        
        citation = ""
        
        if self._journal is not None:
            citation += "%s" % self._journal.abbreviation if self._journal.abbreviation else self._journal.title
        
        if self._volume is not None:
            citation += " %s" % self._volume
        
        if self._issue is not None:
            citation += " (%s)" % self._issue
        
        if citation:
            citation += ","
        
        if self._pages is not None:
            citation += " %s" % self._pages
        
        if self._year is not None:
            citation += " (%s)" % self._year
        
        return citation
    
    
    def format(self, template):
        """Gets article summary according to given format."""
        
        # init values
        values = {t: "" for t in FORMAT_TAGS if t in template}
        
        # add PMID
        if '[PMID]' in values and self.pmid:
            values['[PMID]'] = self.pmid
        
        # add DOI
        if '[DOI]' in values and self.doi:
            values['[DOI]'] = self.doi
        
        # add DOI link
        if '[DOIX]' in values and self.doi:
            values['[DOIX]'] = "http://dx.doi.org/%s" % self.doi
        
        # add title
        if '[TI]' in values and self.title:
            values['[TI]'] = self.title
        
        # add abstract
        if '[AB]' in values and self.abstract:
            values['[AB]'] = self.abstract
        
        # add notes
        if '[NOTE]' in values and self.notes:
            values['[NOTE]'] = self.notes
        
        # add labels
        if '[LB]' in values and self.labels:
            values['[LB]'] = ", ".join(l.title for l in self.labels)
        
        # add journal title
        if '[JT]' in values and self.journal and self.journal.title:
            values['[JT]'] = self.journal.title
        
        # add journal abbreviation
        if '[JA]' in values and self.journal and self.journal.abbreviation:
            values['[JA]'] = self.journal.abbreviation
        
        # add citation
        if '[CI]' in values and self.journal:
            values['[CI]'] = self.citation
        
        # add year
        if '[PY]' in values and self.year:
            values['[PY]'] = str(self.year)
        
        # add volume
        if '[VOL]' in values and self.volume:
            values['[VOL]'] = self.volume
        
        # add issue
        if '[ISS]' in values and self.issue:
            values['[ISS]'] = self.issue
        
        # add pages
        if '[PAGE]' in values and self.pages:
            values['[PAGE]'] = self.pages
        
        # add authors
        if '[AU]' in values and self.authors:
            values['[AU]'] = ", ".join(a.shortname for a in self.authors)
        
        # add first author
        if '[FAU]' in values and self.authors:
            values['[FAU]'] = self.authors[0].shortname
        
        # add last author
        if '[LAU]' in values and self.authors:
            values['[LAU]'] = self.authors[-1].shortname
        
        # add PDF name
        if '[PDF]' in values and self.pdf:
            values['[PDF]'] = self.filename
        
        # init text
        text = template
        
        # replace by safe tags
        for tag in values:
            text = text.replace(tag, "$$%s$$" % tag[1:-1])
        
        # replace tags by values
        for tag, value in values.items():
            text = text.replace("$$%s$$" % tag[1:-1], value)
        
        return text
