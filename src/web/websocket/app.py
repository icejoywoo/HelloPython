#!/bin/env python
# ^_^ encoding: utf-8 ^_^
# @date: 2015/7/21

__author__ = 'wujiabin'

import os
import sys
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.websocket
from tornado.options import define, options

# 为了避免编码错误的问题
reload(sys)
sys.setdefaultencoding("utf-8")

define("port", default=8888, help="listen on the given port", type=int)


class EchoWebSocket(tornado.websocket.WebSocketHandler):
    def open(self):
        print("WebSocket opened")

    def on_message(self, message):
        self.write_message(u"You said: " + message)

    def on_close(self):
        print("WebSocket closed")


# urls routers config
url_routers = [
    (r"^/websocket$", EchoWebSocket),
]

# tornado config
settings = {
    "cookie_secret": "35ehsFuYh7EQn42XdTP1o/VooETzKXQAFaYdkL5gEmG=",
    "template_path": os.path.join(os.path.dirname(__file__), "templates"),
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
}


if __name__ == "__main__":
    # http://localhost:8888/static/index.html
    application = tornado.web.Application(url_routers, **settings)
    tornado.options.parse_command_line(sys.argv)
    http_server = tornado.httpserver.HTTPServer(application, xheaders=True)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
