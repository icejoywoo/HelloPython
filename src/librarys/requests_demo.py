#!/bin/env python
# ^_^ encoding: utf-8 ^_^
# @author: icejoywoo
# @date: 14-3-10

import requests

r = requests.get("http://www.baidu.com/")
# r = requests.get('https://api.github.com/user', auth=('user', 'pass'))

print r.status_code
print r.headers["content-type"]
print r.encoding
print r.text
print r.json
