#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import os
import sys
import pickle
import time
import datetime
import random
import functools
import hashlib
import urlparse

from bs4 import BeautifulSoup
import requests

# post_verifycode_url = "http://sonidigg.xicp.net:9000/"
post_verifycode_url = "http://54.223.153.21:9000/"
# verifycode_url = "http://221.123.160.241:9000/baikecode?type="

def rerun(method):
    """Decorate with this method to restrict to site admins."""
    @functools.wraps(method)
    def wrapper(*args, **kwargs):
        for i in xrange(300):
            try:
                return method(*args, **kwargs)
            except Exception, e:
                print e, 'run again!'
                continue
    return wrapper

class Tieba(object):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    cookies_path = os.path.join(current_dir, "cookies/")
    # use this login_url, it will redirect to tieba index(http://tieba.baidu.com/mo)
    login_url = "http://wappass.baidu.com/passport/?login&u=http%3A%2F%2Ftieba.baidu.com%2Fmo"
    post_url = "http://wappass.baidu.com/passport/login"
    headers = {
        # "User-Agent": '"Opera 10.00 Mobi - SymbOS" useragent="Opera/9.80 (S60; SymbOS; Opera Mobi/499; U; ru) Presto/2.4.18 Version/10.00',
        "User-Agent": 'Mozilla/5.0 (Android; Mobile; rv:22.0) Gecko/22.0 Firefox/22.0',
    }

    def __init__(self, username, passwd, proxies=None): # {'http': 'http://123.21.32.32:80'}
        self.username = username
        self.passwd = passwd
        #self.session.proxies = {'http': 'http://113.11.198.163:2223/'}
        self.session = requests.session()
        self.session.proxies = proxies or {}
        
        self.verifycode_id = None
        try:
            self._load_cookie()
        except Exception, e:
            pass
            # print e
        self.session.headers.update(self.headers)
        
        
    def _save_cookie(self):     # if login successufully, will call this function to save cookies
        if not os.path.exists(self.cookies_path):
            os.makedirs(self.cookies_path)        
        with open(self.cookies_path+hashlib.md5(self.username+self.passwd).hexdigest()+'.cookie', 'w') as f:
            pickle.dump(self.session.cookies, f)

    def _load_cookie(self):
        with open(self.cookies_path+hashlib.md5(self.username+self.passwd).hexdigest()+'.cookie') as f:
            self.session.cookies = pickle.load(f)
    def _del_cookie(self):
        cookiefile = self.cookies_path+hashlib.md5(self.username+self.passwd).hexdigest()+'.cookie'
        if os.path.isfile(cookiefile):
            print_message("该用户需重新登录")
            os.remove(cookiefile)

    def _get_form(self, htmlstr):
        formdata = {}
        soup = BeautifulSoup(htmlstr)
        for i in soup.find_all('input'):
            if i.get('name'):
                formdata[i.get('name')] = i.get('value')
        return formdata

    def _get_verifycode(self, htmlstr):
        re_hm_url = re.compile(u'src="(http://hm.*?)"')
        hm_url = re_hm_url.findall(htmlstr)
        if hm_url:
            self.session.get(hm_url[0]) # just want to get the cookies in http://hm.baidu.com/hm.gif
        re_verifycode_url = re.compile(u'src="(.*?captchaservice.*?)"')
        verifycode_url = re_verifycode_url.findall(htmlstr)
        if verifycode_url:
            r = self.session.get(verifycode_url[0].replace('&amp;', '&'), stream=True)
            if r.status_code == 200:
                with open('./code.jpg', 'wb') as f:
                    for chunk in r.iter_content():
                        f.write(chunk)
            print_message("正在识别['./code.jpg']验证码...")

            if 'tieba' in verifycode_url[0]:
                verifycode = post_verifycode('./code.jpg', "cn")
            else:
                verifycode = post_verifycode('./code.jpg', "en")
            if '|' in verifycode:
                row = verifycode.split('|')
                verifycode = row[0]
                self.verifycode_id = row[1]
            else:
                self.verifycode_id = None
            print_message('自动识别[./code.jpg]验证码为: ' + verifycode)

            # verifycode = raw_input("请输入[./code.jpg]验证码: ")
        else:
            verifycode = ""
        return verifycode

    def _get_error_message(self, htmlstr, re_pattern):
        error_message = re.findall(re_pattern, htmlstr)
        return error_message[0] if error_message else ""

    def islogin(self):
        r = self.session.get('http://tieba.baidu.com/mo/',timeout=10)
        if "注销" in r.content:
            return True
        else:
            return False

    def _login(self):
        htmlstr = self.session.get(self.login_url,timeout=10).content
        formdata = self._get_form(htmlstr)
        verifycode = self._get_verifycode(htmlstr)
        if verifycode:
            formdata.update({"verifycode": unicode(verifycode)})
        formdata.update({
            "password": unicode(self.passwd),
            "username": unicode(self.username),
            })
        if 'changevcode' in formdata:
            formdata.pop('changevcode')
        r = self.session.post(self.post_url, data=formdata) 
        if "BDUSS" in self.session.cookies:
            self._save_cookie()
            print_message("%s 登陆成功\n" %  self.username)
            return True
        else:
            error_message = self._get_error_message(r.content, '<span class="highlight">(.*?)</span>')
            if error_message:
                raise TiebaError(error_message)
            else:
                raise TiebaError('登录失败')

    def login(self):
        print_message("%s : %s 正在登陆" % (self.username, self.passwd))
        if self.islogin():
            print_message("%s 登陆成功\n" %  self.username)
            return True
        else:
            return self._login()

    def open_url(self, url):
        return self.session.get(url,timeout=10).content

    def get_questions(self, pn='0'):        
        return self.session.get('http://zhidao.baidu.com/ihome/api/push?pn=%s&rn=25&type=tag&tags=歌名' % pn).json()

    def get_zhidao_similar(self, title='', content=''):
        data = {
            'content': content,
            'word': title
            }
        r = self.session.post('http://zhidao.baidu.com/api/newaskpush', data=data)
        try:
            return random.choice(r.json()['list'])['answer']
        except:
            return None
    # @rerun
    def answer_q(self, qid, content='用“音乐雷达”能搜到'):
        q_url = 'http://zhidao.baidu.com/question/%s.html' % qid
        page = self.open_url(q_url).decode('utf-8','ignore').encode('utf-8')
        formdata = self._get_form(page)
        # print formdata
        for i in ['cifr', 'rn', 'sub0', 'sub1', 'sub_answer', 'word']:
            if i in formdata: formdata.pop(i)
        formdata.update({
                "content": content,
                "anonymous": '0',
                })
        r = self.session.post('http://zhidao.baidu.com/msubmit/answer?ta=1&cifr=null', data=formdata)
        htmlstr = r.content.decode('utf-8','ignore').encode('utf-8')
        # print htmlstr
        soup = BeautifulSoup(htmlstr)
        if soup.title.string.encode('utf8') == '输入验证码': # if verifycode exist do it, else skip
            formdata = self._get_form(htmlstr)
            if 'vcode_reload' in formdata: formdata.pop('vcode_reload')
            verifycode = self._get_verifycode(htmlstr)
            if verifycode:
                formdata.update({"vcode": verifycode})
            r = self.session.post('http://zhidao.baidu.com/msubmit/answer?ta=1&cifr=null', data=formdata)
            htmlstr = r.content.decode('utf-8','ignore').encode('utf-8')
        if '您的回答已成功提交' in r.content:
            # print r.headers
            # print r.content
            print 'Answer Succefull!\t%s\t%s' % (q_url, content)
        else:
            # print htmlstr
            raise Exception('Answer Failed')

    def session(self):
        return self.session

    def ding_tie(self, tie_url, content="ding"):
        print_message("正在回帖: "+ tie_url)
        page = self.open_url(tie_url)
        if '您要浏览的贴子不存在' in page:
            raise TiebaError('您要浏览的贴子不存在\n'+'帖子地址：'+tie_url)
        formdata = self._get_form(page)
        formdata.update({
                "co": content,
                })
        for i in ['sub', 'pnum', 'pd', 'lp', 'kz', 'tnum', 'insert_pic', 'insert_smile']:
            if i in formdata: formdata.pop(i)
        # print page
        submit_url = urlparse.urljoin(tie_url, re.findall(u'<div class="d h"><form action="(.*?/submit)" method="post"', page)[0])
        print "submit_url: "+submit_url
        r = self.session.post(submit_url, data=formdata)
        htmlstr = r.content.decode('utf-8').encode('utf-8')
        if "回贴成功" in htmlstr: # some time you did not need verifycode
            print_message("回贴成功 回帖内容: %s\n帖子地址: %s\n" % (content, tie_url))
            return True
        # 此时回帖不成功可能有两种可能，1.跳转到填验证码页面，2，跳转到登录页面（因为会话过期，执行敏感操作需重新登录
        # 如果登录失败，可清楚cookie，下次重新登录就ok了
        # print htmlstr+"\n\n\n....."
        if "登录百度帐号" in htmlstr:
            self._del_cookie()
            raise TiebaError("会话到期，顶贴需重新登录")
        formdata = self._get_form(htmlstr)
        verifycode = self._get_verifycode(htmlstr)
        if verifycode:
            formdata.update({"word1": verifycode})
        formdata.update({
                "co": content,
                })
        if "img1" in formdata: formdata.pop('img1')
        r = self.session.post(submit_url, data=formdata)        
        if "回贴成功" in r.content.decode('utf-8').encode('utf-8'):
            print_message("回贴成功, 回帖内容: %s\n帖子地址: %s\n" % (content, tie_url))
            return True
        else:
            error_message = self._get_error_message(r.content, 'class="light">(.*?)</span>')
            if error_message:
                print_message("回帖失败,错误信息: "+error_message)
                if "验证码" in error_message and self.verifycode_id:
                    post_wrong_verifycode(self.verifycode_id)
                raise TiebaError(error_message+"|"+verifycode)
            else:
                raise TiebaError(r.content)

    # def ding_tie(self, tie_url, content=None):
    #     print_message("正在回帖: "+ tie_url)
    #     if not content:
    #         content = get_random_sentense()
    #     for i in range(2):      # if not return true, it will try 2 times
    #         if self._ding_tie(tie_url, content):
    #             return True
            
    # @re_run(3, 30)
    def ding_ties(self, tie_urls, content=None):
        for url in tie_urls:
            self.ding_tie(url, content)

    def like_ba(self, name):
        r = self.session.get('http://tieba.baidu.com/f?ie=utf-8&kw='+name)
        if "喜欢本吧" in r.content:
            like_url = re.findall(u'right;"><a href="(.*?favolike.*?)"', r.content)[0]
            like_url = urlparse.urljoin('http://tieba.baidu.com/', like_url).replace('&amp;', '&')
            r = self.session.get(like_url)
            if "恭喜你成为本吧" in r.content:
                print "已加入%s吧会员" % name

