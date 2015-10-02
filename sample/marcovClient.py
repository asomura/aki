# coding: utf-8
import sys
import os
import os.path
import socket
import time
sys.path.append(os.pardir)
from eguchi import marcov
from lib import textParser

dicFile = "dic.dump"
startsFile = "starts.dump"
m = marcov.MarcovModel()
if os.path.isfile(dicFile) and os.path.isfile(startsFile):
    m.load(dicFile, startsFile)
else:
    m.readTextFile("test.txt")
    m.save(dicFile, startsFile)
m.readTextFile("test.txt")

host = '127.0.0.1'
port = 5001
initFlag = True

clientsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientsock.connect((host,port))
c_msg = u"こんばんは。"
while True:
    print c_msg
    clientsock.sendall(c_msg.encode('utf-8'))
    rcvmsg = clientsock.recv(4096).decode('utf-8')
    #clientsock.sendall(c_msg)
    #rcvmsg = clientsock.recv(4096)
    print 'Received -> %s' % (rcvmsg)
    if rcvmsg == '':
      break
    p = textParser.TextParser(rcvmsg.encode('utf-8'))
    keywords = p.phraseList
    c_msg = m.generate(keywords)
    time.sleep(1)
clientsock.close()
