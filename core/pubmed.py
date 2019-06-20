#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

# import modules
import json
import xml.etree.cElementTree as etree
from urllib.error import URLError

from . import eutils
from .journal import Journal
from .article import Article
from .author import Author


class PubMed(object):
    """Provides basic tools for PubMed search."""
    
    
    def __init__(self, exsafe=False):
        """Initializes a new instance of PubMed."""
        
        super(PubMed, self).__init__()
        self._exsafe = exsafe
    
    
    def search(self, query, **kwargs):
        """Searches for articles according to given query."""
        
        try:
            
            # search
            response = eutils.esearch(db='pubmed', term=query, retmode='JSON', **kwargs)
            results = json.loads(response)['esearchresult']
            
            # get response data
            ids = results['idlist'] if 'idlist' in results else []
            total = int(results['count']) if 'count' in results else 0
            retstart = int(results['retstart']) if 'retstart' in results else 0
            
            # check IDs
            if not ids:
                return PubMedResults(query)
            
            # retrieve articles data
            articles_data = eutils.efetch(db='pubmed', id=','.join(ids), retmode='XML')
            
            # parse articles
            articles = self._parse_articles(articles_data)
            
            return PubMedResults(query, articles, total, retstart)
        
        # error during search
        except URLError as error:
            if self._exsafe:
                return PubMedResults(query, error=error)
            raise
    
    
    def _parse_articles(self, data):
        """Parses articles XML."""
        
        articles = []
        
        # parse XML
        xml = etree.fromstring(data)
        
        # process each article
        for pubmed_article_elm in xml.iter('PubmedArticle'):
            
            # init template
            article = {
                'pmid': None,
                'doi': None,
                'title': None,
                'abstract': None,
                'source': None,
                'authors': None,
            }
            
            # retrieve IDs
            pubmed_data_elm = pubmed_article_elm.find('PubmedData')
            if pubmed_data_elm is not None:
                
                article_id_list_elm = pubmed_data_elm.find('ArticleIdList')
                if article_id_list_elm is not None:
                    
                    for article_id_elm in article_id_list_elm.iter('ArticleId'):
                        id_type = article_id_elm.get('IdType', None)
                        
                        # retrieve DOI
                        if id_type == 'doi':
                            article['doi'] = article_id_elm.text
                        
                        # retrieve PMID
                        elif id_type == 'pubmed':
                            article['pmid'] = article_id_elm.text
            
            # retrieve citation
            medline_citation_elm = pubmed_article_elm.find('MedlineCitation')
            if medline_citation_elm is not None:
                
                # retrieve PMID
                pmid_elm = medline_citation_elm.find('PMID')
                if pmid_elm is not None:
                    article['pmid'] = pmid_elm.text
                
                # retrieve article
                article_elm = medline_citation_elm.find('Article')
                if article_elm is not None:
                    
                    # retrieve title
                    article_title_elm = article_elm.find('ArticleTitle')
                    if article_title_elm is not None:
                        article['title'] = article_title_elm.text
                    
                    # retrieve abstract
                    article['abstract'] = self._retrieve_abstract(article_elm)
                    
                    # retrieve source
                    article['source'] = self._retrieve_source(article_elm)
                    
                    # retrieve authors
                    article['authors'] = self._retrieve_authors(article_elm)
            
            # make article
            articles.append(self._make_article(article))
        
        return articles
    
    
    def _make_article(self, data):
        """Makes article object from raw data."""
        
        # make article
        article = Article(
            pmid = data['pmid'],
            doi = data['doi'],
            year = data['source']['year'],
            volume = data['source']['volume'],
            issue = data['source']['issue'],
            pages = data['source']['pages'],
            title = data['title'],
            abstract = data['abstract'])
        
        # set journal
        article.journal = Journal(
            title = data['source']['title'],
            abbreviation = data['source']['abbreviation'])
        
        # set authors
        for item in data['authors']:
            
            author = Author(
                firstname = item['firstname'],
                lastname = item['lastname'],
                initials = item['initials'])
            
            article.authors.append(author)
        
        return article
    
    
    def _retrieve_abstract(self, article_elm):
        """Retrieves abstract text."""
        
        # get abstract
        abstract_elm = article_elm.find('Abstract')
        if abstract_elm is None:
            return None
        
        # retrieve all parts
        abstract = []
        for abstract_text_elm in abstract_elm.iter('AbstractText'):
            
            # get text
            text = ''.join(abstract_text_elm.itertext())
            
            # add label
            label = abstract_text_elm.get('Label', None)
            if label:
                text = "%s: %s" % (label.title(), text)
            
            # store text
            abstract.append(text)
        
        # concatenate text
        return "\n\n".join(abstract)
    
    
    def _retrieve_source(self, article_elm):
        """Retrieves source info."""
        
        source = {
            'title': None,
            'abbreviation': None,
            'issn': None,
            'year': None,
            'month': None,
            'day': None,
            'volume': None,
            'issue': None,
            'pages': None,
        }
        
        # retrieve pages
        pagination_elm = article_elm.find('Pagination')
        if pagination_elm is not None:
            medline_pgn_elm = pagination_elm.find('MedlinePgn')
            if medline_pgn_elm is not None:
                source['pages'] = medline_pgn_elm.text
        
        # retrieve journal info
        journal_elm = article_elm.find('Journal')
        if journal_elm is not None:
            
            # retrieve title
            title_elm = journal_elm.find('Title')
            if title_elm is not None:
                source['title'] = title_elm.text
            
            # retrieve abbreviation
            abbreviation_elm = journal_elm.find('ISOAbbreviation')
            if abbreviation_elm is not None:
                source['abbreviation'] = abbreviation_elm.text
            
            # retrieve ISSN
            issn_elm = journal_elm.find('ISSN')
            if issn_elm is not None:
                source['issn'] = issn_elm.text
            
            # retrieve article info
            journal_issue_elm = journal_elm.find('JournalIssue')
            if journal_issue_elm is not None:
                
                # retrieve volume
                volume_elm = journal_issue_elm.find('Volume')
                if volume_elm is not None:
                    source['volume'] = volume_elm.text
                
                # retrieve issue
                issue_elm = journal_issue_elm.find('Issue')
                if issue_elm is not None:
                    source['issue'] = issue_elm.text
                
                # retrieve date from journal issue
                pub_date_elm = journal_issue_elm.find('PubDate')
                if pub_date_elm is not None:
                    
                    # retrieve year
                    year_elm = pub_date_elm.find('Year')
                    if year_elm is not None:
                        source['year'] = year_elm.text
                    
                    # retrieve month
                    month_elm = pub_date_elm.find('Month')
                    if month_elm is not None:
                        source['month'] = month_elm.text
                    
                    # retrieve day
                    day_elm = pub_date_elm.find('Day')
                    if day_elm is not None:
                        source['day'] = day_elm.text
        
        # retrieve date from article date
        article_date_elm = article_elm.find('ArticleDate')
        if article_date_elm is not None and source['year'] is None:
            
            # retrieve year
            year_elm = article_date_elm.find('Year')
            if year_elm is not None:
                source['year'] = year_elm.text
            
            # retrieve month
            month_elm = article_date_elm.find('Month')
            if month_elm is not None:
                source['month'] = month_elm.text
            
            # retrieve day
            day_elm = article_date_elm.find('Day')
            if day_elm is not None:
                source['day'] = day_elm.text
        
        return source
    
    
    def _retrieve_authors(self, article_elm):
        """Retrieves authors info."""
        
        authors = []
        
        # retrieve authors
        for author_elm in article_elm.iter('Author'):
            
            author = {
                'firstname': None,
                'lastname': None,
                'initials': None,
            }
            
            # retrieve first name
            fore_name_elm = author_elm.find('ForeName')
            if fore_name_elm is not None:
                author['firstname'] = fore_name_elm.text
            
            # retrieve last name
            last_name_elm = author_elm.find('LastName')
            if last_name_elm is not None:
                author['lastname'] = last_name_elm.text
            
            # retrieve initials
            initials_elm = author_elm.find('Initials')
            if initials_elm is not None:
                author['initials'] = initials_elm.text
            
            # save valid author
            if author['lastname'] is not None:
                authors.append(author)
        
        return authors


class PubMedResults(object):
    """Holds PubMed search results."""
    
    
    def __init__(self, query, articles=[], total=0, retstart=0, error=None):
        """Initializes a new instance of PubMedResults."""
        
        super(PubMedResults, self).__init__()
        
        self._query = query
        self._articles = articles
        self._total = total
        self._retstart = retstart
        self._error = error
    
    
    @property
    def query(self):
        """Gets original query."""
        
        return self._query
    
    
    @property
    def articles(self):
        """Gets parsed articles."""
        
        return self._articles
    
    
    @property
    def total(self):
        """Gets total count."""
        
        return self._total
    
    
    @property
    def count(self):
        """Gets current count."""
        
        return len(self._articles)
    
    
    @property
    def retstart(self):
        """Gets starting index."""
        
        return self._retstart
    
    
    @property
    def retstop(self):
        """Gets ending index."""
        
        return self._retstart + len(self._articles)
    
    
    @property
    def error(self):
        """Gets error."""
        
        return self._error
