#!/usr/bin/env python3
#
# Crawls current directory recursively, queries CrossRef for citations for PDFs
#
# PDF file names must take the following form:
# year, first author's last name, partial title.pdf
#
# Mustafa Hussain, Spring 2018
#
# TODO: do a date-time modified thing to avoid re-querying old ones. and record the last date-time it was run.

import os, glob
import urllib.request
import pdb
import json
from pprint import pprint
import time

email = "YOUR EMAIL HERE (in case the CrossRef API people need to tell you to throttle it down or something)"

#searches for roots, directory and files
#Path
p=os.getcwd()

limit = 300

def getWebpage(url):
    req = urllib.request.Request(
        url, 
        data=None, 
        headers={
            'User-Agent': 'Python/3.6.1 (Macintosh; Intel macOS 10_13_4) mailto:' + email
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

currentfile = "none"
for root,dirs,files in os.walk(p):
    for f in files:
        if len(f) > 4 and f[-4:] == ".pdf":
            try:
                f = f[:-4]
                currentfile = f
                year, author, title = f.split(',')
                
                author = author.strip().replace(' ', '+').lower()
                title = title.strip().replace(' ', '+').lower()
                
                # check if it exists already, or if it is marked "ignore". skip it if it does.
                firstwordoftitle = title.split('+')[0]
                reffilename = 'bibs/' + year + author + firstwordoftitle + '.txt'
                if os.path.isfile(reffilename) or firstwordoftitle == 'ignore':
                    continue
                
                # Search for the DOI - visit the web at that address and Get the search results
                # https://github.com/CrossRef/rest-api-doc#queries
                url = "https://api.crossref.org/works?query.title=" + title + "&query.author=" + author
                data = getWebpage(url)
                
                # reports and such, skip
                if author in ['onc']:
                    continue
                
                # Get the DOI of the first item in search results
                doi = data['message']['items'][0]['DOI']
                
                # Get the bibtex item
                # https://citation.crosscite.org/docs.html
                #time.sleep(1)
                url = 'https://api.crossref.org/works/' + doi + '/transform/application/x-bibtex'
                data = getWebpage(url)
                
                # Write the citation into a file
                #f = open(reffilename, 'w')
                #f.write(data)
                #f.close()

                print(data)
                
                if limit == 0:
                    exit()
                else:
                    limit = limit - 1
                
            except Exception as e:
                print(currentfile + ": " + str(e))
                continue
         

            
