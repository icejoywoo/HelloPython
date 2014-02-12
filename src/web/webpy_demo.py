#!/bin/env python
# ^_^ encoding: utf-8 ^_^
# @date: 12-11-15

__author__ = 'icejoywoo'

import web


urls = (
    '/', 'index',
    '/add', 'add',
    '/upload', 'upload'
)


class index:
    def GET(self):
        todos = db.select('todo')
        return render.index(todos)


class add:
    def POST(self):
        i = web.input()
        n = db.insert('todo', id=i.id, title=i.title)
        raise web.seeother('/')


class upload:
    def POST(self):
        x = web.input(myfile={})
        filedir = '.' # change this to the directory you want to store the file in.
        if 'myfile' in x: # to check if the file-object is created
            filepath = x.myfile.filename.replace('\\', '/') # replaces the windows-style slashes with linux ones.
            filename = filepath.split('/')[-1] # splits the and chooses the last part (the filename with extension)
            fout = open(filedir + '/' + filename, 'wb') # creates the file where the uploaded file should be stored
            fout.write(x.myfile.file.read()) # writes the uploaded file to the newly created file.
            #            fout.write(x.myfile.value) # writes the uploaded file to the newly created file.
            fout.close() # closes the file, upload complete.
        raise web.seeother('/')


app = web.application(urls, globals())
render = web.template.render('templates/')
#db = web.database(dbn='sqlite', db=":memory:")
db = web.database(dbn='sqlite', db="sqlite.db")

conn = db._db_cursor().connection
cursor = conn.cursor()
cursor.execute('DROP TABLE todo')
cursor.execute('''
CREATE TABLE todo (
    id text primary key,
    title text,
    created timestamp,
    done boolean
)
''')

cursor.execute('''
INSERT INTO todo (id, title) VALUES ('01', 'Learn web.py')
''')

cursor.execute('''
INSERT INTO todo (id, title) VALUES ('02', 'Learn python')
''')

conn.commit()

if __name__ == "__main__":
    app.run()