def print_index(index, allstr):
    indexn = allstr.find(index)
    start = indexn - 300 if indexn-300>0 else 0
    end = indexn + 300
    return allstr[start:end]

def print_message(msg):
    print "%s: %s" % (get_cur_dt(), msg)

def get_random_sentense():
    return random.choice([
            '有人说我是来混经验的，卧槽 劳资反手就是一巴掌，你特么不是说废话么',
            '参加选秀金节目去吧！好歌曲等你来',
            '又是方言歌曲啊，无感',
            '现在这个社会就是这样的，太多虚假恶心',
            '哈哈，可以用普通话来唱骂，楼主快征集人来挑战不同方言吧',
            '听不懂，看不懂，不懂你，懂小姐，啊哈哈哈哈哈',
            '挺搞怪的，加油啊，湖南人顶一个',
            '看了你的豆瓣，近期没活动，可惜了',
            '现在还有越策越开心么',
            '妹陀之歌',
            '听着好像粤语啊，呵呵呵呵呵',
            '药别停',
            '还是喜欢四川方言',
            '有点模仿抄袭的感觉',
            '推荐湖南美食美女吧，别唱了',
            '你丫到底唱什么',
            '滚粗',
            '想听湖南方言唱 最炫民族风',
            '开始怀疑人生',
            '感动',
            '刘海砍樵咯',
            '湖南方言还是挺有特色的',
            '很酷，特别佩服湖南人的娱乐精神',
            '湖南出了好多歌唱家，李谷一啊，张也啊，宋祖英啊，希望你也加油',
            '民族的就是世界的！！！',
            '什么破玩意，傻逼',
            '马克！！！虽然没听懂',
            '不要侮辱了歌手这个行业，就你这样的也唱歌？照镜子去',
            '还是挺有感觉的，加油！歌词不错',
            '拍个视频吧，再跳个舞，火起来',
            '期待你更多的歌曲',
            # '虽然不知道楼主在说什么，但好像很厉害的样子。。。。。。。',
            # '以前不懂看贴总是不回，一直没提升等级和增加经验。。。',
            # '酱油在手，低头猛走，小手一提，经验带走。。。。。。。',
            # '默默地顶完贴转身就走，不求深藏功与名，只求前排混脸熟',
            # '顶顶顶顶顶顶顶顶顶顶顶顶顶顶顶顶顶顶顶顶顶顶顶顶顶顶顶顶顶顶顶顶顶顶顶',
            # '楼主挽尊',
            # '嗯，这是个好帖。',
            # '啊哈哈哈哈。长沙话呀，太有意思了。',
            # '听着还不错，就是像外国人唱歌一样，神马也听不懂。',
            # '哟活。长沙还有噶哈人才诶？',
            # '诶哟不错～',
            # '太好听了，民谣就是地带有地方特色才好～！',
            # '报道',
            # '火钳流明',
            # '听着很有意思的赶脚。',
            # '歌词真有意思',
            # '我要把这个帖子一直往上顶，往上顶！顶到所有人都看到为止！',
            ])
    

