# -*- coding: utf-8 -*-
import random


def reply():
    answers = [
        u'ふむふむ',
        u'それで？',
        u'もっと具体的には？',
        u'ちょっと違うと思うな',
        u'別の観点から考えよう',
        u'とてもいい視点だね',
        u'あとは何が足りないかな']
    print answers[random.randint(0, len(answers) - 1)]


def start():
    while 1:
        command = raw_input('>>>')
        reply()
        if command == 'exit':
            break


if __name__ == '__main__':
    start()
    print 'Bye :) .'
