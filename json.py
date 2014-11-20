import requests
import json
import urllib2
import urllib


response = urllib2.urlopen('http://54.223.153.21:8012/proxy').read()#requests.get('http://54.223.153.21:8012/proxy')
#response.decoding = 'gb2312'
test = json.loads(response)
for a in test.keys():
    for b in test[a].keys():
        print test[a][b]