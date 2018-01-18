import tornado.web
import tornado.ioloop
import tornado.websocket
import os

import Handlers as WH

def CheckEvents():
    pass

def ServerCreate():
    settings = {
        "static_path": os.path.join(os.path.dirname(__file__), "static")
    }

    app = tornado.web.Application([
        (r"/", WH.DefaultHandler),
        (r"/EventHandler", WH.EventSocket)
    ],**settings)

    app.listen(8888)

    ioLoop = tornado.ioloop.IOLoop.current()

    #run this function every 1000ms
    #ioLoop.PeriodicCallback(CheckEvents,1000)

    #start processing loop
    ioLoop.start()

if __name__ == "__main__":
    ServerCreate()
