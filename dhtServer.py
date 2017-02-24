from urllib.parse import urlparse
import threading
import queue
from dht import DHT
import json
import requests
import time



class DhtServer:
    def __init__(self, port):
        self.dht = DHT(port)
        self.myPort = port
        self.fila = queue.Queue()
        self.t = threading.Thread(target=self.enviando)
        self.t.start()

    def enviando(self):
        while True:
            time.sleep(1)
            print('indo travar')
            try:
                key, value, peer = self.fila.get(block=False, timeout=2)
                print('voltando travar')
                try:
                    requests.get(peer + '/dht/' + key + '/' + value)
                except Exception as e:
                    print(peer + '/dht/' + key + '/' + value, '<<ERRO:', e)
            except:
                time.sleep(1)

    def envia_dht(self, key, value, peer):
        self.fila.put((key, value, peer))

    # usar este método para fazer as validações necessárias referente a inserção na dht.
    def insert_dht(self, key, value, peers):
        if not self.dht.lookup(key):
            self.dht.insert(key, value)
            for p in peers:
                a = urlparse(p)
                if a.port != int(self.myPort):
                    self.envia_dht(key, value, p)

    def lookup_dht(self, key):
        #regra para busca
        return self.dht.lookup(key)

    def dht_lookup(self, key):
        return self.dht.lookup(key)

    def dht_lookup_dump(self, key):
        return json.dumps(self.lookup_dht(key))

    def dht_insert_dump(self, key, value):
        self.dht.insert(key, value)
        return json.dumps(key, value)