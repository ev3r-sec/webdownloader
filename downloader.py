#!/usr/bin/env python
#-*- coding:utf-8 -*-
#author: ev3r

import requests
import re
import os
import argparse
from bs4 import BeautifulSoup

jsbasedir = "js"
cssbasedir = "css"

def testurl(url):
    pattern = r'http[s]?://(.*)'
    if re.match(pattern,url):
        return True
    else:
        return False

def proctext(html):

    soup = BeautifulSoup(html, 'lxml')

    script = soup.findAll("script",attrs={"src":True})
    #  print script
    for item in script:

        src = item['src']
        newname = saveotherfile(src)
        item['src'] = newname

    #  print soup
    return soup.prettify()

def saveotherfile(link):
    filename = link.split('/')[-1]

    if filename.split('.')[-1] == 'js':
        print filename



if __name__=='__main__':
    parser = argparse.ArgumentParser(description='Back up any webpage to the local')
    parser.add_argument('--url',dest = 'url', help='input your url')
    args = parser.parse_args()

    url = args.url

    if testurl(url):

        page = requests.get(url=url)
        #  print len(page.text)
        pagedic = proctext(page.text)
        #  savefile(pagedic)

    else:
        print "[*] Invalid URL"


