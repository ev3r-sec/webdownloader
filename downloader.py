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
imgbasedir = "img"

def testurl(url):
    pattern = r'http[s]?://(.*)/.*'
    if re.match(pattern,url):
        result = re.findall(pattern,url)[0]
        return result
    else:
        return False

def proctext(html):

    soup = BeautifulSoup(html, 'lxml')

    script = soup.findAll("script",attrs={"src":True})
    for jsitem in script:
        src = jsitem['src']
        newname = saveotherfile(src)
        jsitem['src'] = newname

    link = soup.findAll("link",attrs={"href":True})
    for cssitem in link:
        href = cssitem['href']
        newname = saveotherfile(href)
        cssitem['href'] = newname

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

    elif filename.split('.')[-1] == 'css':
        content = requests.get(url=link).text
        if not os.path.exists(cssbasedir):
            os.makedirs(cssbasedir)
        newname = basedir + "/" + cssbasedir + "/" + filename
        with open(newname, "w") as f:
            f.write(content)
        return newname

    else:
        pattern = r'.*\.(png|jpe?g|gif|bmp|psd|tiff|tga|eps)'
        if re.match(pattern, filename):
            content = requests.get(url=link).text
            if not os.path.exists(imgbasedir):
                os.makedirs(imgbasedir)
            newname = basedir + "/" + imgbasedir + "/" + filename
            with open(newname, "wb") as f:
                f.write(content)
            return newname

if __name__=='__main__':
    parser = argparse.ArgumentParser(description='Back up any webpage to the local')
    parser.add_argument('--url',dest = 'url', help='input your url', required=True)
    args = parser.parse_args()

    url = args.url

    splurl = testurl(url)
    if splurl :
        basedir = splurl
        print basedir
        if not os.path.exists(basedir):
            os.makedirs(basedir)

        page = requests.get(url=url)
        newpage = proctext(page.text)
        webpagedir = basedir + "/index.html"  
        with opne(webpagedir, "w") as f:
            f.write(newpage)

    else:
        print "[*] Invalid URL"

