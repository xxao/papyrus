
Papyrus
=======

Papyrus is a lightweight article manager. A simple tool to organize, tag and search articles and retrieve their metadata
from PubMed.

.. image:: https://raw.githubusercontent.com/xxao/papyrus/master/dist/screenshot.png


License
-------

MIT License

Copyright (c) 2010-2019 Martin Strohalm

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.


Distribution
------------

Currently there is just a Windows distribution available.


Requirements to run from the source
-----------------------------------

- Python 3.6+
- wxPython
- PyMuPDF


Article Query Tags
------------------

**(int)[ID]** - Article database ID (e.g. *42[ID]*)
**(int)[KEY]** - Article key (e.g. *ag4o[KEY]*)
**(str)[DOI]** - Article DOI (e.g. *10.1021/ac100818g[DOI]*)
**(int)[PMID]** - Article PubMed ID (e.g. *20465224[PMID]*)
**(int)[PY]** - Article publication year (e.g. *2010[PY]*)
**(str)[TI]** - Article title (e.g. *mmass[TI]* or "open source"[TI])
**(str)[AB]** - Article abstract (e.g. *mmass[AB]* or *"open source"[AB]*)
**(str)[NOTE]** - Article notes (e.g. *mmass[NOTE]* or *"open source"[NOTE]*)
**(bool)[PDF]** - Article PDF availability (e.g. *yes[PDF]* or *no[PDF]*)
**(str)[COLOR]** - Article assigned color name (e.g. *red[COLOR]*)
**(str)[LB]** - Article assigned label (e.g. *algorithms[LB]* or *"protein ID"[LB]*)
**(int)[RECENT]** - Article imported within last X days (e.g. *5[RECENT]*)
**(int)[RATING]** - Article rating (e.g. *5[RATING]*)
**(int)[RBE]** - Article rating below or equal (e.g. *3[RBE]*)
**(int)[RAE]** - Article rating above or equal (e.g. *3[RAE]*)

**(str)[JT]** - Journal title (e.g. *proteom[JT]*)
**(str)[JA]** - Journal abbreviation (e.g. *"anal chem"[JA]*)

**(str)[AU]** - Author's short name (e.g. *Strohalm[AU]* or *"Strohalm M"[AU]*)
**(int)[AUID]** - Author's database ID (e.g. *42[AUID]*)
**(str)[FAU]** - First author short name (e.g. *Strohalm[FAU]* or *"Strohalm M"[FAU]*)
**(str)[LAU]** - Last author short name (e.g. *Strohalm[LAU]* or *"Strohalm M"[LAU]*)

**(int)[LBID]** - Assigned label database ID (e.g. *42[LBID]*)
**(int)[COLLECTIONID]** - Assigned collection database ID (e.g. *42[COLLECTIONID]*)


Article Query Grammar
---------------------

**space** - &&-like operand (e.g. *mmass protein*)
*AND**  - &&-like operand (e.g. *mmass AND protein*)
**OR**  - |-like operand (e.g. *mmass OR protein*)
**"quote"** or **'quote'** - exact string sequence (e.g. *"mmass data miner"*)
**[TAG]** - restricts search to specific database field (e.g. *10.1021/ac100818g[DOI]*)
**(group)** - grouping of logical expressions (e.g. *strohalm AND (kodicek OR havlicek)*)
**NOT** - negation of expression (e.g. *NOT strohalm AND kodicek*)
