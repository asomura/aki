# coding: utf-8
import sys
import os
import os.path
import socket
import select
import threading
sys.path.append(os.pardir)
from eguchi import marcov
from lib import textParser

def sendMsg(msg):
    print"%s > %s" % (user, msg)
    try:
        server_sock.send(('%s| %s' % (user, msg)).encode('utf-8'))
    except:
        print('connection error')
        sys.exit()

if __name__ == "__main__":
    initFlag = True
    if len(sys.argv) < 4:
        print('Usage : python %s user host [master|slave]' % sys.argv[0])
        sys.exit()
    (user, host, role) = sys.argv[1:4]
    port = 5001
    print "user: %s, host: %s, role: %s, port: %s" % (user, host, role, port)
    #マルコフモデルセットアップ
    dicFile = "dic.dump"
    startsFile = "starts.dump"
    m = marcov.MarcovModel()
    if os.path.isfile(dicFile) and os.path.isfile(startsFile):
        m.load(dicFile, startsFile)
    else:
        m.readTextFile("test.txt")
        m.save(dicFile, startsFile)
    m.readTextFile("test.txt")
    #Socket接続
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try :
        server_sock.connect((host, port))
    except :
        print('Unable to connect')
        sys.exit()
    print('Start')
    def chat():
        while True:
            read_sockets, write_sockets, error_sockets = select.select([server_sock], [], [])
            try:
                data = server_sock.recv(4096).decode('utf-8')
            except:
                break
            sys.stdout.write('\r%s\n' % data)
            p = textParser.TextParser(data)
            keywords = p.phraseList
            msg = m.generate(keywords)
            sendMsg(msg)
        print('\rTerminated')
    t = threading.Thread(target=chat)
    t.start()
    if role == "master":
        sendMsg("こんにちは")
