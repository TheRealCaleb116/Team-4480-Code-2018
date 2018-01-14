import tornado.web
import tornado.ioloop
import tornado.websocket

import Handlers as WH

def CheckEvents():
    pass

def ServerCreate():
    app = tornado.web.Application([
        (r"/", WH.defaultHandler),
        (r"/eventHandler",WH.EventSocket)
    ])
    app.listen(8888)

    ioLoop = tornado.ioloop.IOLoop.current()

    #run this function every 1000ms
    ioLoop.PeriodicCallback(CheckEvents,1000)

    #start processing loop
    ioLoop.start()

if __name__ == "__main__":
    ServerCreate()
