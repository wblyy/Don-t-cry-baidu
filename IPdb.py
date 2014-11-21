#coding=utf-8
import random
import MySQLdb
import sys

class Mydb(object):
    def __init__(self, user, passwd, dbname):
        self._id = 0           # use in pop function
        self.user = user
        self.passwd = passwd
        self.dbname = dbname

    @property
    def db(self):
        return MySQLdb.connect("54.223.153.21", self.user, self.passwd, self.dbname, charset='utf8')

    @classmethod
    def instance(cls):
        if not hasattr(cls, "_instance"):
            cls._instance = cls()
        return cls._instance

    def _execute(self, *args, **kwargs):
        conn = self.db
        cur = conn.cursor()
        cur.execute(*args, **kwargs)
        conn.commit()

    def _query_row(self, *args):
        conn = self.db
        cur = conn.cursor()
        cur.execute(*args)
        rows = cur.fetchone()
        return rows

    def _query_rows(self, *args):
        conn = self.db
        cur = conn.cursor()
        cur.execute(*args)
        rows = cur.fetchall()
        return rows    

class IPdb(Mydb):
    def __init__(self):
        Mydb.__init__(self, 'root', '654321', 'proxy_service')
    def get_IP(self):
        return self._query_rows("select * from proxy order by id desc")
    def get_fast_IP(self):
        return self._query_rows("select ip,port from proxy where delay_time<200")
    def get_tie(self, tieid):
        return self._query_rows("select t.baname, t.tieid, s.senten, t.marks from sentens s left join ties t on s.tieid=t.tieid where t.tieid=%s", (tieid,))

        
if __name__ == "__main__":
    mydb = IPdb()
    # for row in mydb.get_random_rows(100, "%gmail.com"):
        # print row
    # sys.exit(0)
<<<<<<< HEAD
    for IP in mydb.get_fast_IP():
        print str(IP[0])+':'+str(IP[1])

=======
    print mydb.get_fast_IP()
>>>>>>> origin/master
    
