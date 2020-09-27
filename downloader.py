#!/usr/bin/env python
#-*- coding:utf-8 -*-
#author: ev3r

import requests
import re
import argparse

def testurl(url):
    pattern = r'http[s]?://(.*)'
    if re.match(pattern,url):
        print '[*] valid'
    else:
        print '[*] invalid url'


if __name__=='__main__':
    parser = argparse.ArgumentParser(description='Back up any webpage to the local')
    parser.add_argument('--url',dest = 'url', help='input your url')
    args = parser.parse_args()

    url = args.url
    testurl(url)

