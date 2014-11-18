 # encoding: UTF-8
import re
import urllib2
import urllib
import time
from mydb import Tiedb
tiebadb = Tiedb()

for shown in tiebadb.is_q_shown_detected():
    print shown[0]
    print shown[1]
#ques_stat=','.join(str(i) for i in tiebadb.is_q_shown_detected())
#print ques_stat.split(',')

#userNameEnc:"
#",user:
