#coding: utf-8
import tornado.web
import tornado.websocket
from config import SITE,static_path

class Index(tornado.web.RequestHandler):
    def get(self):
        if self.get_cookie("nickname"):
            self.redirect('/room')
        else:
            self.render('templates/index.html', static=static_path)

    def post(self):
        if self.get_argument("nickname"):
            self.set_cookie("nickname",self.get_argument("nickname"))
            self.redirect("/room")
        else:
            self.redirect("/")
        


class RoomHandler(tornado.web.RequestHandler):
    def get(self):
        if not self.get_cookie("nickname"):
            self.redirect("/")
        self.render('templates/room.html', site=SITE, static=static_path)


class LogoutHandler(tornado.web.RequestHandler):
    def get(self):
        self.set_cookie("nickname", "")
        self.redirect("/")


class SocketHandler(tornado.websocket.WebSocketHandler):
    clients = set()
    messages = []

    def open(self):
        nick = self.get_cookie("nickname")
        for x in SocketHandler.clients:
            x.write_message('%s 来了'%nick)
        self.write_message('你好, %s！在线的人有%s'%(nick, ','.join([x.get_cookie("nickname") for x in SocketHandler.clients])))
        for x in SocketHandler.messages:
            self.write_message(x)

        SocketHandler.clients.add(self)

    def on_message(self, message):
        m = "%s:%s<br />"%(self.get_cookie("nickname").decode('utf-8'), message)
        SocketHandler.messages.append(m)
        SocketHandler.messages = SocketHandler.messages[-20:]
        for x in SocketHandler.clients:
            x.write_message(m)

    def on_close(self):
        name = self.get_cookie("nickname")
        SocketHandler.clients.remove(self)
        for x in SocketHandler.clients:
            x.write_message("%s 离开了<br />"%name)
