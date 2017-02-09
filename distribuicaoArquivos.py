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
        p = str(n)
        self.p = p.zfill(4)

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

        for sk in self.subkeys(self, k):
            print(sk)
            print("\n")
            if sk in self.h:
                if not self.h[sk]:
                    self.h[sk] = (k, v)
                    return sk + p
        return None

    def lookup(self, k):
        print(list(self.subkeys(self, k)))
        for sk in self.subkeys(self, k):
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
    app = Bottle()

    def __init__(self, port):
        self.myPort = port
        self.dht = DHT(port)

    def start_dht_Server(self):
        run(self.app, host='localhost', port=self.myPort)

    def insert_dht(self, key, value):
        #usar este método para fazer as validações necessárias referente a inserção na dht.
        self.dht.insert(key, value)

    def lookup_dht(self,key):
        return self.dht.lookup(key)

    @get('/dht/<key>')
    def dht_lookup(key):
        #return json.dumps(dht.lookup(key))
        #return json.dumps(lookup_dht(key))
        print(key,'teste lookup')
        return json.dumps(key)

    # @post('/dht/<key>/<value>')
    # def dht_insert(key, value):
    #    global dht
    #    print(p)
    #    return json.dumps(dht.insert(key, value))

    @bottle.route('/dht/<key>/<value>')
    def dht_insert(key, value):
        #global dht
        #return json.dumps(dht.insert(key, value))
        #return json.dumps(insert_dht(key, value))
        return json.dumps(key, value)


'''---------------------------------------------------------------------------------'''
class PeerToPeerServer:
    def __init__(self, port, peers):
        self.myPort = port
        self.peers = peers
        self.hostLocal1 = 'localhost'
        self.urlLocal = 'http://'

    #Nos métodos abaixo ver como fazer pra usar as informações da classe.
    @bottle.route('/peers/<hostLocal>/<myPort>')
    def index(hostLocal, myPort):
        try:
            teste = peers.index(urlLocal+hostLocal+':'+myPort)
            return json.dumps(peers)
        except Exception as e:
            peers.append(urlLocal+hostLocal+':'+myPort)
            return json.dumps(peers)

    def client():
        time.sleep(5)
        while True:
            time.sleep(1)
            np = []
            for p in peers:
                r = requests.get(p + '/peers/'+hostLocal1+'/'+myPort1)
                np = np + json.loads(r.text)
                print(r.text)
                time.sleep(1)
            peers[:] = list(set(np + peers))

    def start_PeerToPeer_Server(self):
        t = threading.Thread(target=client)
        t.start()
        bottle.run(host=self.hostLocal, port=int(self.myPort))



'''---------------------------------------------------------------------------------'''

class DistribuicaoArquivos:
    def __init__(self, port, peers):
        self.myPort = port
        self.peers = peers

    def initDht(self):
        self.servidorDht = DhtServer(self.myPort)
        self.servidorDht.start_dht_Server()

    def initPeerToPeer(self):
        self.servidorPeerToPeer = PeerToPeerServer(self.myPort, self.peers)
        self.servidorPeerToPeer.start_PeerToPeer_Server()


#implementação, separar dos arquivos de classe

servidor = DistribuicaoArquivos(sys.argv[1], sys.argv[2:])
servidor.initDht()
#servidor.initPeerToPeer()

