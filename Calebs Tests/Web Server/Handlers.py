import tornado.web
import tornado.websocket

class defaultHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("Web/index.html")

class EventSocket(tornado.websocket.WebSocketHandler):
    def open(self):
        print("The event handler Web Socket is open.")
        while True:
            msg = raw_input(">>:")
            self.write_message(msg)
    def close(self):
        print("The event handler Web Socket is closed")
