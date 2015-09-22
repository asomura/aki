# -*- coding: utf-8 -*-
from ctypes import *

def sparse(s):
    # ライブラリの場所を指定
    #libpath = 'c:/mecab/bin/libmecab.dll'
    libpath = '/usr/lib/libmecab.so.2'
    # ライブラリを ctypes を使って読み込み
    lib = cdll.LoadLibrary(libpath)

    # 解析器初期化用の引数を指定（-Owakati で分かち書き)
    argc = c_int(2)
    argv = (c_char_p * 2)("mecab", "-Owakati")

    # 解析器のオブジェクトを作る
    tagger = lib.mecab_new(argc, argv)

    """ 指定された文字列を分かち書きして返す。 """
    s = lib.mecab_sparse_tostr(tagger, s)
    ret = c_char_p(s).value

    # 終わったら、一応、殺しておく 
    lib.mecab_destroy(tagger)

    return ret

if __name__ == "__main__":
    import random, sys, os

    filename = raw_input("file:")
    # 元にする文章の読み込み
    #filename = "test.txt"
    s = open(filename, "r").read()
    #s = raw_input("What your name? >")

    # わかち書きした単語をリストに格納する
    wordlist = sparse(s).rstrip(" \n").split(" ")
    while wordlist.count("") > 0:
	wordlist.remove("")
    #print wordlist

    # マルコフ連鎖テーブルの作成
    markov = {}
    pw = "" # pw - previous word, cw - current word
    for cw in wordlist:
        if pw:
            if markov.has_key(pw):
                lst = markov[pw]
            else:
                lst = []

            lst.append(cw)
            markov[pw] = lst
        pw = cw

    # マルコフ連鎖で文章作成
    selectword = wordlist[0]
    sentence = ""
    count = 0
    while len(wordlist) > count:
        sentence += selectword
        #selectword = random.choice(markov[selectword])
        #print random.choice(markov[selectword])
	#print len(markov[selectword])
	#print count
       	#print markov[selectword]
       	selectword = random.choice(markov[selectword])
        count += 1
    print sentence  
