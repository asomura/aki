# coding: utf-8
import io
import pickle
import sys
import os
import random
sys.path.append(os.pardir)
from lib import textParser

class MarcovModel:
    #クラス変数
    ENDMARK = '__END__'
    MAXNUM  = 10

    #コンストラクタ
    def __init__(self):
        self.dic = {}
        self.starts = {}
        self.parser = textParser.TextParser()

    #メソッド
    #テキストファイルを読み込んで学習
    def readTextFile(self, txtFile):
        lines = open(txtFile, 'r').readlines()
        for line in lines:
            self.read(line)

    #与えられた行を読み込んで学習
    def read(self, line):
        self.parser.parse(line)
        self.__addSentence()

    #コメント生成
    def generate(self, keywords):
        count = 0
        maxNum = MarcovModel.MAXNUM
        dicLen = len(self.dic)
        if maxNum > dicLen:
            maxNum = dicLen
        w1 = ""
        w2 = ""
        (w1, w2) = self.__getStartPhrase(keywords)
        sentence = w1 + w2
        while count < maxNum:
            tmp = random.choice(self.dic[(w1, w2)])
            if tmp == MarcovModel.ENDMARK:
                break
            sentence += tmp
            w1, w2 = w2, tmp
            count += 1
        return sentence

    #辞書ファイル(json)のセーブ
    def save(self, dicFile="dic.dump", startsFile="starts.dump"):
        filePairs = [
            [dicFile, self.dic],
            [startsFile, self.starts]
        ]
        for (saveFile, data) in filePairs:
            f = open(saveFile, "w")
            pickle.dump(data, f)
            f.close()

    #辞書ファイル(json)のロード
    def load(self, dicFile="dic.dump", startsFile="starts.dump"):
        f = open(dicFile, "r")
        self.dic = pickle.load(f)
        f.close()
        f = open(startsFile, "r")
        self.starts = pickle.load(f)
        f.close()

    #プライベートメソッド
    #辞書ファイルへのデータ追加
    def __addSentence(self):
        p1 = ""
        p2 = ""
        startFlag = True
        phraseList = list(self.parser.phraseList)
        phraseList.append(MarcovModel.ENDMARK)
        for phrase in phraseList:
            if p1 and p2:
                if startFlag:
                    self.__addStart(p1, p2)
                    startFlag = False
                if (p1, p2) not in self.dic:
                    self.dic[(p1, p2)] = []
                self.dic[(p1, p2)].append(phrase)
            p1, p2 = p2, phrase

    #文の最初に来るフレーズ（文頭フレーズ）辞書startsへのデータ追加
    def __addStart(self, p1, p2):
        if (p1, p2) not in self.starts:
            self.starts[(p1, p2)] = 0
        self.starts[(p1, p2)] += 1

    #文頭フレーズの選択・取得
    def __getStartPhrase(self, keywords):
        selectedTuple = ("", "")
        for tpl in self.starts.keys():
            for keyword in keywords:
                if tpl[0] == keyword:
                    if selectedTuple == ("", ""):
                        selectedTuple = tpl
                    else:
                        selectedTuple = self.__selectPhrase(tpl, selectedTuple)
        if selectedTuple == ("", ""):
            selectedTuple = random.choice(self.starts.keys())
        return selectedTuple

    #文頭フレーズ候補が複数ある場合の選択ロジック（学習時の登場回数が多いほうが選ばれ易くなる）
    def __selectPhrase(self, tpl1, tpl2):
        cnt1 = self.starts[tpl1]
        cnt2 = self.starts[tpl2]
        selectedTuple = tpl1
        totalCnt = cnt1 + cnt2
        r = random.randint(1, totalCnt)
        if r > cnt1:
            selectedTuple = tpl2
        return selectedTuple
