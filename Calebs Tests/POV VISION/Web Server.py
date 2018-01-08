import tornado.web
import tornafo.ioloop
import tornado.websocket

#import the handler classes

import WebServerHandlers as WH

def ServerCreate():
    application = tornado.web.Application([
        (r"/", WH.defaultHandler)
    ])

    application.listen(8888)
    tornado.ioloop.IOLoop.current().start()

if __name__ == "__main__":
    ServerCreate()
