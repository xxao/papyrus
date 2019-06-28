#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

# help: http://www.ncbi.nlm.nih.gov/books/NBK25499/

# import main classes
import time
import urllib.parse
import urllib.request

# define constants
EMAIL = "papyrus@bymartin.cz"
TOOL = "papyrus"
DELAY = 0.34

EINFO_CGI = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/einfo.fcgi'
ESEARCH_CGI = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi'
EPOST_CGI = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/epost.fcgi'
ESUMMARY_CGI = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi'
EFETCH_CGI = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi'
ELINK_CGI = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi'
EGQUERY_CGI = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/egquery.fcgi'
ESPELL_CGI = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/espell.fcgi'

_last_request_time = 0


def einfo(db=None, **kwargs):
    """Entrez EInfo tool."""
    
    parameters = {'db': db}
    parameters.update(kwargs)
    
    return request(EINFO_CGI, parameters).read()


def esearch(db, term, **kwargs):
    """Entrez ESearch tool."""
    
    parameters = {'db': db, 'term': term}
    parameters.update(kwargs)
    
    return request(ESEARCH_CGI, parameters).read()


def epost(db, id, **kwargs):
    """Entrez EPost tool."""
    
    parameters = {'db': db, 'id': id}
    parameters.update(kwargs)
    
    return request(EPOST_CGI, parameters).read()


def esummary(db, **kwargs):
    """Entrez ESummary tool."""
    
    parameters = {'db': db}
    parameters.update(kwargs)
    
    return request(ESUMMARY_CGI, parameters).read()


def efetch(db, **kwargs):
    """Entrez EFetch tool."""
    
    parameters = {'db': db}
    parameters.update(kwargs)
    
    return request(EFETCH_CGI, parameters).read()


def elink(db, dbfrom, cmd, **kwargs):
    """Entrez EFetch tool."""
    
    parameters = {'db': db, 'dbfrom': dbfrom, 'cmd': cmd}
    parameters.update(kwargs)
    
    return request(ELINK_CGI, parameters).read()


def egquery(term, **kwargs):
    """Entrez EGQuery tool."""
    
    parameters = {'term': term}
    parameters.update(kwargs)
    
    return request(EGQUERY_CGI, parameters).read()


def espell(db, term, **kwargs):
    """Entrez EGQuery tool."""
    
    parameters = {'db': db, 'term': term}
    parameters.update(kwargs)
    
    return request(ESPELL_CGI, parameters).read()


def request(path, parameters, post=False):
    """Builds the URL and opens handle."""
    
    # remove unset parameters
    parameters = {k:v for k,v in parameters.items() if v is not None}
    
    # remove post from parameters
    if 'post' in parameters:
        post = parameters['post']
        del parameters['post']
    
    # add identification
    parameters['tool'] = TOOL
    parameters['email'] = EMAIL
    
    # prepare options
    options = urllib.parse.urlencode(parameters, doseq=True)
    
    # assert time restrictions
    global _last_request_time
    while True:
        delay = _last_request_time + DELAY - time.time()
        if delay <= 0:
            _last_request_time = time.time()
            break
        else:
            time.sleep(delay)
    
    # send request
    if post:
        handle = urllib.request.urlopen(path, options.encode('utf8'))
    else:
        url = "%s?%s" % (path, options)
        handle = urllib.request.urlopen(url)
    
    return handle
