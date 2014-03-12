# by lauchingjun@baidu
import re
from collections import OrderedDict


def _parse_from_generator(gen):
    g = OrderedDict()
    groupstack = [('', g)]
    cur = g

    re_groups = re.compile('^\[[ \\t]*(\.*)((?:[a-zA-Z0-9_]+\.)*)(@?)([a-zA-Z0-9_]+)[ \\t]*\][ \\t]*(?:#.*)?$')
    re_items = re.compile('^[ \r\t]*(@?)([a-zA-Z0-9_]+)[ \t]*:[ \t]*(.*)$')
    for line in gen:
        line = line.strip()
        if len(line) == 0 or line[0] == '#':
            continue
        if re_groups.match(line) is not None:
            #remove comments
            line = line.split('#', 1)[0].strip()
            line = line.strip('[]')
            groups = line.split('.')
            level = 0
            cur = g
            for i in groups:
                if i == '':
                    cur = groupstack[level + 1][1]
                else:
                    if i[0] == '@':  # list
                        i = i[1:]
                        if i not in cur:
                            cur[i] = []
                        if not isinstance(cur[i], list):
                            return None
                        tmp = OrderedDict()
                        cur[i].append(tmp)
                        cur = tmp
                        del groupstack[level + 1:]
                        groupstack.append((i, cur))
                    else:  # normal group
                        if i not in cur:
                            cur[i] = OrderedDict()
                        if not isinstance(cur[i], dict):
                            return None
                        cur = cur[i]
                        if groupstack[level][0] != i:
                            del groupstack[level + 1:]
                            groupstack.append((i, cur))
                level += 1
            del groupstack[level + 1:]
        elif re_items.match(line) is not None:
            part = line.split(':', 1)
            key = part[0].strip()
            value = part[1].strip()
            if len(value) == 0:
                value = ''
            elif value[0] == '"':  # quoted mode
                value = value[1:].rsplit('"', 1)[0]
            else:
                value = value.split('#', 1)[0].strip()

            if key[0] == '@':  # list type
                key = key[1:]
                if key not in cur:
                    cur[key] = []
                if type(cur[key]) is not list:
                    return None
                cur[key].append(value)
            else:
                cur[key] = value
        else:
            return None
    return g


def parse_file(f):
    return _parse_from_generator(open(f))


def parse(s):
    return _parse_from_generator(s.split('\n'))


def isprimitive(value):
    return (not isinstance(value, dict)) and (not isinstance(value, list))


def dictkeyfunc(v):
    if isinstance(v[1], dict) or isinstance(v[1], list):
        prefix = 'b'
    else:
        prefix = 'a'
    return prefix


def _dump(key, value, level):
    out = ''
    indention = '    ' * level
    if isinstance(value, dict):
        if key:
            out += indention
            out += '[%s%s]\n' % ('.' * level, key)
        for k, v in sorted(value.items(), key=dictkeyfunc):
            out += _dump(k, v, level + 1)
        out += '\n'
    elif isinstance(value, list):
        for i in value:
            if key:
                out += indention
                if isprimitive(value[0]):
                    out += '@%s: ' % key
                else:
                    out += '[%s@%s]\n' % ('.' * level, key)
            out += _dump(None, i, level)
        out += '\n'
    elif value:
        if key:
            out += indention
            out += "%s: " % key
        out += "%s\n" % value
    return out


def dump_file(conf, filename):
    with open(filename, 'w') as f:
        f.write(dump(conf))


def dump(conf):
    return _dump(None, conf, -1)

if __name__ == '__main__':
    from pprint import pprint
    import sys
    pprint(parse_file(sys.argv[1]))
