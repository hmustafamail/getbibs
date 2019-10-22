# getbibs
This repository has two scripts:

*rename_and_get_bibs.py* renames all the PDFs of academic articles in a folder with the format 'year, author, title.pdf', and also gets you Bibtex (Latex-compatible) citations for each of your PDFs.

*getbibs.py* walks through a folder recursively, and gets you Bibtex (Latex-compatible) citations for each of your PDFs.

## Usage for rename_and_get_bibs.py
_This one is probably what you want._
1. Put a bunch of academic PDFs in a folder
2. Open a Terminal in that folder
3. Run `python3 rename_and_get_bibs.py`

## Usage for getbibs.py
_This one is not as useful._
1. Rename all the PDFs to be of the following form: year, first author last name, partial title.pdf (e.g., 2012, boyd, critical questions for big data.pdf)
2. Open a Terminal in the current directory
3. Run `getbibs.py > bibs.txt`

## Dependencies
1. Python 3
2. PyPDF2

## Technical details
These scripts use the CrossRef API. CrossRef is much more friendly to developers than Google Scholar, which does not support automated querying.

Copyright for all code in this repository: CC BY-NC 4.0 (https://creativecommons.org/licenses/by-nc/4.0/)
