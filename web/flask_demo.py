#!/bin/env python
#^_^ encoding: utf-8 ^_^
# @date: 14-1-20

__author__ = 'wujiabin'

from flask import Flask
app = Flask(__name__)


@app.route("/")
def index():
    return "Index page."

@app.route("/hello")
def hello():
    return "Hello World!"

@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return 'User %s' % username

@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return 'Post %d' % post_id

@app.route('/projects/')
def projects():
    return 'The project page'

@app.route('/about')
def about():
    return 'The about page'

if __name__ == "__main__":
    app.run(debug=True, use_debugger=True, use_reloader=True)