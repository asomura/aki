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
serversock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serversock.bind((host,port))
serversock.listen(1)
print 'Waiting for connections...'
clientsock, client_address = serversock.accept()
while True:
    rcvmsg = clientsock.recv(4096).decode('utf-8')
    #rcvmsg = clientsock.recv(4096)
    print 'Received -> %s' % (rcvmsg)
    if rcvmsg == '':
      break
    p = textParser.TextParser(rcvmsg.encode('utf-8'))
    keywords = p.phraseList
    s_msg = m.generate(keywords)
    print s_msg
    clientsock.sendall(s_msg.encode('utf-8'))
    #clientsock.sendall(s_msg)
    time.sleep(1)
clientsock.close()
