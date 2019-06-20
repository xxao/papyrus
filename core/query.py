#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

# import modules
from .grammar import Grammar
from .queries import *
from .article import Article
from .journal import Journal
from .author import Author
from .label import Label
from .collection import Collection


# create basic query grammar
_GRAMMAR = Grammar(
    op = 'AND | OR',
    val = '[A-Za-z0-9-_\.\\\/]+',
    quote = '" [A-Za-z0-9-_\.\s\\\/]+ " | \' [A-Za-z0-9-_\.\s\\\/]+ \'',
    tag = '\[[A-Za-z0-9]+\]',
    elm = 'val tag | quote tag',
    group = '\( expr \)',
    neg = 'NOT expr',
    expr = 'neg | group op expr | elm op expr | quote op expr | val op expr | group | elm | quote | val',
    )


class Query(object):
    """
    Represents library query definition and provides functionality to parse
    query and convert it into SQLite query and list of values.
    """
    
    
    def __init__(self, query, entity):
        """
        Initializes a new instance of Query.
        
        Args:
            query: str
                Query string.
            
            entity: str
                Entity name, typically main table name.
        """
        
        super(Query, self).__init__()
        
        self._query = query
        self._entity = entity
        self._tree = self._parse(query)
    
    
    def __str__(self):
        """Gets standard string representation."""
        
        return _GRAMMAR.visualize(self.tree) if self.tree is not None else ""
    
    
    @property
    def query(self):
        """
        Gets query string.
        
        Returns:
            query: str
                Query string.
        """
        
        if not self._tree:
            return ""
        
        return self._to_str(self._tree[0])
    
    
    @property
    def entity(self):
        """
        Gets entity name.
        
        Returns:
            entity: str
                Entity entity.
        """
        
        return self._entity
    
    
    @property
    def tree(self):
        """
        Gets parsed query tree.
        
        Returns:
            tree: hierarchical list
                Parsed query tree.
        """
        
        return self._tree
    
    
    def select(self):
        """
        Parses query into SQL SELECT and list of values.
        
        Returns:
            result: (sql, list of values)
                Tuple of SQL query and values.
        """
        
        conditions = ""
        values = []
        
        # get query tree
        tree = self.tree
        
        # make sqls and values from tree
        if tree:
            sqls, values = self._parse_expr(tree[0])
            conditions = " ".join(sqls)
        
        # check conditions
        if not conditions and self._query:
            return None, None
        
        # make sql query
        sql = "SELECT * FROM %s" % self._entity
        if conditions:
            sql += " WHERE %s" % conditions
        
        return sql, values
    
    
    def count(self):
        """
        Parses query into SQL COUNT(*) and list of values.
        
        Returns:
            result: (sql, list of values)
                Tuple of SQL query and values.
        """
        
        conditions = ""
        values = []
        
        # get query tree
        tree = self.tree
        
        # make sqls and values from tree
        if tree:
            sqls, values = self._parse_expr(tree[0])
            conditions = " ".join(sqls)
        
        # check conditions
        if not conditions and self._query:
            return None, None
        
        # make sql query
        sql = "SELECT COUNT(*) FROM %s" % self._entity
        if conditions:
            sql += " WHERE %s" % conditions
        
        return sql, values
    
    
    def _to_str(self, tree):
        """Converts query into text."""
        
        text = ""
        
        if type(tree) != list:
            return " %s" % tree
        
        if tree[0] == 'quote':
            return " \"%s\"" % tree[2]
        
        for item in tree[1:]:
            text += self._to_str(item)
        
        return text
    
    
    def _parse(self, query):
        """Parses query into tree."""
        
        # parse query into tree
        tree = _GRAMMAR.parse('expr', query)
        
        # join individual expressions by AND
        if tree and len(tree) > 1:
            
            buff = ['expr', tree[0]]
            for expr in tree[1:]:
                buff += [['op', 'AND'], expr]
                
            tree = [buff]
        
        return tree
    
    
    def _parse_expr(self, expr):
        """Parses expr into SQL conditions."""
        
        sqls = []
        values = []
        
        for item in expr[1:]:
            name = item[0]
            
            if name == 'expr':
                parsed = self._parse_expr(item)
            
            elif name == 'neg':
                parsed = self._parse_neg(item)
            
            elif name == 'group':
                parsed = self._parse_group(item)
            
            elif name == 'elm':
                parsed = self._parse_elm(item)
            
            elif name == 'quote':
                parsed = self._parse_quote(item)
            
            elif name == 'val':
                parsed = self._parse_val(item)
            
            elif name == 'op':
                parsed = [item[1]], []
            
            else:
                raise KeyError("Unknown rule! --> '%s" % name)
            
            sqls += parsed[0]
            values += parsed[1]
        
        return sqls, values
    
    
    def _parse_neg(self, item):
        """Parses negation into SQL conditions."""
        
        results = self._parse_expr(item[2])
        sqls = [item[1]] + results[0]
        values = results[1]
        
        return sqls, values
    
    
    def _parse_group(self, item):
        """Parses group into SQL conditions."""
        
        results = self._parse_expr(item[2])
        sqls = [item[1]] + results[0] + [item[3]]
        values = results[1]
        
        return sqls, values
    
    
    def _parse_elm(self, item):
        """Parses element into SQL conditions."""
        
        tag = item[2][1]
        value = item[1][2] if item[1][0] == 'quote' else item[1][1]
        
        return self._make_query(value, tag)
    
    
    def _parse_quote(self, item):
        """Parses quote into SQL conditions."""
        
        return self._make_query(item[2])
    
    
    def _parse_val(self, item):
        """Parses value into SQL conditions."""
        
        return self._make_query(item[1])
    
    
    def _make_query(self, value, tag=None):
        """Creates SQL for specific entity type."""
        
        # uppercase tag
        if tag:
            tag = tag.upper()
        
        # parse articles tags
        if self._entity == Article.NAME:
            return make_articles_query(value, tag)
        
        # parse journals tags
        elif self._entity == Journal.NAME:
            return make_journals_query(value, tag)
        
        # parse authors tags
        elif self._entity == Author.NAME:
            return make_authors_query(value, tag)
        
        # parse labels tags
        elif self._entity == Label.NAME:
            return make_labels_query(value, tag)
        
        # parse collections tags
        elif self._entity == Collection.NAME:
            return make_collections_query(value, tag)
        
        # unknown entity type
        else:
            message = "Unsupported entity to create SQL query from! --> %s" % self._entity
            raise KeyError(message)
