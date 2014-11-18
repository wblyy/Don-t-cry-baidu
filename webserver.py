# -*- coding: utf-8 -*-

import os
import time
import re
import requests
import functools
from urlparse import urlparse

import tornado
import tornado.ioloop
import tornado.httpserver
import tornado.web
from tornado.escape import json_encode

from mydb import Tiedb

from tornado.options import define, options
define("port", default=1028, help="run on the given port", type=int)


def administrator(method):
    """Decorate with this method to restrict to site admins."""
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        if not self.get_current_user():
            raise tornado.web.HTTPError(403)
        else:
            return method(self, *args, **kwargs)
    return wrapper

class Application(tornado.web.Application):
    def __init__(self):
        static_path = os.path.join(os.path.dirname(__file__), "static")
        settings = {
            "cookie_secret": 'fjdkals;jfl;asjdfkl;jasd;jfl;dkalsjweurpq',
            "debug": False,
            }
        handlers = [
            (r"/?$", TestHandler),
            (r"/submit?$", PostdataHandler),
            (r"/del?$", DelHandler),
            (r"/ties?$", TieHandler),
            (r"/login?$", LoginHandler),
            (r"/logout$", LogoutHandler),
            # (r"/submiturl/?$", SubmitHandler),
            (r'/static/(.*)', tornado.web.StaticFileHandler, {'path': static_path}),
            ]
        tornado.web.Application.__init__(self, handlers, **settings)

class BaseHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return Tiedb.instance()

    def get_current_user(self):
        return self.get_secure_cookie("user")

    def set_current_user(self, user):
        if user:
            self.set_secure_cookie("user", tornado.escape.json_encode(user))
        else:
            self.clear_cookie('user')

class TestHandler(BaseHandler):
    @administrator
    def get(self):
        self.write("It works!")

class DelHandler(BaseHandler):
    @administrator
    def get(self):
        tieid = self.get_argument("tieid", default=None, strip=False)
        if tieid:
            self.db.deltie(tieid)
            self.redirect("/tie")
        else:
            self.write("error")

class PostdataHandler(BaseHandler):
    @administrator
    def get(self):
        tieid = self.get_argument("tieid", default=None, strip=False)
        if tieid:
            tie = self.db.get_tie
            row = []
            rows = self.db.get_tie(tieid)
            row.append(rows[0][0])
            row.append(rows[0][1])
            row.append('\r\n'.join([s[2] for s in rows]))
            row.append(rows[0][3])
            self.render("template/submit.html", row=row)
        else:
            self.render("template/submit.html", row=None)

    @administrator
    def post(self):
        editid = self.get_argument("tieid", default=None, strip=False)
        marks = self.get_argument("marks", default=None, strip=False)
        sentens = self.get_argument("sentens", default=None, strip='\r\n')
        # if no editid mean insert new tiezi, then insert new tiezi first
        if editid:
            tieid = editid
        else:
            posturl = self.get_argument("tieurl", default=None, strip=False)
            tieurl = urlparse(posturl).path
            tieid = tieurl[tieurl.rfind('/')+1:]
            title = re.findall('<title>(.*?)</title>', requests.get('http://tieba.baidu.com/p/'+tieid).content.decode('gbk'))
            if title and len(title[0].split('_'))==3:
                self.db.insert_tiezi(tieid, title[0].split('_')[0], title[0].split('_')[1].replace(u"吧", ""), marks)
            else:
                raise tornado.web.HTTPError(500)
        self.db.update_marks(tieid, marks)
        self.db.del_sentens(tieid)
        for s in set(sentens.split("\r\n") if "\r\n" in sentens else sentens.split("\n")):
            if s.replace(" ", ""):
                self.db.insert_senten(tieid, s)
        self.redirect('/tie')
            
class TieHandler(BaseHandler):
    def get(self):
        ties = self.db.get_ties()
        self.render('./template/ties.html', ties=ties)

class LoginHandler(BaseHandler):
    def get(self):
        self.render('./template/login.html')

    def post(self):
        username = self.get_argument("user", default=None, strip=False)
        passwd = self.get_argument("passwd", default=None, strip=False)        
        if username == "baidu" and passwd == "tieba,robot":
            self.set_current_user(username)
            self.redirect("/ties")
        else:
            self.write('Error!')

class LogoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie("user")
        self.redirect("/ties")
                            
def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port, address='0.0.0.0')
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()    
