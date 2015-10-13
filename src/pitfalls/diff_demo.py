#!/bin/env python
# ^_^ encoding: utf-8 ^_^
# @author: icejoywoo
# @date: 14-3-24

text1 = '''  1. Beautiful is better than ugly.
  2. Explicit is better than implicit.
  3. Simple is better than complex.
  4. Complex is better than complicated.
'''.splitlines(True)

text2 = '''  1. Beautiful is better than ugly.
  3.   Simple is better than complex.
  4. Complicated is better than complex.
  5. Flat is better than nested.
'''.splitlines(True)

from difflib import Differ, SequenceMatcher
from pprint import pprint

d = Differ()
result = d.compare(text1, text2)
pprint(list(d.compare(text1, text2)))
pprint(list(d.compare(text1, text1)))

s = SequenceMatcher(a=text1, b=text2)
print s.ratio()
print s.get_opcodes()
for tag, alo, ahi, blo, bhi in s.get_opcodes():
    print tag
