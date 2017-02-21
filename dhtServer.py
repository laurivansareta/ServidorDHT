from dht import DHT
import json


class DhtServer:
    def __init__(self, port):
        self.dht = DHT(port)

    def insert_dht(self, key, value):
        #usar este método para fazer as validações necessárias referente a inserção na dht.
        self.dht.insert(key, value)

    def lookup_dht(self, key):
        return self.dht.lookup(key)

    def dht_lookup(self, key):
        return self.dht.lookup(key)

    def dht_lookup_dump(self, key):
        return json.dumps(self.dht_lookup(key))

    def dht_insert(self, key, value):
        self.dht.insert(key, value)
        return json.dumps(key, value)