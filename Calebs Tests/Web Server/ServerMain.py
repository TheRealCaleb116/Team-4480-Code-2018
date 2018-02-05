import tornado.web
import tornado.ioloop
import tornado.websocket
import os

import Handlers as WH
from networktables import NetworkTables

#import py networktables bindings
import pynetworktables2js.tornado_handlers as networkTablesToJS

from multiprocessing import Process, Queue
import RobotChecker as RC
#default robotIP
robotIP = "127.0.0.1"

def InitNetworkTables():
    print("Connecting to network tables")
    NetworkTables.initialize(server=robotIP)

def StartRobotChecker():
    global Q
    Q = Queue()

    robotChecker = Process(target=RC.Start,args=(robotIP,Q))
    #Start the sub process
    robotChecker.start()

def SubCheck():
    if (Q.empty() == False):
        
        for x in range(0, Q.qsize()):
            msg = Q.get()
            WH.EventSocket.AlertClients(msg)

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

    #start up robotchecker subprocess
    StartRobotChecker()

    ioLoop = tornado.ioloop.IOLoop.current()

    tornado.ioloop.PeriodicCallback(SubCheck,1000).start()


    #start processing loop
    ioLoop.start()

if __name__ == "__main__":
    ServerCreate()
