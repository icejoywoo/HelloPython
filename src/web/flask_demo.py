#!/bin/env python
#^_^ encoding: utf-8 ^_^
# @date: 14-1-20

__author__ = 'wujiabin'

from flask import abort
from flask import Flask
from flask import make_response
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from werkzeug import secure_filename

app = Flask(__name__)

# set the secret key.  keep this really secret:
# import os; os.urandom(24)
app.secret_key = '\xc4\xda\xc2\x0b\xa2\xf7\x07\xbb\x9df3a\xad<\x85\x95\xd0\x07\xef\x0b\n\x05PU'


# error pages config
@app.errorhandler(404)
def page_not_found(error):
    resp = make_response(render_template('page_not_found.html'), 404)
    resp.headers['X-Something'] = 'A value'
    return resp


@app.route('/404')
def _404():
    abort(404)


@app.route("/")
def index():
    # username = request.cookies.get("username")
    username = None
    if 'username' in session:
        username = session["username"]
    return render_template("hello.html", name=username)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('index'))
    return '''
        <form action="" method="post">
            <p><input type=text name=username>
            <p><input type=submit value=Login>
        </form>
    '''


@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))


@app.route("/hello")
def hello():
    return "Hello World!"


@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    resp = make_response(render_template("hello.html", name=username))
    resp.set_cookie("username", username)
    return resp


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


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        f.save(secure_filename(f.filename))
        return redirect(url_for("upload_file"))
    elif request.method == 'GET':
        return '''
        <!doctype html>
        <title>Upload new File</title>
        <h1>Upload new File</h1>
        <form action="%s" method="post" enctype="multipart/form-data">
          <p><input type="file" name="file">
             <input type="submit" value="Upload">
        </form>
        ''' % url_for("upload_file")


if __name__ == "__main__":
    # host = '0.0.0.0'
    app.run(debug=True, use_debugger=True, use_reloader=True)
