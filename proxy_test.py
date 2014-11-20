#coding=utf-8
import urllib2
import random



proxy_dict=['http://113.11.198.163:2223/',
			'http://113.11.198.164:2223/',
			'http://113.11.198.165:2223/',
			'http://113.11.198.166:2223/',
			'http://113.11.198.167:2223/',
			'http://113.11.198.168:2223/',
			'http://113.11.198.169:2223/',
			]


proxy_handler = urllib2.ProxyHandler({'http': 'http://113.11.198.167:2223/'})
#113.11.198.[163-169] 2223


proxy_auth_handler = urllib2.HTTPBasicAuthHandler()
proxy_auth_handler.add_password('realm', 'host', 'username', 'password')

opener = urllib2.build_opener(proxy_handler, proxy_auth_handler) 
f = opener.open('http://www.douban.com')
content = f.read()
print content

proxy_handler = urllib2.ProxyHandler({"http":random.choice(proxy_dict)})

opener = urllib2.build_opener(proxy_handler, proxy_auth_handler)
# This time, rather than install the OpenerDirector, we use it directly:
f = opener.open('http://www.douban.com')
content = f.read()
print content

