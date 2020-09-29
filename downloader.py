#!/usr/bin/env python
#-*- coding:utf-8 -*-
#author: ev3r

import requests
import re
import os
import argparse
from bs4 import BeautifulSoup

basedir = ""
jsbasedir = "js"
cssbasedir = "css"

def testurl(url):
    pattern = r'http[s]?://(.*)'
    if re.match(pattern,url):
        result = re.findall(pattern,url)[0]
        return result
    else:
        return False

def proctext(html):

    soup = BeautifulSoup(html, 'lxml')

    script = soup.findAll("script",attrs={"src":True})
    for item in script:

        src = item['src']
        newname = saveotherfile(src)
        item['src'] = newname

    #  print soup
    return soup.prettify()

def saveotherfile(link):
    filename = link.split('/')[-1]

    if filename.split('.')[-1] == 'js':
        content = requests.get(url=link).text
        if not os.path.exists(jsbasedir):
            os.makedirs(jsbasedir)
        newname = basedir + "/" + jsbasedir + "/" + filename
        with open(newname, "w") as f:
            f.write(content)
        return newname



if __name__=='__main__':
    parser = argparse.ArgumentParser(description='Back up any webpage to the local')
    parser.add_argument('--url',dest = 'url', help='input your url', required=True)
    args = parser.parse_args()

    url = args.url

    splurl = testurl(url)
    if splurl != "No":
        basedir = splurl
        if not os.path.exists(basedir):
            os.makedirs(basedir)

        page = requests.get(url=url)
        pagedic = proctext(page.text)

    else:
        print "[*] Invalid URL"

