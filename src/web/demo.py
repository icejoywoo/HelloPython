#!/bin/env python
# ^_^ encoding: utf-8 ^_^
# @author: icejoywoo
# @date: 12-11-15

import web


urls = (
    '/', 'index',
    '/a', 'xxx',
)


class index:
    def GET(self):
        import time

        time.sleep(100)
        return "Hello, World!"


class xxx:
    def GET(self):
        print web.ctx.ip
        print web.ctx.env
        return "Hello, World!"


app = web.application(urls, globals())
render = web.template.render('templates/')

if __name__ == "__main__":
    app.run()
