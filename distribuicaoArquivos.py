from bottle import run, get, Bottle, post, view, request, redirect
import requests
import bottle
import json
import threading
import time
import sys
import hashlib

'''---------------------------------------------------------------------------------'''

class DHT:
    def subkeys(self, k):
        for i in range(len(k), 0, -1):
            yield k[:i]
        yield ""

    def gerar_hash(self, my_port):
        h = hashlib.sha256(my_port.encode())
        h.hexdigest()
        n = int(h.hexdigest(), base=16) % 15
        n = "{0:b}".format(n)
        m = str(n)
        self.p = m.zfill(4)

    def __init__(self, k):
        self.gerar_hash(k)
        self.k = k
        self.h = {}
        print("CHAVE " + self.p)
        print(type(self.h))
        print("\n")

        for sk in self.subkeys(self.k):
            self.h[sk + '0'] = None

        for sk in self.subkeys(self.k):
            self.h[sk + '1'] = None

        sorted(self.h.keys())

    def insert(self, k, v):

        for sk in self.subkeys(k):
            print(sk)
            print("\n")
            if sk in self.h:
                if not self.h[sk]:
                    self.h[sk] = (k, v)
                    return sk + self.p
        return None

    def lookup(self, k):
        print(list(self.subkeys(k)))
        for sk in self.subkeys(k):
            print(sk)
            print("\n")
            print(self.h)
            if sk in self.h:
                if self.h[sk]:
                    (ki, vi) = self.h[sk]
                    if ki == k:
                        return vi
        return None

    def __repr__(self):
        return "<<DHT:" + repr(self.h) + ">>"


class DhtServer:
    def __init__(self, port):
        self.dht = DHT(port)

    def insert_dht(self, key, value):
        #usar este método para fazer as validações necessárias referente a inserção na dht.
        self.dht.insert(key, value)

    def lookup_dht(self,key):
        return self.dht.lookup(key)

    def dht_lookup(self,key):
        return self.dht.lookup(key)

    def dht_lookup_dump(self, key):
        return json.dumps(self.dht_lookup(key))


    #@bottle.route('/dht/<key>/<value>')
    def dht_insert(self, key, value):
        self.dht.insert(key, value)
        #global dht
        #return json.dumps(dht.insert(key, value))
        #return json.dumps(insert_dht(key, value))
        return json.dumps(key, value)


'''---------------------------------------------------------------------------------'''

class PeerToPeerServer:
    def __init__(self, port, peers):
        self.myPort = port
        self.peers = peers
        self.hostLocal = 'localhost'
        self.urlLocal = 'http://'

    #Nos métodos abaixo ver como fazer pra usar as informações da classe.
    #@bottle.route('/peers/<hostLocal>/<myPort>')
    def index(self, host, port):
        try:
            self.peers.index(self.urlLocal + host + ':' + port)
            return json.dumps(self.peers)
        except Exception as e:
            self.peers.append(self.urlLocal + host + ':' + port)
            return json.dumps(self.peers)

    def client(self):
        time.sleep(5)
        while True:
            time.sleep(1)
            np = []
            for p in self.peers:
                r = requests.get(p + '/peers/'+self.hostLocal+'/'+self.myPort)
                np = np + json.loads(r.text)
                print(r.text)
                time.sleep(1)
                self.peers[:] = list(set(np + self.peers))

    def start_PeerToPeer_Server(self):
        t = threading.Thread(target=self.client)
        t.start()




'''---------------------------------------------------------------------------------'''

class DistribuicaoArquivos:
    def __init__(self, port, peers):
        self.myPort = port
        self.peers = peers
        self.servidorDht = DhtServer(self.myPort)
        self.servidorPeerToPeer = PeerToPeerServer(self.myPort, self.peers)
        self.b = bottle.Bottle()
        self.b.get('/dht/<key>')(self.servidorDht.dht_lookup)
        self.b.route('/dht/<key>/<value>')(self.servidorDht.dht_insert)
        self.b.route('/peers/<host>/<port>')(self.servidorPeerToPeer.index)
        self.initPeerToPeer()


    def initDht(self):
        #self.servidorDht = DhtServer(self.myPort)
        #self.servidorDht.start_dht_Server()
        pass

    def initPeerToPeer(self):
        #self.servidorPeerToPeer = PeerToPeerServer(self.myPort, self.peers)
        self.servidorPeerToPeer.start_PeerToPeer_Server()

    def run(self):
        self.b.run(host='localhost', port=self.myPort)


#instância.

servidor = DistribuicaoArquivos(sys.argv[1], sys.argv[2:])
servidor.run()

