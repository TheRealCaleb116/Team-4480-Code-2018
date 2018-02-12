import tornado.web
import tornado.websocket


class DefaultHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")

class EventSocket(tornado.websocket.WebSocketHandler):


    eSockets = set()

    def open(self):
        print("The event handler Web Socket is open.")
        self.eSockets.add(self)

    def close(self):
        print("The event handler Web Socket is closed")
        self.eSockets.remove(self)


    @classmethod
    def AlertClients(cls, label, value):
        #send event to all open clients
        for socket in cls.eSockets:
            Socket.write_message(label + ":" + value)
