#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

HTML_ARTICLE_TOP = """<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">

<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="cs" lang="cs">
<head>
  <meta http-equiv="content-type" content="text/html; charset=utf-8" />
  <title>Article Details</title>
  <style type="text/css">
  <!--
    
    body{
        margin: 1.5em;
        font-size: 9pt;
        font-family: Arial, Verdana, Geneva, Helvetica, sans-serif;
    }
    
    a{
        color: #000;
        text-decoration: none;
    }
    
    a:hover{
        background-color: #eee;
    }
    
    #title{
        font-size: 1.2em;
        margin: .3em 0 .7em 0;
    }
    
    #rating{
        margin: 0 0 .7em 0;
    }
    
    #rating a{
        margin: 0 2px 0 0;
        color: #e6e6e6;
        font-size: 26px;
    }
    
    #rating a:hover{
        background-color: #fff;
    }
    
    #rating a.selected{
        color: #3232ff;
    }
    
    #colour{
        margin: 0 0 1.5em 0;
    }
    
    #colour a{
        display: inline-block;
        width: 11px;
        height: 11px;
        margin: 0 4px 0 0;
        color: #c8c8c8;
        background-color: #c8c8c8;
        border: 1px solid #fff;
    }
    
    #colour a.selected{
        border-color: #000;
    }
    
    #colour a:hover{
        border-color: #000;
    }
    
    #citation{
        margin: 0 0 .5em 0;
        font-size: 1em;
        font-style: oblique;
    }
    
    #doi{
        margin: 0;
        font-size: 1em;
        font-style: oblique;
    }
    
    #pmid{
        margin: 0;
        font-size: 1em;
        font-style: oblique;
    }
    
    #filename{
        margin: 0;
        font-size: 1em;
        font-style: oblique;
    }
    
    #authors{
        margin-left: 0;
        padding-left: 0;
        font-size: 1em;
        list-style-position: inside;
    }
    
    #authors .author_count{
        margin-left: .5em;
        font-size: 1em;
        color: #aaa;
    }
    
    #labels{
        font-size: 1em;
    }
    
    #abstract{
        font-size: 1.05em;
    }
    
    #notes{
        font-size: 1.05em;
    }
    
  -->
  </style>
  
</head>

<body>
"""

HTML_BOTTOM = """
</body>
</html>
"""