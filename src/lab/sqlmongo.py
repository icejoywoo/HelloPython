#!/bin/env python
# ^_^ encoding: utf-8 ^_^
# @date: 14/11/28

__author__ = 'icejoywoo'

import sqlparse
import sqlparse.sql
from sqlparse import tokens


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


def is_comparison(parsed):
    return isinstance(parsed, sqlparse.sql.Comparison)


def transfer_in_operation(parsed, idx):
    """ 存在多个关键字, in 和 not in两种, 需要回溯
    @param tokens:
    @param idx:
    @return:
    """
    in_operators = {
        'in': '$in',
        'not in': '$nin',
    }

    in_idx = idx
    operator = parsed.tokens[idx].value

    def get_token(parsed, index, direction):
        def update_index(i):
            if direction == 'forward':
                return i + 1
            elif direction == 'backward':
                return i - 1
            else:
                raise Exception("Unsupported direction.")
        token_idx = update_index(index)
        token = parsed.tokens[token_idx]
        # ignore the Whitespace
        while token.ttype in (tokens.Whitespace, tokens.Punctuation):
            token_idx = update_index(token_idx)
            token = parsed.tokens[token_idx]
        return token, token_idx

    # 前面是否有not
    prev_token, idx = get_token(parsed, idx, direction='backward')
    if prev_token.ttype is tokens.Keyword and prev_token.value.upper() == 'NOT':
        operator = 'not ' + operator
        field_token = get_token(parsed, idx, direction='backward')[0].value
    else:
        field_token = prev_token.value

    right_token = get_token(parsed, in_idx, direction='forward')[0]
    right_value = None
    # in操作存在子查询的情况
    if isinstance(right_token, sqlparse.sql.Parenthesis):
        first_token = get_token(right_token, 0, direction='forward')[0]
        if first_token.ttype is tokens.DML and first_token.value.upper() == 'SELECT':
            # 去除两边的括号
            right_value = transfer_sql(right_token.value[1:-1])
    else:
        right_value = eval(right_token)

    return {field_token: {in_operators[operator]: right_value}}


def transfer_comparison(parsed):
    """ 是一个token表示的
    @param parsed:
    @return:
    """
    # 比较操作
    # {a: {'$gt': 15}}
    comparison_operators = {
        '=': '$eq',
        '!=': '$ne',
        '>': '$gt',
        '<': '$lt',
        '>=': '$gte',
        '<=': '$lte',
    }
    left_field = None
    right_value = None
    print parsed.tokens
    for t in parsed.tokens:
        if isinstance(t, sqlparse.sql.Identifier) or (isinstance(t, sqlparse.sql.Token)
                                                      and t.ttype in (tokens.Literal.Number.Integer, )):
            if t.is_whitespace():
                continue
            if left_field is None:
                left_field = t.value
            elif right_value is None:
                # 右值可以是python表达式
                right_value = eval(t.value)
            else:
                raise Exception("Error")
        elif t.ttype is tokens.Operator.Comparison:
            operator = comparison_operators[t.value]

    return {left_field: {operator: right_value}}


def transfer_sql(sql):
    sql = sql.strip()
    dbs = []
    query = {}
    fields = {}
    fields_wildcard = False

    for item in sqlparse.parse(sql):
        from_seen = False
        select_seen = False

        for t in item.tokens:
            if t.ttype is tokens.Whitespace:
                continue
            # update flags
            elif t.ttype is tokens.Keyword and t.value.upper() == 'FROM':
                from_seen = True
                select_seen = False
            elif t.ttype is tokens.DML and t.value.upper() == 'SELECT':
                select_seen = True
            else:
                if is_subselect(t):
                    print t.tokens

                # 处理where语句
                if is_where(t):
                    # 一般第一个表达式之后才是and或or等操作符
                    last_comparison = None
                    operator = None
                    logical_operators = {
                        'AND': '$and',
                        'OR': '$or',
                    }
                    # 跳过第一个where关键字
                    for i in t.tokens[1:]:
                        if i.is_whitespace():
                            continue
                        # and, or
                        if i.ttype is tokens.Keyword and i.value.upper() in logical_operators:
                            if not operator:
                                # 初始化
                                operator = logical_operators.get(i.value.upper(), None)
                                query[operator] = [last_comparison]
                            else:
                                new_operator = logical_operators.get(i.value.upper(), None)
                                last_comparison = {operator: query.pop(operator)}
                                operator = new_operator
                                query[operator] = [last_comparison]

                        elif is_comparison(i):
                            last_comparison = transfer_comparison(i)
                            if operator:
                                query[operator].append(transfer_comparison(i))
                        elif i.ttype is tokens.Keyword and i.value.upper() == 'IN':
                            if operator:
                                query[operator].append(transfer_in_operation(t, t.token_index(i)))

                if from_seen:
                    if isinstance(t, sqlparse.sql.Identifier):
                        db = t.get_name()
                        dbs.append(db)
                        from_seen = False
                    if isinstance(t, sqlparse.sql.IdentifierList):
                        for identifier in t.get_identifiers():
                            dbs.append(identifier.get_name())
                        from_seen = False

                if select_seen:
                    if fields_wildcard:
                        raise Exception('Wildcard(*) cannot be selected with other fields.')
                    elif t.ttype is tokens.Wildcard:
                        fields_wildcard = True
                    else:
                        fields[t.value] = 1
    if len(dbs) != 1:
        raise Exception('Only support from one db.')
    return dbs[0], query, fields


if __name__ == '__main__':

    sql = """
    select * from foo where a = 1 and b != 'xxx' or
        uid in (select uid from bar where _ = ISODate("2014-11-19"))
    """

    # sql = """select * from foo where a = 1 and b != "xxx" or uid not in ("1", "2") and c in (3, 4)"""
    print transfer_sql(sql)

    sql = """ select uid from bar where a = 1 and $log_date = Date("2014-11-19") """
    print sqlparse.parse(sql)[0].tokens[-2].tokens
    t = sqlparse.parse(sql)[0].tokens[-2].tokens[6]
    print t, type(t), t.ttype

