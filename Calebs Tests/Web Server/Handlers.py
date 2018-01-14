import tornado.web
import tornado.websocket

class DefaultHandler(tornado.web.RequestHandler):
    def Get(self):
        self.render("Web/index.html")

class EventSocket(tornado.websocket.WebSocketHandler):
    def Open(self):
        print("The event handler Web Socket is open.")
        while True:
            msg = raw_input(">>:")
            self.write_message(msg)
    def Close(self):
        print("The event handler Web Socket is closed")
