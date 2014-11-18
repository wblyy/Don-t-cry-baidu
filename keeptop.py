#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import re
import time
import traceback
import requests
from tieba import Tieba, TiebaError, get_random_sentense, print_message
from mydb import Tiedb

tie_url = "http://tieba.baidu.com/p/"
ba_url = "http://tieba.baidu.com/mo/q---1624A7231591D97C2DEA6D55F8DA2ABF%3AFG%3D1--1-3-0--2--wapp_1403864988809_638/m?kw="
pc_ba_url = "http://tieba.baidu.com/f?ie=utf-8&kw="

tiebadb = Tiedb()

def ding_tie(tie_dic, username, passwd):
    for k in tie_dic:
        totalcount = re.findall(ur'3px">(.*?)</span>回复贴'.encode('utf-8'),
                         requests.get(tie_url+k).content.decode('gbk').encode('utf-8'))
        # print k, totalcount, "......................"
        if totalcount:
            tiebadb.update_tie_total_count(k, totalcount[0])
        r = requests.get(pc_ba_url+tie_dic[k])
        if k in r.content:
            # print_message('It is on the top\t'+tie_url+k)
            tiebadb.update_tie_status(k, "在首页")
        else:
            tieba = Tieba(username, passwd)
            try:
                tieba.login()
            except TiebaError, e:
                print e
                return False
            tieba.like_ba(tie_dic[k])
            content = tiebadb.get_radom_senten(k)
            try:
                if tieba.ding_tie(tie_url+k, content):
                    print "ding count +1"
                    tiebadb.update_tie_dingcount(k)
                    tiebadb.set_statue(username, "1")
                tiebadb.update_tie_status(k, "在首页")
            except Exception, e:
                # print traceback.format_exc()
                error_message = str(e)
                print "顶贴失败， 错误信息：", error_message
                if "不存在" in error_message:
                    tiebadb.update_tie_status(k, "帖子已被删除")
                elif "验证码" in error_message:
                    verifycode = error_message[error_message.find('|')+1:]
                    if verifycode == "-1":
                        tiebadb.update_tie_status(k, "验证码返回: -1")                    
                elif "您帐号异常" in error_message:
                    tiebadb.set_statue(username, "4")
                elif "baike_code?type" in error_message:
                    tiebadb.update_tie_status(k, "无法识别验证码")
                else:           # 如果不是帖子被删，验证码错误，账号被封，那只能是改了密码或者
                    tiebadb.update_tie_status(k, "顶贴失败")
                            # 或者回话过期，你确实是登录状态，但你要执行某些操作时需要重新登录，譬如顶贴
                    # tiebadb.set_statue(username, "3")

if __name__ == "__main__":
    # tie_dic = {
        # "3144094773": "长沙",
        # "3142735074": "湖南",
        # }
    tie_dic = {}
    for row in tiebadb.get_dingties():
        tie_dic[row[0].encode('utf-8')] = row[1].encode('utf-8')
    username, passwd = tiebadb.get_random_bd_user()
    print_message('%s\t%s' % (username, passwd))
    ding_tie(tie_dic, username, passwd)
