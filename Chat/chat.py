from bottle import run, get, post, view, request, redirect
import requests
import bottle
import json
import threading
import time
import sys

messages 	= [(sys.argv[2], "Entrou no Chat!")]
messagesRepitidas =  [(sys.argv[2], "Entrou no Chat!")]
peers 		= sys.argv[3:]
nick 		= sys.argv[2]
myPort 		= sys.argv[1]
hostLocal 	= 'localhost'
urlLocal 	= 'http://'

@get('/')
@view('index')
def index():
    return {'messages': messages, 'nick': nick}

@get('/All')
def index():
    return json.dumps(messages)

@post('/send')
def sendMessage():
    global nick
    m = request.forms.get('message')
    n = request.forms.get('nick')
    messages.append([n, m])
    messagesRepitidas.append([n, m])
    nick = n
    redirect('/')


@bottle.route('/peers/<host>/<port>')
def index(host,port):
    try:
        teste = peers.index(urlLocal+host+':'+port)
        return json.dumps(peers)
    except Exception as e:
        peers.append(urlLocal+host+':'+port)
        return json.dumps(peers)

def client():
    time.sleep(5)
    while True:
        time.sleep(1)
        np = []
        for p in peers:
            r = requests.get(p + '/peers/'+hostLocal+'/'+myPort)
            np = np + json.loads(r.text)
            time.sleep(1)
        peers[:] = list(set(np + peers))


t = threading.Thread(target=client)
t.start()

def buscaMensagens():
    time.sleep(3)
    while True:
        #time.sleep(1)
        np = []
        mp = []
        count = 0
        for p in peers:
            r = requests.get(p + '/All')
            np = np + json.loads(r.text)
            
        try:
            for i in np:
                mp = i
                teste = messages.index(i)                  
        except Exception as e:  
            messagesRepitidas.extend(mp) 
            messages.append(i)   
            print(messages) 


thread = threading.Thread(target=buscaMensagens)
thread.start()

run(host=hostLocal, port=myPort)
