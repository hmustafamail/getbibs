# getbibs
Ever want to automatically query Google Scholar to get all your citations? Well, Google makes that really hard to do. CrossRef is much nicer to you; they have an API. This script walks through a folder recursively, and queries Crossref's API to get you Bibtex (Latex-compatible) citations for each of your PDFs. 

## Usage
1. Rename all the PDFs to be of the following form: year, first author last name, partial title.pdf (e.g., 2012, boyd, critical questions for big data.pdf)
2. Open a Terminal in the current directory
3. getbibs.py > bibs.txt

## Dependencies
1. Python 3

That's all! Yay!
