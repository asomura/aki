# coding: utf-8
import sys,os
sys.path.append(os.pardir)
from lib import textParser
p = textParser.TextParser("太郎はこの本を二郎を見た女性に渡した")
print "* 文節リストの表示："
for s in  p.phraseList:
    print s
print "* 文節の詳細情報の表示："
for c in  p.chunks:
    print '['+c['phrase']+']'
    print 'id:' + c['id']
    print 'link to:' + c['link_id']
    for t in c['tok']:
        print t['word']
        print t['feature']
