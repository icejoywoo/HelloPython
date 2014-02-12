#!/bin/env python
# ^_^ encoding: utf-8 ^_^
# @date: 14-1-21

__author__ = 'icejoywoo'

from flask import render_template


@app.errorhandler(404)
def internal_error(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500
