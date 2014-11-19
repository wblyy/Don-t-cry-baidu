#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import traceback
import requests
from tieba import Tieba, TiebaError, get_random_sentense, print_message, rerun
from mydb import Tiedb
import json
import re
import random
from random import choice
from reg_test import Reg_test
from IP_test import Getmyip
import sys


reload(sys)
sys.setdefaultencoding("utf-8")
senten1 = [
    '好像在哪听过',
    '听过',
    '有点印象',
    '前几天还听过呢，记不太清',
    '哎，确实想知道是什么歌',
    '好像在哪个酒吧听过',
    '好像在丽江听哪个歌手唱过',
    '好像在电视里听过',
    '好像真的有印象耶',
    ]
senten2 = [
    '如果记得旋律的话可以用音乐雷达的哼唱识别功能试试',
    '有声音的话，可以下载音乐雷达的音乐识别',
    '用音乐雷达的哼唱识别功能看能不能找到这首歌',
    '这首歌用音乐雷达的声音识别看能不能找到',
    '用音乐雷达的声音识别看能找到吗',
    '好像音乐雷达有一个哼唱功能，哼出旋律就能识别歌曲',
    '好像音乐雷达有听歌识曲的功能，放出来就能识别歌曲',
    ]

senten3 = [
    '。',
    '。。',
    '。。。',
    '。。。。',
    '~_~',
    '~_~。',
    '~_~。。',
    ]

q_re = re.compile('<a href="(http://zhidao.baidu.com/question/\d+\.html)".*?<em>(.*?)</em></a>')

def yield_q():
    for i in range(0, 460, 10):
        msg = requests.get('http://zhidao.baidu.com/search?word=%D5%E2%CA%D7%B8%E8%BD%D0%CA%B2%C3%B4%C3%FB%D7%D6&ie=gbk&site=-1&sites=0&date=3&pn='+str(i)).content.decode('gbk')
        for row in re.findall(r'<a href="(http://zhidao.baidu.com/question/\d+\.html)".*?<em>(.*?)</em>.*?<dd class="dd summary">.*?</i>(.*?)</dd>', msg, re.DOTALL):
            yield [i.encode('utf8') for i in row]
            # yield row[0].encode('utf8'), row[1].encode('utf8')

def get_random_senten(insert=''):
    return '%s %s%s%s' % (choice(senten1), choice(senten2), insert, choice(senten3))

def get_cur_ts():
    return str(time.time()).replace('.', '0')

tiebadb = Tiedb()
tieba = Tieba('eternalcxx0302', 'yanhuai0202')
reg=Reg_test()
getmyip = Getmyip()
current_IP=getmyip.getip()
print 'current_IP:',current_IP
def answer_once(qid,content,current_user):
    try:
        # username, passwd = tiebadb.get_random_bd_user()
        # tieba = Tieba(username, passwd)
        # tieba.login()
        tieba.answer_q(qid, content)
        print '入库前：',qid, content,'et',current_IP
        tiebadb.save_question(qid, content,current_user,current_IP)
    except TiebaError, e:
        print 'Answer Failed'    

