# coding: utf-8
import Cabocha
import re
from xml.etree.ElementTree import *

'''
TextParser
==================
与えられたテキストをCabochaで解析した情報を提供します。

パラメータ
----------
+ `text` : [文字列]解析を行うテキスト

インスタンス変数
---------------
+ `text` : [文字列] 与えられたテキスト（パラメータとして与えたtextと同一）
+ `phraseList` : [配列] 分かち書きした文節のリスト
+ `chunks`: [ディクショナリ] 各文節の詳細情報
  + `id` : [数値]文節のid
  + `link_id` : [数値]修飾している文節のid(修飾先がない場合は-1)
  + `tok` : [ディクショナリ]: 文節を構成する単語とその情報
    + `word` : [文字列]単語
    + `feature` : [文字列]単語の情報（品詞、読みなど）
+ `xmlString` : [文字列]Cabocha解析結果のXMLデータ
'''
class TextParser:

    #コンストラクタ
    def __init__(self, text=""):
        self.parse(text)

    #メソッド
    #テキストを読み込み、解析
    def parse(self, text):
        self.text = text
        self.xmlString = ""
        self.phraseList = []
        self.chunks = []
        self.linkCount = {}
        if not text == "":
            self.xmlString = self.__cabochaParse()
            self.__getPhraseList()

    #プライベートメソッド
    #Cabochaによる解析
    def __cabochaParse(self):
        c = Cabocha.Parser()
        tree =  c.parse(self.text)
        return tree.toString(Cabocha.FORMAT_XML)

    def __getPhraseList(self):
        elem = fromstring(self.xmlString)
        for e in elem.getiterator("chunk"):
            s = ""
            chunk = {
                'id': e.get('id'),
                'link_id': e.get('link'),
                'phrase':'',
                'tok':[]}
            for c in e.getiterator("tok"):
                s += c.text
                chunk['tok'].append({
                    'word': c.text,
                    'feature': c.get('feature'),
                    })
            self.phraseList.append(s)
            chunk['phrase'] = s
            self.chunks.append(chunk)
