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
        return MySQLdb.connect("localhost", self.user, self.passwd, self.dbname, charset='utf8')

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

class Tiedb(Mydb):
    def __init__(self):
        Mydb.__init__(self, 'root', '654321', 'tiedb')
    def insert_tiezi(self, tieid, tietitle, baname, marks):
        self._execute('insert ignore ties (tieid, tietitle, baname, insertime, marks) values (%s, %s, %s, NOW(), %s)', (tieid, tietitle, baname, marks))

    def insert_senten(self, tieid, senten):
        self._execute('insert ignore sentens (tieid, senten) values (%s, %s)', (tieid, senten))
    def get_ties(self):
        return self._query_rows("select baname, tieid, tiestatus, tietitle, id, lastdingtime, dingcount, totalcount from ties order by id desc")
    def get_tie(self, tieid):
        return self._query_rows("select t.baname, t.tieid, s.senten, t.marks from sentens s left join ties t on s.tieid=t.tieid where t.tieid=%s", (tieid,))

    def deltie(self, tieid):
        self._execute("delete from sentens where tieid=%s", (tieid,))    
        self._execute("delete from ties where tieid=%s", (tieid,))    
    def del_sentens(self, tieid):
        self._execute("delete from sentens where tieid=%s", (tieid,))
    def get_dingties(self):
        # return self._query_rows("select tieid, baname from ties where tiestatus <> %s", ("帖子已被删除",))
        return self._query_rows("select tieid, baname from ties")
    def update_tie_dingcount(self, tieid):
        self._execute("update ties set dingcount=dingcount+1, totalcount=totalcount+1,lastdingtime=NOW() where tieid=%s", (tieid, ))
    def update_tie_total_count(self, tieid, c):
        self._execute("update ties set totalcount=%s where tieid=%s", (c, tieid))
    def update_tie_status(self, tieid, sta):
        self._execute("update ties set tiestatus=%s where tieid=%s", (sta, tieid))
    def update_marks(self, tieid, marks):
        self._execute("update ties set marks=%s where tieid=%s", (marks, tieid))
    def get_radom_senten(self, tieid):
        rows = self._query_rows('select id from sentens where tieid=%s', (tieid,))
        rows = [row[0] for row in rows]
        random_id = random.sample(rows, 1)
        # print str(random_id)
        row = self._query_row('select senten from sentens where id=%s', (str(random_id[0]), ))
        return row[0].encode('utf-8')
    def add_user(self, username, passwd, email):
        self._execute("insert ignore users (username, passwd, email) values (%s, %s, %s)", (username, passwd, email))

    def add_bd_user(self, username, passwd, email):
        self._execute("insert ignore bdusers (username, passwd, email) values (%s, %s, %s)", (username, passwd, email))

    def set_statue(self, username, status):
        self._execute("update bdusers set ustatus=%s where username=%s", (status, username))                

    def get_random_bd_user(self):
        rows = self._query_rows('select id from bdusers where ustatus=1')
        rows = [row[0] for row in rows]
        random_id = random.sample(rows, 1)
        # print str(random_id)
        row = self._query_row('select username, passwd from bdusers where id=%s', (str(random_id[0]), ))
        return [i.encode('utf-8') for i in row]
    
    def save_q(self, qid, senten):
        self._execute("insert zhidao (qid, senten) values (%s, %s)", (qid, senten))
    def save_question(self,qid,senten,answered_user,related_IP):
        self._excute("insert zhidao (qid, senten,answered_user,related_IP) values (%s,%s,%s,%s)",(qid, senten,answered_user,related_IP))

    def is_q_in(self, qid):
        if self._query_row('select id from zhidao where qid=%s', (qid, )):
            return True     
        return False



    def is_q_shown(self, qid):
        if self._query_row('select is_shown from zhidao where qid=%s', (qid, ))>=2:
        #规定0状态是未知，1状态是未显示，2状态是已显示，3状态是显示的是当前状态的信息
            return True
        return False

    def is_q_shown_detected(self):
        #从数据库中获取is-shown状态未知的 qid以及时间
        return self._query_row('select qid, inserted,from zhidao where is_shown=0')

    def update_q_shown(self,qid):
        #将所有有显示的置为2
        self._query_row('update zhidao set is_shown=2 where qid=%s',(qid, ))

    def update_q_shown_avaliable(self,qid,answered_user):
        #将正确post上去的这位同志置为3
        self._query_row('update zhidao set is_shown=3 where qid=%s and answered_user=%s',(qid,answered_user))

    def evaluate(self,inserted):
        #抽取特定时间段以后的回复情况进行水态评估
        self._query_row('select * from zhidao where inserted>%s',(inserted, ))


class csdndb(Mydb):
    def __init__(self):
        Mydb.__init__(self, 'root', '654321', 'csdn')

    def insert_data(self, username, passwd, email):
        self._execute('insert ignore users (username, passwd, email) values (%s, %s, %s)', (username, passwd, email))

    def get_recond_by_id(self, rid):
        return self._query_row('select * from users where id=%s', (rid,))

    def pop(self):
        rows = self._query_row('select username, passwd from users limit %s,1', (self._id,))
        self._id += 1
        if rows:
            return rows
        else:
            raise StopIteration
        
    def get_random_rows(self, n, wherecase=None):
        if wherecase:
            # rows = self._query_rows('select c.id from csdn.users c inner join xiaomi.xiaomi_com m on c.email=m.email and c.email like %s', (wherecase, ))
            rows = self._query_rows('select id from users where length(username)between 6 and 15 and email like %s', (wherecase, ))
        else:
            rows = self._query_rows('select c.id from csdn.users c inner join xiaomi.xiaomi_com m on c.email=m.email')
            # rows = self._query_rows('select id from myusers.users where length(username) between 6 and 15')
            # rows = self._query_rows('select id from users where length(username)between 6 and 15')
        rows = [row[0] for row in rows]
        random_ids = random.sample(rows, n)
        return self._query_rows('select username, passwd, email from users where id in ('+','.join(['%s']*len(random_ids))+')', tuple(random_ids))

class myuserdb(Mydb):
    def __init__(self):
        Mydb.__init__(self, 'root', '654321', 'myusers')

class xiaomidb(Mydb):
    def __init__(self):
        Mydb.__init__(self, 'root', '654321', 'xiaomi')
    def get_user_by_passwd(self, passwd):
        return self._query_row('select username, email from xiaomi_com where password=%s', (passwd, ))
        
if __name__ == "__main__":
    mydb = Tiedb()
    # for row in mydb.get_random_rows(100, "%gmail.com"):
        # print row
    # sys.exit(0)
    print mydb.get_ties()
    sys.exit(0)
    with open('./csdn.csv', 'r') as f:
        for line in f:
            row = line.strip('\r\n').split(' # ')
            print '\t'.join(row)
            mydb.insert_data(row[0], row[1], row[2])
