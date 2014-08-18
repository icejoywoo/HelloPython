#!/bin/env python
# ^_^ encoding: utf-8 ^_^
# @date: 2014/8/18

__author__ = 'wujiabin'

import sqlite3
import pickle
import collections


class DBDict(collections.MutableMapping):
    """Database driven dictlike object (with non-persistent in-memory option).
        >>> d = DBDict(raymond='red', rachel='blue')
        >>> d
        {'rachel': 'blue', 'raymond': 'red'}
        >>> d['critter'] = ('xyz', [1,2,3])
        >>> d['critter']
        ('xyz', [1, 2, 3])
        >>> len(d)
        3
        >>> list(d)
        ['rachel', 'raymond', 'critter']
        >>> d.keys()
        ['rachel', 'raymond', 'critter']
        >>> d.items()
        [('rachel', 'blue'), ('raymond', 'red'), ('critter', ('xyz', [1, 2, 3]))]
        >>> d.values()
        ['blue', 'red', ('xyz', [1, 2, 3])]
    """

    def __init__(self, db_filename=':memory:', **kwds):
        self.db = sqlite3.connect(db_filename)
        self.db.text_factory = str
        try:
            self.db.execute('CREATE TABLE dict (key text PRIMARY KEY, value text)')
            self.db.execute('CREATE INDEX key ON dict (key)')
            self.db.commit()
        except sqlite3.OperationalError:
            pass                # DB already exists
        self.update(kwds)

    def __setitem__(self, key, value):
        if key in self:
            del self[key]
        value = pickle.dumps(value)
        self.db.execute('INSERT INTO dict VALUES (?, ?)', (key, value))
        self.db.commit()

    def __getitem__(self, key):
        cursor = self.db.execute('SELECT value FROM dict WHERE key = (?)', (key,))
        result = cursor.fetchone()
        if result is None:
            raise KeyError(key)
        return pickle.loads(result[0])

    def __delitem__(self, key):
        if key not in self:
            raise KeyError(key)
        self.db.execute('DELETE FROM dict WHERE key = (?)', (key,))
        self.db.commit()

    def __iter__(self):
        return iter([row[0] for row in self.db.execute('SELECT key FROM dict')])

    def __repr__(self):
        list_of_str = ['%r: %r' % pair for pair in self.items()]
        return '{' + ', '.join(list_of_str) + '}'

    def __len__(self):
        return len(list(iter(self)))

if __name__ == "__main__":
    d = DBDict(db_filename='sqlite3.db')
    d.update(dict(zip(("key_%d" % i for i in xrange(1000)), ("value_%d" % i for i in xrange(1000)))))
    print d
    from profile import run
    run('for ii in xrange(1000): x = d["key_%d" % ii]')
