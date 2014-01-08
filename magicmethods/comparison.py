#!/bin/env python
# ^_^ encoding: utf-8 ^_^
# @date: 14-1-7

__author__ = 'icejoywoo'


class Word(str):
    '''Class for words, defining comparison based on word length.'''

    def __new__(cls, word):
        # Note that we have to use __new__. This is because str is an immutable
        # type, so we have to initialize it early (at creation)
        if ' ' in word:
            print "Value contains spaces. Truncating to first space."
            word = word[:word.index(' ')] # Word is now all chars before first space
        return str.__new__(cls, word)

    #    def __eq__(self, other):
    #        return len(self) == len(other)
    #    def __ne__(self, other):
    #        return len(self) != len(other)
    def __gt__(self, other):
        return len(self) > len(other)

    def __lt__(self, other):
        return len(self) < len(other)

    def __ge__(self, other):
        return len(self) >= len(other)

    def __le__(self, other):
        return len(self) <= len(other)


if __name__ == "__main__":
    x = Word("test")
    y = Word("test test")
    assert x == y
    z = Word("abcdef")
    assert x < z
