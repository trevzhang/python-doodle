import urllib2

ids2 = [1, 2, 3, 4, 5, 6]
prefix = "https://newmall-uat-site.ejoy365hk.com/wap/#/pages/item/detail/index?id="
for i in range(1000):
    strip = prefix + str(i)
    headers = {
        "user-agent"
    }
    request = urllib2.Request(strip, headers)
    response = urllib2.urlopen(request)
    html = response.read()
    print(response.geturl())
    print(response.getcode())
    print(response.info())
    print(html)
