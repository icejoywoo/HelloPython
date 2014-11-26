#!/bin/env python
# ^_^ encoding: utf-8 ^_^
# @date: 14-1-27

__author__ = 'wujiabin'

'''
维基百科: http://zh.wikipedia.org/wiki/%E4%B8%AD%E5%8D%8E%E4%BA%BA%E6%B0%91%E5%85%B1%E5%92%8C%E5%9B%BD%E5%85%AC%E6%B0%91%E8%BA%AB%E4%BB%BD%E5%8F%B7%E7%A0%81
公民身份号码是由17位数字码和1位校验码组成。排列顺序从左至右分别为：6位地址码，8位出生日期码，3位顺序码和1位校验码。
地址码（身份证地址码对照表见下面附录）和出生日期码很好理解，顺序码表示在同一地址码所标识的区域范围内，对同年同月同日出生的人编定的顺序号，顺序码的奇数分配给男性，偶数分配给女性。
身份证最后一位校验码算法如下：
1. 将身份证号码前17位数分别乘以不同的系数，从第1位到第17位的系数分别为：7 9 10 5 8 4 2 1 6 3 7 9 10 5 8 4 2
2. 将得到的17个乘积相加。
3. 将相加后的和除以11并得到余数。
4. 余数可能为0 1 2 3 4 5 6 7 8 9 10这些个数字，其对应的身份证最后一位校验码为1 0 X 9 8 7 6 5 4 3 2。
'''

import datetime
import random


area_code = dict([i.split() for i in file("id_area_code_china.txt")])
id_checksum = lambda s: str((1 - 2 * int(s, 13)) % 11).replace('10', 'X')


def location_from_id(_id):
    # 地址码   出生日期码   顺序码   校验码
    area_2 = area_code.get(_id[:2], None)
    area_4 = area_code.get(_id[:4], None)
    area_6 = area_code.get(_id[:6], None)
    # 顺序码 奇数分配给男性，偶数分配给女性
    gender = 'Female' if int(_id[14:17]) % 2 == 0 else 'Male'
    return {
        'location': (area_2, area_4, area_6),
        'gender': gender
    }


# only for 18位id
def validate_id(_id):
    if len(_id) != 18:
        raise TypeError("Only support 18-bit id code.")
    location = area_code.get(_id[:6], None)
    if not location:
        return False, "location does not exist! location code: %s" % _id[:6]

    if _id[-1] != id_checksum(_id[:17]):
        return False, "checksum wrong! checksum should be %s, actually be %s" % (id_checksum(_id[:17]), _id[-1])
    return True


def random_birthday(start=datetime.datetime(1900, 1, 1), end=datetime.datetime.now()):
    return (start + datetime.timedelta(
        seconds=random.randint(0, int((end - start).total_seconds())))).strftime("%Y%m%d")


def _random_id(area_code_6):
    location = random.choice(area_code_6.keys())
    birthday = random_birthday()
    sequence = "%03d" % random.randint(0, 999)
    checksum = id_checksum("%s%s%s" % (location, birthday, sequence))
    return "%s%s%s%s" % (location, birthday, sequence, checksum)


def random_id(area_code_6={}):
    try:
        return _random_id(area_code_6)
    except IndexError:
        print "loading area_code once ..."
        for k, v in area_code.items():
            if len(k) == 6:
                area_code_6[k] = v
        return _random_id(area_code_6)


def _random_chinese_name(d, f):
    name = random.choice(d)
    family_name = [i for i in f if name.startswith(i)]
    return family_name[0] if family_name else "Unknown", name


# chinese name
def random_chinese_name(d=[], f=[]):
    try:
        return _random_chinese_name(d, f)
    except IndexError:
        print "loading dict once ..."
        [d.append(i.strip()) for i in file("chinese_names.txt")]
        [f.append(i.strip()) for i in file("chinese_family_names.txt")]
        return _random_chinese_name(d, f)


if __name__ == "__main__":
    # 处理原始地区编码
    # f = open("id_area_code_format.txt", "w")
    # for line in file("id_area_code_china.txt"):
    #     words = line.strip().split()
    #     if len(words[0]) == 6:
    #         print >> f, "    '%s': '%s'," % (words[0], words[1])

    # int('63280119790817003', 13) -> 4156357119502734149L
    assert id_checksum('15212219890105556') == '5'
    assert id_checksum('44512220071021799') == 'X'

    print location_from_id('152122198901055565')['gender']
    print location_from_id('44512220071021799X')['location']

    print validate_id('152122198901055565')

    for _ in xrange(5):
        print random_id()

    for _ in xrange(5):
        family_name, name = random_chinese_name()
        print family_name, name
