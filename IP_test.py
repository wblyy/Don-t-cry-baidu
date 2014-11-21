# -*- coding: utf-8 -*-
import re,urllib2
class Getmyip:
    def getip(self):
        try:
            myip = self.visit("http://www.ip138.com/ip2city.asp")
        except:
            try:
                myip = self.visit("http://www.bliao.com/ip.phtml")
            except:
                try:
                    myip = self.visit("http://www.whereismyip.com/")
                except:
                    myip = "So sorry!!!"
        return myip
    def visit(self,url):
        proxy_handler = urllib2.ProxyHandler({'http': 'http://113.11.198.163:2223/'})
        proxy_auth_handler = urllib2.HTTPBasicAuthHandler()
        proxy_auth_handler.add_password('realm', 'host', 'username', 'password')
 
        opener = urllib2.build_opener(proxy_handler, proxy_auth_handler)
        # This time, rather than install the OpenerDirector, we use it directly:
        #f = opener.open('http://www.douban.com')
        #content = f.read()
        opener = urllib2.urlopen(url)
        if url == opener.geturl():
            str = opener.read()
        return re.search('\d+\.\d+\.\d+\.\d+',str).group(0)
getmyip = Getmyip()
localip = getmyip.getip()
print localip