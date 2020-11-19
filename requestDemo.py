import urllib2

import requests


def req_url():
    stri = "https://www.bilibili.com"
    print stri
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36"}
    request = urllib2.Request(stri, headers=headers)
    response = urllib2.urlopen(request)
    html = response.read()
    print response.getcode()
    print response.geturl()
    print response.info()
    print(html)


def req():
    stri = "https://www.bilibili.com"
    print stri
    result = requests.get(stri)
    print result


req_url()
