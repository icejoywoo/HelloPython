#!/bin/env python
#^_^ encoding: utf-8 ^_^
# @date: 14-7-18

__author__ = 'wujiabin'

import gettext
import os

locale_path = os.path.join(os.path.dirname(__file__), 'locale')

gettext.install('lang', locale_path, unicode=True)
gettext.translation('lang', locale_path, languages=['cn'], fallback=True).install(True)

#_ = t.gettext

print _("Open")

cat = gettext.GNUTranslations(open(os.path.join(os.path.dirname(__file__), "locale/cn/LC_MESSAGES/lang.mo")))
_ = cat.gettext
print _("Open")
print _("Hello")
