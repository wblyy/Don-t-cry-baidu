 # encoding: UTF-8
import re
import urllib2
import urllib
import time
from mydb import Tiedb
tiebadb = Tiedb()

while True:
	time.sleep(1800)
	try:	
		for shown in tiebadb.is_q_shown_detected():
			is_user_exist=False
    		print 'qid:',shown[0]
    		print 'time:',shown[1]
    		question_url='http://zhidao.baidu.com/question/'+shown[0]+'.html'
    		msg=urllib2.urlopen(question_url).read()
    		users=re.findall('userNameEnc:"(.*?)",user:'.decode('utf-8').encode('utf-8'), msg, re.DOTALL)
  	    	for user in users:
    			if(tiebadb.is_user_exist()):
    				tiebadb.update_q_shown(shown[0])
	    			tiebadb.update_q_shown_avaliable(shown[0],user)
	    			is_user_exist=True
	   	if(!is_user_exist):
	    	tiebadb.update_q_not_shown(shown[0])

	except Exception, e:
		time.sleep(5)
		print e
#ques_stat=','.join(str(i) for i in tiebadb.is_q_shown_detected())
#print ques_stat.split(',')

#userNameEnc:"
#",user:
