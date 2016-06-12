# -*- coding: utf-8 -*-
import urllib
import urllib2

url = "http://sleep.ddns.net/"


def upload_grade(account, score, anonymous):
    if anonymous:
        anonymous = 1
    else:
        anonymous = 0
    try:
        data = {'account': account, 'score': score, 'anonymous': anonymous}
        data = urllib.urlencode(data)
        html = urllib2.urlopen(url + "upload", data).read()
        print html
    except:
        print "YeePortal Server not open"


def look_grade(account):
    try:
        data = {'account': account}
        data = urllib.urlencode(data)
        html = urllib2.urlopen(url + "rank", data).read()
        print html
    except:
        print "YeePortal Server not open"
