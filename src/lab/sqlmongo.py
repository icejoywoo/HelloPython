#!/bin/env python
# ^_^ encoding: utf-8 ^_^
# @date: 14/11/28

__author__ = 'icejoywoo'

import sqlparse
import sqlparse.sql
from sqlparse import tokens

import itertools
import datetime


def sql_date(date_str):
    return datetime.datetime.strptime(date_str, "%Y-%m-%d")

yesterday = datetime.datetime.combine(datetime.datetime.now(), datetime.time()) - datetime.timedelta(days=1)

built_in_var_and_funcs = {
    'Date': sql_date,
    'ISODate': sql_date,
    '$yesterday': yesterday,
}


def sql_eval(str_to_be_evaled):
    str_to_be_evaled = str_to_be_evaled.strip()
    if str_to_be_evaled.startswith('$'):
        return built_in_var_and_funcs[str_to_be_evaled]
    return eval(str_to_be_evaled, built_in_var_and_funcs)


def get_token(parsed, index, direction):
    """
    @param parsed:
    @param index:
    @param direction:
    @return:
    """
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
    if isinstance(parsed, sqlparse.sql.Comparison):
        return True
    elif isinstance(parsed, sqlparse.sql.Token) and parsed.ttype is tokens.Comparison:
        return True
    elif isinstance(parsed, sqlparse.sql.Parenthesis):
        first_token = parsed.token_next_by_instance(0, sqlparse.sql.Comparison)
        if first_token:
            return True

        first_token = parsed.token_next_by_type(0, tokens.Comparison)
        if first_token:
            return True

    return False


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

    # 前面是否有not
    left_token, idx = get_token(parsed, idx, direction='backward')
    if left_token.ttype is tokens.Keyword and left_token.value.upper() == 'NOT':
        operator = 'not ' + operator
        field_token = get_token(parsed, idx, direction='backward')[0].value
    else:
        field_token = left_token.value

    right_token = get_token(parsed, in_idx, direction='forward')[0]
    right_value = None
    # in操作存在子查询的情况
    if isinstance(right_token, sqlparse.sql.Parenthesis):
        first_token = get_token(right_token, 0, direction='forward')[0]
        if first_token.ttype is tokens.DML and first_token.value.upper() == 'SELECT':
            # 去除两边的括号
            right_value = transfer_sql(right_token.value[1:-1])
    else:
        right_value = sql_eval(right_token)

    return {field_token: {in_operators[operator]: right_value}}


def transfer_between_operation(parsed, idx):
    """
    @param parsed:
    @param idx:
    @return:
    """
    between_token = parsed.tokens[idx]
    field_token = parsed.token_prev(idx)

    lower_token = parsed.token_next(idx)
    lower_token_idx = parsed.token_index(lower_token)

    in_token = parsed.token_next(lower_token_idx)
    in_token_idx = parsed.token_index(in_token)

    upper_token = parsed.token_next(in_token_idx)

    lower_value = sql_eval(lower_token.value)
    upper_value = sql_eval(upper_token.value)
    field_name = field_token.value

    return {field_name: {'$gte': lower_value, '$lte': upper_value}}


def transfer_comparison(parent, parsed):
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
    if isinstance(parsed, sqlparse.sql.Comparison):
        for t in parsed.tokens:
            if isinstance(t, sqlparse.sql.Identifier) or (isinstance(t, sqlparse.sql.Token)
                                                          and t.ttype in (tokens.Literal.Number.Integer, )):
                if t.is_whitespace():
                    continue
                if left_field is None:
                    left_field = t.value
                elif right_value is None:
                    # 右值可以是python表达式
                    right_value = sql_eval(t.value)
                else:
                    raise Exception("Error")
            elif t.ttype is tokens.Operator.Comparison:
                operator = comparison_operators[t.value]

        return {left_field: {operator: right_value}}
    elif isinstance(parsed, sqlparse.sql.Token) and parsed.ttype is tokens.Comparison:
        operator = comparison_operators[parsed.value]
        idx = parent.token_index(parsed)

        prev_token = get_token(parent, idx, direction='backward')[0]
        next_token = get_token(parent, idx, direction='forward')[0]

        field = prev_token.value
        value = sql_eval(next_token.value)

        return {field: {operator: value}}
    elif isinstance(parsed, sqlparse.sql.Parenthesis):
        return transfer_where(parsed)


