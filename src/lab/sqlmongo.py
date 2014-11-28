#!/bin/env python
# ^_^ encoding: utf-8 ^_^
# @date: 14/11/28

__author__ = 'icejoywoo'

import sqlparse
import sqlparse.sql
from sqlparse import tokens


sql = """
select * from (select * from foo) where a = 1 and b != "xx" or
    uid in (select uid from bar where _ = ISODate("2014-11-19"))
"""

sql = 'select * from foo, bar where a = 1 and b != "xx" and uid in ("1", "2")'

parsed = sqlparse.parse(sql)


def is_subselect(parsed):
    if not parsed.is_group():
        return False
    for i in parsed.tokens:
        if i.ttype is tokens.DML and i.value.upper() == 'SELECT':
            return True
    return False


def is_where(parsed):
    if isinstance(parsed, (sqlparse.sql.Where, )):
        return True
    else:
        return False


query = {}
fields = {}
dbs = []

for item in parsed:
    from_seen = False
    select_seen = False
    # print item.tokens
    for t in item.tokens:
        if is_subselect(t):
            print t.tokens
        if is_where(t):
            print t.tokens
            # 跳过第一个where关键字
            for t in t.tokens[1:]:
                if t.is_whitespace():
                    continue
                # and, or
                if t.ttype is tokens.Keyword:
                    print t
                if isinstance(t, sqlparse.sql.Comparison):
                    print t.tokens

        if from_seen:
            if isinstance(t, sqlparse.sql.Identifier):
                db = t.get_name()
                dbs.append(db)
                from_seen = False
            if isinstance(t, sqlparse.sql.IdentifierList):
                for identifier in t.get_identifiers():
                    dbs.append(identifier.get_name())
                from_seen = False

        # update flags
        if t.ttype is tokens.Keyword and t.value.upper() == 'FROM':
            from_seen = True
        if t.ttype is tokens.DML and t.value.upper() == 'SELECT':
            select_seen = True

print dbs
