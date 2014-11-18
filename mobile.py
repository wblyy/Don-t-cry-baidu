#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import requests
import time
import json
import urllib
import os

class Mobie(object):
    """docstring for Mobie"""
    def __init__(self, username, passwd):
        super(Mobie, self).__init__()
        self.session = requests.session()
        self.main_url = 'http://tieba.baidu.com/mo/q----,sz@320_240-1-3---2/m?tn=bdIndex&lp=9002'
        self.username = username
        self.passwd = passwd

    def start(self):
        self.head()
        self.main_page()

    def main_page(self):
        #首页
        r = self.session.get(self.main_url)
        self.baiduid = self.session.cookies.get('BAIDUID')
        login_url = self.find_url(r.content, type=0)
        self.session.get('http://wap.baidu.com/r/wise/wapsearchindex/top.gif', headers={'Host':'wap.baidu.com'})
        
        #登录页
        r = self.session.get(login_url, headers={"Host":"wappass.baidu.com","Referer":self.main_url})
        print '*'*20
        print r.request.headers
        print '-'*20
        print r.headers
        print '*'*20
        print r.request.url
        bdcm = self.find_url(r.content, type=3)
        u = self.find_url(r.content, type=5)
        print 'bdcm', bdcm
        print 'u', u
        # print r.content
        self.make_cookie()
        img_str = self.find_url(r.content, type=1)
        img_url = 'http://wappass.baidu.com/cgi-bin/genimage?%s' % img_str
        # img = self.session.get(img_url, headers={'Accept':'image/webp,*/*;q=0.8','Referer':login_url})

        for i in self.session.cookies:
            print 'login page', i
        #验证码
        img = self.session.get(img_url, headers={'Referer':login_url})
        for i in self.session.cookies:
            print 'get img page', i

        print '---'*10
        print 'request headers:\n', img.request.headers
        print '---'*10
        print 'result headers:\n', img.headers
        # print img.content
        if not os.path.exists('./code/'):
            os.makedirs('./code')
        path = "./code/code.jpg"
        with file(path, 'wb')as f:
            f.write(img.content)

        #提交验证码
        verifycode = self.write_code(path)
        print verifycode
        #登陆
        self.login(verifycode, img_str, login_url, bdcm, u)

    def make_cookie(self):
        pass
        cookies=[]
        for i in self.session.cookies:
            if i.name.find('Hm_lpvt') or i.name.find('Hm_lvt'):
                print i.name + ':' + i.value
                cookies.append([i.name,i.value])
        for i in cookies:
            self.session.cookies.update({i[0]:None})
            self.session.cookies.update({i[0]:i[1]})

    def login(self, verifycode="", img_str="", referer='', bdcm="", u=""):
        data = {
            'username':self.username,
            'password':self.passwd,
            'verifycode':verifycode,
            'submit':'登录',
            'quick_user':'0',
            'isphone':'0',
            'sp_login':'waprate',
            'uname_login':'',
            'loginmerge':'1',
            'vcodestr':verifycode,
            'u':u,
            'skin':'default_v2',
            'tpl':'tb',
            'ssid':'',
            'from':'',
            'uid':self.baiduid,
            'pu':'sz@320_240',
            'tn':'bdIndex',
            'bdcm':bdcm,
            'type':'',
            'bd_page_type':'1' }

        head={
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language':'zh,zh-CN;q=0.8,zh-TW;q=0.6',
            'Content-Type':'application/x-www-form-urlencoded',
            'Origin':'http://wappass.baidu.com',
            'Referer':referer}
        result = self.session.post('http://wappass.baidu.com/passport/login', data=urllib.urlencode(data), headers=head, verify=True)
        print '---'*10
        for i in self.session.cookies:
            print i.name + ':' + i.value

        print '---'*10
        print 'request headers:\n', result.request.headers
        print '---'*10
        print 'result body:\n', result.request.body
        print '---'*10
        print 'result headers:\n', result.headers
        print '---'*10
        print 'BDUSS', result.cookies.get('BDUSS')
        print self.find_url(result.content, type=4)

    def write_code(self, path):
        verifycode = ''
        while not verifycode:
            verifycode = raw_input("请输入[%s]验证码:" % path)
            print verifycode
        return verifycode

    def find_url(self, content="", type=0):
        """
        type:0  登录网址
        type:1  字母验证码
        type:2  汉字验证码
        type:3  bdcm
        type:4  error message
        """
        res = ""
        if type == 0:
            res = r'href="(http://wappass.baidu.com/passport/.login.+?)"'
        elif type == 1:
            res = r'genimage\?(.+?)"'
        elif type == 2:
            res = r''
        elif type == 3:
            res = r'bdcm.+value="(.+?)"'
        elif type == 4:
            res = r'error_area.+'
        elif type == 5:
            res = r'name="u" value="(.+)"'
        else:
            return False
        result = re.findall(res, content)
        if len(result) > 0:
            return max(result)
        else:
            return False


    def head(self):
        heads = {
            "Host":"tieba.baidu.com",
            "User-Agent":"Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36",
            # "User-Agent":"Mozilla/5.0 (iPhone; CPU iPhone OS 7_0 like Mac OS X; en-us) AppleWebKit/537.51.1 (KHTML, like Gecko) Version/7.0 Mobile/11A465 Safari/9537.53",
            "Accept-Encoding":"gzip,deflate,sdch",
            "Accept-Language":"zh,zh-CN;q=0.8,zh-TW;q=0.6",
            "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
        }
        self.session.headers.update(heads)

if __name__ == '__main__':
    Mobie('13869139163','zhang!4343').start()
