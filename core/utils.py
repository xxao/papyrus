#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

# import modules
import re
import os.path
import time
import unicodedata
import fitz

# set patterns
DOI_PATTERN = re.compile('(10\.\d{4}/[a-zA-Z0-9\.\-\_/\(\)]+)')
PAGES_PATTERN = re.compile('^([0-9]+)-([0-9]+)$')

# set diacritics replacements
REPLACERS = [
    (u"á", "a"), (u"Á", "A"),
    (u"é", "e"), (u"É", "E"),
    (u"ě", "e"), (u"Ě", "E"),
    (u"í", "i"), (u"Í", "I"),
    (u"ý", "y"), (u"Ý", "Y"),
    (u"ó", "o"), (u"Ó", "O"),
    (u"ú", "u"), (u"Ú", "U"),
    (u"ů", "u"), (u"Ů", "U"),
    (u"ž", "z"), (u"Ž", "Z"),
    (u"š", "s"), (u"Š", "S"),
    (u"č", "c"), (u"Č", "C"),
    (u"ř", "r"), (u"Ř", "R"),
    (u"ď", "d"), (u"Ď", "D"),
    (u"ť", "t"), (u"Ť", "T"),
    (u"ň", "n"), (u"Ň", "N"),
    (u"ľ", "l"), (u"Ľ", "L"),
]


def doi_from_pdf(path):
    """Retrieves article DOI from given PDF file."""
    
    doi = None
    
    # check path
    if not os.path.exists(path):
        return doi
    
    # open PDF
    doc = fitz.open(path)
    
    # get DOI from text
    for page in doc:
        
        # get page text
        text = page.getText()
        
        # retrieve DOI
        doi = parse_doi(text)
        if doi:
            break
    
    # close
    doc.close()
    
    return doi


def parse_doi(value):
    """Parses DOI from given text."""
    
    # check value
    if not value:
        return None
    
    # match raw pattern
    match = DOI_PATTERN.search(value)
    if not match:
        return None
    
    # get raw match
    doi = match.group(0)
    
    # remove trailing dot
    if doi[-1] == ".":
        doi = doi[:-1]
    
    # remove trailing brackets
    if doi[-1] == ")" and doi.count("(") != doi.count(")"):
        doi = doi[:-1]
    
    return doi


def remove_diacritics(value):
    """Removes special characters."""
    
    # check value
    if not value:
        return value
    
    # copy value
    text = str(value)
    
    # replace known characters
    for pair in REPLACERS:
        text = text.replace(pair[0], pair[1])
    
    # convert encoding
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')
    
    return text


def move_cover_page(path, query, delete=False):
    """Moves the cover page to the end of the PDF or removes it completely."""
    
    # check path and query
    if not os.path.exists(path) or not query:
        return
    
    # get matching pages
    pages = search_pdf(path, query)
    
    # skip if no match or unexpected match
    if len(pages) != 1 or pages[0] != 1:
        return
    
    # init paths
    in_path = path
    out_path = path + ".out"
    
    # open PDF
    doc = fitz.open(in_path)
    
    # prepare pages
    pages = list(range(1, len(doc)))
    if not delete:
        pages.append(0)
    
    # make new PDF
    try:
        doc.select(pages)
        doc.save(out_path)
        doc.close()
        os.remove(in_path)
        time.sleep(0.5)
        os.rename(out_path, in_path)
    
    except IOError:
        pass


def search_pdf(path, query):
    """Searches PDF for specified text to get page numbers."""
    
    pages = []
    
    # check path
    if not os.path.exists(path):
        return pages
    
    # open PDF
    doc = fitz.open(path)
    
    # search for text
    i = 0
    for page in doc:
        i += 1
        
        # get page text
        text = page.getText()
        
        # remember matching page
        if query in text:
            pages.append(i)
    
    # close
    doc.close()
    
    return pages


def count_pages(pages):
    """Parses given page string to get total number of pages."""
    
    # check value
    if not pages:
        return None
    
    # match pattern
    match = PAGES_PATTERN.match(pages)
    if match is None:
        return None
    
    # try to count pages
    try:
        start = int(match.group(1)[-len(match.group(2)):])
        end = int(match.group(2))
        return end - start + 1
    
    except ValueError:
        return None
