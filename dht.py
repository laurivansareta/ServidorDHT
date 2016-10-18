from bottle import run, get, post, view, request, redirect
import requests
import bottle
import json
import threading
import time
import sys
import hashlib

# BUGLIST
# - insercao da mesma chave 2 vezes, possibilita inserir o mesmo par de chave/valer em posicoes diferentes da DHT
# - necessario cria uma maneira para inicializar a DHT, a partir de uma chave inicial
# - necessario implementar comunicacao em grupo, e propagar os inserts e lookups

myPort 		= sys.argv[1]

h = hashlib.sha256(myPort.encode())
h.hexdigest()
n = int(h.hexdigest(), base = 16) % 15
n = "{0:b}".format(n)
p = str(n)
p = p.zfill(4)

def subkeys(k):
    for i in range(len(k), 0, -1):
        yield k[:i]
    yield ""


class DHT:
    def __init__(self, k):
        self.k = k
        self.h = {}
        print("CHAVE "+p)
        print (type(self.h))

        for sk in subkeys(self.k):
            self.h[sk+'0'] = None

        for sk in subkeys(self.k):
            self.h[sk+'1'] = None
        
        sorted(self.h.keys())

    def insert(self, k, v):
        
        for sk in subkeys(k):
            print(sk)
            if sk in self.h:
                if not self.h[sk]:
                    self.h[sk] = (k, v)
                    return sk + p
        return None

    def lookup(self, k):
        print(list(subkeys(k)))
        for sk in subkeys(k):
            print(sk)
            print(self.h)
            if sk in self.h:
                if self.h[sk]:
                    (ki, vi) = self.h[sk]
                    if ki == k:
                        return vi
        return None

    def __repr__(self):
        return "<<DHT:"+ repr(self.h) +">>"

dht = DHT(p)




@get('/dht/<key>')
def dht_lookup(key):
    global dht
    print(p)
    return json.dumps(dht.lookup(key))

@bottle.route('/dht/<key>/<value>')
def dht_insert(key, value):
    global dht
    return json.dumps(dht.insert(key, value))


run(host='localhost', port=myPort)
