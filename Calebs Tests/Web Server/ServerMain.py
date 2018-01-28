import tornado.web
import tornado.ioloop
import tornado.websocket
import os

import Handlers as WH
from networktables import NetworkTables

#import py networktables bindings
import pynetworktables2js.tornado_handlers as networkTablesToJS

#default robotIP
robotIP = "127.0.0.1"

def InitNetworkTables():
    print("Connecting to network tables")
    NetworkTables.initialize(server=robotIP)

def ServerCreate():
    settings = {
        "static_path": os.path.join(os.path.dirname(__file__), "static")
    }
    #startup networkTables for networktables2js
    InitNetworkTables()

    app = tornado.web.Application(networkTablesToJS.get_handlers() + [
        (r"/", WH.DefaultHandler),
        (r"/EventHandler", WH.EventSocket)
    ],**settings)

    app.listen(8888)

    ioLoop = tornado.ioloop.IOLoop.current()


    #start processing loop
    ioLoop.start()

if __name__ == "__main__":
    ServerCreate()
