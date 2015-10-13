#!/bin/env python
# ^_^ encoding: utf-8 ^_^
# @author: icejoywoo
# @date: 2014/11/28

import sqlparse
from sqlparse.sql import IdentifierList, Identifier
from sqlparse.tokens import Keyword, DML, Group


# simple find
spec = {}
fields = {'_id': False}  # 默认_id会被返回, 进行屏蔽
# 是否是explain
is_explain = False

# SQL语句基本可以分解成下面7大块：
# (5)SELECT (6)DISTINCT < select list >
# (1)FROM < table source > 可以有subquery
# (2)WHERE < condition > 可以有subquery
# (3)GROUP BY < group by list >
# (4)HAVING < having condition >
# (7) ORDER BY < order by list >


# 暂时不支持聚合函数和group by
sql = "select _id, sum(*) from foo, bar where foo.id = bar.id and uid in (select uid from t);"
sql = "select id from foo where x = 1;"


def is_subselect(parsed):
    """ 判断是否为子查询
    """
    if not parsed.is_group():
        return False
    for item in parsed.tokens:
        if item.ttype is DML and item.value.upper() == 'SELECT':
            return True
    return False


def is_wheregroup(parsed):
    if not parsed.is_group():
        return False
    for item in parsed.tokens:
        if item.ttype is Group.Where:
            return True
    return False


for i in sqlparse.parse(sql):
    # 判断是否有explain, keyword里面没有这个, 单独处理一下
    if i.token_first().to_unicode().lower() == u"explain":
        is_explain = True

    print dir(i.tokens[-1])

    from_seen = False
    where_seen = False
    print i.tokens
    for t in i.tokens:
        if from_seen:
            if is_subselect(t):
                print t
        if t.ttype is Keyword and t.value.upper() == 'FROM':
            from_seen = True

        if is_wheregroup(t):
            where_seen = True
            print t


print is_explain

sql = """
select K.a,K.b from (select H.b from (select G.c from (select F.d from
(select E.e from A, B, C, D, E), F), G), H), I, J, K order by 1,2;
"""


def extract_from_part(parsed):
    from_seen = False
    for item in parsed.tokens:
        if from_seen:
            if is_subselect(item):
                for x in extract_from_part(item):
                    yield x
            elif item.ttype is Keyword:
                raise StopIteration
            else:
                yield item
        elif item.ttype is Keyword and item.value.upper() == 'FROM':
            from_seen = True


def extract_table_identifiers(token_stream):
    for item in token_stream:
        if isinstance(item, IdentifierList):
            for identifier in item.get_identifiers():
                yield identifier.get_name()
        elif isinstance(item, Identifier):
            yield item.get_name()
        # It's a bug to check for Keyword here, but in the example
        # above some tables names are identified as keywords...
        elif item.ttype is Keyword:
            yield item.value


def extract_tables():
    stream = extract_from_part(sqlparse.parse(sql)[0])

    return list(extract_table_identifiers(stream))


if __name__ == '__main__':
    print 'Tables: %s' % ', '.join(extract_tables())