@rerun
def answer_search():
    #tieba = Tieba('eternalcxx0302', 'yanhuai0202')
    username, passwd = tiebadb.get_random_bd_user()
    tieba = Tieba(username, passwd)
    tieba.login()
    try:
        #tieba.login()
        switch_user=0
        p = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
        temp_word='确实挺熟悉的'
        for row in yield_q():
            #print 'switch_user'
            #temp_word='确实挺熟悉的'
            content=''
            senten=''
            senten_left=''
            senten_right=''
            #url_filter=[]
            qid = row[0][row[0].rfind('/')+1:row[0].rfind('.')]
            title = row[1]
            if tiebadb.is_q_shown(qid)[0]==1:
                switch_user=switch_user+1
                #print tiebadb.is_q_shown(qid)
                if switch_user%10==0:
                    print 'switch to another user....'
                    username, passwd = tiebadb.get_random_bd_user()
                    print_message('%s\t%s' % (username, passwd))
                    tieba = Tieba(username, passwd)
                    tieba.login()
                print row[2]
                con_fil=p.split(content+row[2])
                for con in con_fil:
                    content=content+con
                print content    
                similar_answer = reg.get_bing_similar(title,content)
                if similar_answer:
                    for hanzi in re.findall(ur"([\u4e00-\u9fa5]+)",similar_answer.decode('utf8')):
                        choose=random.randint(2,5)
                        if len(hanzi)%choose!=0 and len(senten_left)<20:
                            senten_left=senten_left+hanzi+','
                    senten=senten_left+senten1[random.randint(0,len(senten1))]+','+senten2[random.randint(0,len(senten2))]        
                    print "从bing中得到最佳答案：     "+senten  
                else:                
                    for hanzi in re.findall(ur"([\u4e00-\u9fa5]+)",temp_word.decode('utf8')):
                        choose=random.randint(2,5)
                        if len(hanzi)%choose!=0 and len(senten_left)<20:
                            senten_left=senten_left+hanzi+','
                        #print hanzi
                        #print "left:"+senten_left
                    senten=senten_left+senten1[random.randint(0,len(senten1))]+','+senten2[random.randint(0,len(senten2))]
                    #senten=senten[0:factor]+','+senten1[random.randint(0,4)]+','+senten2[random.randint(0,4)]+','+senten[factor]
                    print  "从bing总抓取答案失败，采用备选答案：        " +senten            
                answer_once(qid, senten,username)
                time.sleep(choice([10, 15])*10)
                temp_word=row[2]
            else:
                print tiebadb.is_q_shown(qid),'answered_before',qid
    except TiebaError, e:
        print 'Answer Failed'
        raise

# @rerun
def main():
    username, passwd = tiebadb.get_random_bd_user()
    print_message('%s\t%s' % (username, passwd))
    tieba = Tieba(username, passwd)
    try:

        
        q = tieba.get_questions()
        for row in q['data']['detail']:
            #username, passwd = tiebadb.get_random_bd_user()
            #print_message('%s\t%s' % (username, passwd))
            #tieba = Tieba(username, passwd)
            #tieba.login()
            # print row['title'].encode('utf8'), row['tagName'][0].encode('utf8')
            # continue
            if u'小时' in row['createTime']:
                return
            qid = row['qid'].encode('utf8')
            title = row['title'].encode('utf8')
            similar_answer = tieba.get_zhidao_similar(title)
            if similar_answer:
                answer = similar_answer.encode('utf8').replace('<font color="#C60A00">', '').replace('</font>', '')
                senten = answer# +',  也可以用音乐识别软件识别'
            else:
                senten = get_random_senten(choice(list(title.decode('utf8'))).encode('utf8'))
            # continue
            if not tiebadb.is_q_in(qid) and not '用户名' in title:
                answer_once(qid, senten)
    except TiebaError, e:
        print 'Answer Failed'
        raise

def get_tag():
    username, passwd = tiebadb.get_random_bd_user()
    print_message('%s\t%s' % (username, passwd))
    tieba = Tieba(username, passwd)
    try:
        tieba.login()
        tagdic = {}
        for i in xrange(0, 750, 25):
            q = tieba.get_questions(str(i))
            for row in q['data']['detail']:
                if row['tagName']:
                    tag = row['tagName'][0].encode('utf8')
                    tagdic[tag] = tagdic.get(tag, 0)+1
    except TiebaError, e:
        print e
    for row in sorted(tagdic.items(), key=lambda x: x[1], reverse=True):
        # print row
        print row[0], row[1]

def test():
    username, passwd = tiebadb.get_random_bd_user()
    print_message('%s\t%s' % (username, passwd))
    tieba = Tieba(username, passwd)
    try:
        tieba.login()
        q = tieba.get_zhidao_similar('这首歌叫什么名字', '在网上搜到的一个铃声，很好听，但是完全没有歌曲信息，我很想知道这首')
        print q.encode('utf8')
    except TiebaError, e:
        print e

if __name__ == "__main__":
    # main()
    # get_tag()
    # test()
    # yield_q()
    while True:
        answer_search()
