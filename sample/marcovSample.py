# coding: utf-8
import sys
import os
import os.path
sys.path.append(os.pardir)
from eguchi import marcov
from lib import textParser

dicFile = "dic.json"
startsFile = "starts.json"
m = marcov.MarcovModel()
'''
if os.path.isfile(dicFile) and os.path.isfile(startsFile):
    m.load(dicFile, startsFile)
else:
    m.readTextFile("test.txt")
    m.save(dicFile, startsFile)
'''
m.readTextFile("test.txt")
while True:
    inputText = raw_input(u"> ")
    #inputText = unicode(inputText, "utf-8")
    p = textParser.TextParser(inputText)
    keywords = p.phraseList
    print m.generate(keywords)
