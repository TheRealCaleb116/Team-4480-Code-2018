import tornado.web
import tornado.ioloop
import tornado.websocket

import Handlers as WH

def ServerCreate():
    app = tornado.web.Application([
        (r"/", WH.defaultHandler),
        (r"/eventHandler",WH.EventSocket)
    ])
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()

if __name__ == "__main__":
    ServerCreate()
