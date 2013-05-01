import tornado.web
import tornado.ioloop
from views import *
import config



if __name__ == "__main__":
    app = tornado.web.Application([
        ('/', Index),
        ('/room', RoomHandler),
        ('/socket', SocketHandler),
        ('/logout', LogoutHandler)],
        static_path=config.static_path)
    app.listen(8000)
    tornado.ioloop.IOLoop.instance().start()