def merge_query(query):
    # [{'a': {'$gt': 10}}, {'a': {'$lt': 5}} ...] 合并为[{'a': {'$gt': 10, '$lt': 5}} ...]
    print "a", query
    merged_query = []
    for k, v in itertools.groupby(query, key=lambda i: i.keys()[0]):
        v = list(v)
        if k in ('$and', '$or'):
            assert len(v) == 1
            print "b", v[0]
            merged_query.append(v[0])
            continue
        for sk, sv in itertools.groupby(v, key=lambda i: i.keys()[0]):
            sv = list(sv)
            merged_subquery = {}
            for i in sv:
                merged_subquery.update(i.values()[0])
            print "x", sk, merged_subquery
            merged_query.append({sk: merged_subquery})
            print "y", merged_query
    return merged_query


def transfer_where(parsed):
    query = {}
    # 一般第一个表达式之后才是and或or等操作符
    last_comparison = None
    operator = None
    logical_operators = {
        'AND': '$and',
        'OR': '$or',
    }
    # 跳过第一个where关键字
    for index, i in enumerate(parsed.tokens[1:]):
        if i.is_whitespace():
            continue
        # and, or
        if i.ttype is tokens.Keyword and i.value.upper() in logical_operators:
            # 区分between and还是只有and
            prev_token = parsed.token_prev(index)
            prev_token = parsed.token_prev(parsed.token_index(prev_token))

            if prev_token.ttype is tokens.Keyword and prev_token.value.upper() == 'BETWEEN':
                continue

            if not operator:
                # 初始化
                operator = logical_operators.get(i.value.upper(), None)
                query[operator] = [last_comparison]
            else:
                new_operator = logical_operators.get(i.value.upper(), None)
                last_query = query.pop(operator)
                last_comparison = {operator: last_query}
                operator = new_operator
                query[operator] = [last_comparison]

        elif is_comparison(i):
            comparison = transfer_comparison(parsed, i)
            if operator:
                query[operator].append(comparison)
            last_comparison = comparison
        elif i.ttype is tokens.Keyword and i.value.upper() == 'IN':
            if operator:
                query[operator].append(transfer_in_operation(parsed, parsed.token_index(i)))
        elif i.ttype is tokens.Keyword and i.value.upper() == 'BETWEEN':
            if operator:
                query[operator].append(transfer_between_operation(parsed, parsed.token_index(i)))
    return query


def transfer_sql(sql):
    # 去除sql两边的空白字符
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
                    #print t.tokens
                    pass

                # 处理where语句
                if is_where(t):
                    query = transfer_where(t)

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
                    elif isinstance(t, sqlparse.sql.IdentifierList):
                        for identifier in t.get_identifiers():
                            if identifier.ttype is tokens.Wildcard:
                                raise Exception('Wildcard(*) cannot be selected with other fields.')
                            fields[identifier.get_name()] = 1
                    else:
                        fields[t.value] = 1
    if len(dbs) != 1:
        raise Exception('Only support from one db.')
    return dbs[0], query, fields


if __name__ == '__main__':

    sql = """
    select * from foo where a = 1 and (b != 'xxx' or
        uid in (select uid from bar where _ = ISODate("2014-11-19")))
    """

    # sql = """select * from foo where a = 1 and b != "xxx" or uid not in ("1", "2") and c in (3, 4)"""
    print transfer_sql(sql)

    sql = """ select uid, c, d from bar where (a < 1 and a > 1 or b < 1) and log_date between Date("2014-11-19") and $yesterday """
    print sqlparse.parse(sql)[0].tokens
    print transfer_sql(sql)

