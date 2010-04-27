#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib2
import string
from collections import deque


queue = deque();
urlcount=0
internalurl=0
externalurl=0
needle=""

def download_and_parse (url,domain):
    #print "downloading ",url
    global urlcount
    global internalurl
    global externalurl
    global needle

    for line in urllib2.urlopen(url):
        index=line.find("a href")
        if index != -1:                 #a href link found in this line
            tempurl =line[(index+8):]
            endIndex=tempurl.find("\"")
            #print "\nURL ",tempurl 
            if endIndex != -1:          # found a terminating " character
                newurl =tempurl[:endIndex]
                endIndex=newurl.find("\'")
                if endIndex != -1:      # also found a terminating ' character
                    newurl =newurl[:endIndex]   # keep string up to endIndex
                urlcount=urlcount+1           # increase url counter
                #print urlcount," ",newurl            
            else: 
                endIndex=tempurl.find("\'")
                if endIndex != -1:
                    newurl =tempurl[:endIndex]
                    endIndex=newurl.find("\'>")
                    if endIndex != -1:
                        newurl =newurl[:endIndex]
                        #print newurl            
            if newurl.startswith("http://"):
                candidate =newurl[7:]
            else: 
                candidate = newurl
            if candidate.startswith(domain) :
                internalurl=internalurl+1
		queue.append(newurl)            
                #print internalurl," ",newurl
            else:
                externalurl=externalurl+1
	index=line.find(needle)
	if index != -1:                 #
	    print "needle was found in ", newurl
    print "There are ", internalurl, " internal urls. Rejected ",externalurl," urls. Total urls: ", urlcount



url=raw_input("Enter URL: ")
maxlinks=raw_input("Enter max links to follow: ")
needle=raw_input("What to find: ")

if url[:4] == 'http':
    domain = url[7:]
    print "starts with http://"
else: 
    print "adding http://"
    domain = url
    url="http://"+url


queue.append(url)
while len(queue) != 0 & internalurl < maxlinks:
    #print internalurl, ": downloading ",url, " for domain ",domain, " maxlinks: ", maxlinks
    download_and_parse(queue.popleft(), domain)

print "There are ", internalurl, " internal urls. Rejected ",externalurl," urls. Total urls: ", urlcount
