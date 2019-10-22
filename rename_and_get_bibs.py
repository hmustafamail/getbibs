# Rename all the PDFs of academic articles in a folder with the format 'year, author, title.pdf'
#
# Usage: Put a bunch of academic PDFs in a folder, cd into that folder, and run this script:
# python3 rename_and_get_bibs.py
#

import PyPDF2
import re
import os
import urllib.request
import json


def getWebpage(url):
    req = urllib.request.Request(
        url, 
        data=None, 
        headers={
            'User-Agent': 'Python/3.6.1 (Macintosh; Intel macOS 10_13_4) mailto:mustafah@protonmail.com'
        }
    )

    # Get the results
    wp = urllib.request.urlopen(req)
    data = wp.read()

    # Try unwrapping it as JSON, and if you can't, then whatever.
    try:
        data = json.loads(data)
    except:
        data = data.decode("utf-8")

    return data


def searchFileForDOI(filename):
    pdfFileObject = open(filename, 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObject)
    count = pdfReader.numPages

    text = ''

    # get all the text
    for i in range(count):
        page = pdfReader.getPage(i)
        text = text + page.extractText()

    # search all the text
    doi_regex = r'\b(10[.][0-9]{4,}(?:[.][0-9]+)*/(?:(?!["&\'<>])\S)+)\b'
    result = re.search(doi_regex, text)

    if result:
        return result.group(0)
    else:
        return None


def getCitationFromDOI(doi):
    # Get the bibtex item
    # https://citation.crosscite.org/docs.html
    url = 'https://api.crossref.org/works/' + doi + '/transform/application/x-bibtex'
    data = getWebpage(url)
    return data


def appendCitationToBib(citation):
    # Appends the citation to a dedicated .bib file
    f = open('autobibs.bib', 'a')
    f.write('\n\n')
    f.write(citation)
    f.close()


def renameFile(file, citation):
    # renames file with format 'year, author, title.pdf'

    # extract year
    year_regex = r'year = \d\d\d\d'
    year = 'unknown'
    try:
        year = re.search(year_regex, citation).group(0)[-4:]
    except:
        pass

    # extract author
    author_regex = r'author = {.*and'
    author = 'unknown'
    try:
        author = re.search(author_regex, citation).group(0).split(' and ')[0].split(' ')[-1]
    except:
        pass

    # extract title
    title_regex = r'title = {.*}'
    title = 'unknown'
    try:
        title = re.search(title_regex, citation).group(0).split('{')[1].split('}')[0]
    except:
        pass

    # create new filename
    new_filename = year + ', ' + author + ', ' + title + '.pdf'

    # rename file
    os.rename(file, new_filename)


files = [f for f in os.listdir('.') if os.path.isfile(os.path.join('.', f))]

for i in range(len(files)):
    
    # f is for current file
    f = files[i]

    print(str(i) + ": " + f)

    # if it's a pdf, 
    if len(f) > 4 and f[-4:] == ".pdf":

        # see if there is a DOI in that PDF
        doi = searchFileForDOI(f)

        # if so, 
        if doi:
            
            try:
                # get the citation for that doi
                citation = getCitationFromDOI(doi)
            except urllib.error.HTTPError:
                print('unable to find citation for doi: ' + doi)
                continue

            # append the citation to bibs.bib
            appendCitationToBib(citation)

            # rename it to year, author, title.pdf
            renameFile(f, citation)