def post_verifycode(filepath, code=None):
    codetype = {
        "en": "1004",
        "cn": "2004",
        }
    try:
        r = requests.post(post_verifycode_url+"baike_code?type="+codetype[code], files={'code.png': open(filepath, 'rb')}, timeout=60)
    except Exception, e:
        raise
    return r.content

def post_wrong_verifycode(num):
    requests.post(post_verifycode_url+"baike_code_err", data={'err_id': num})

def get_cur_dt():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

class TiebaError(Exception):
    def __init__(self, message):
        self._message = message
        # Exception.__init__(self, "%s" % message)

    def __str__(self):
        return self._message
    
if __name__ == "__main__":
    tie_list = [
        'http://tieba.baidu.com/mo/q---1624A7231591D97C2DEA6D55F8DA2ABF%3AFG%3D1--1-3-0--2--wapp_1403074146412_130/m?kz=3047541207&is_bakan=0&lp=5010&pinf=1_2_0',
        'http://tieba.baidu.com/mo/q-63121d1141005dd3fdea6fd05093aff8.3.1403346562.1.V1JrTTJNDY1N--B67D4839CDC25AE7315DC4AC07229569%3AFG%3D1--1-3-0--2--wapp_1403344610000_245/m?kz=2981757492&lp=6000&pn=80&pinf=1_2_0',
        # 'http://tieba.baidu.com/mo/?kz=2987492&lp=6000&pn=80&pinf=1_2_0'
        ]
    tieba = Tieba('by_profession','asdfghjkl')
    # tieba = Tieba('a68327749','68327749')
    try:
        tieba.login()
    except TiebaError, e:
        print e
        # error_message = str(e)
        # if "帐号" in error_message:
            # print "write to database, said username not exist"
        sys.exit(0)
    tieba.answer_q('1495112238204630899', '你直接把歌词拿着搜一下不就找到了')
