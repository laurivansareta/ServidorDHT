import bottle
from dhtServer import DhtServer
from peerToPeerServer import PeerToPeerServer


class DistribuicaoArquivos:
    def __init__(self, port, peers):
        self.myPort = port
        self.peers = peers
        self.servidorDht = DhtServer(self.myPort)
        self.servidorPeerToPeer = PeerToPeerServer(self.myPort, self.peers)
        self.b = bottle.Bottle()
        self.b.get('/dht/<key>')(self.servidorDht.lookup_dht)
        self.b.route('/dht/<key>/<value>')(self.dht_insert)
        self.b.route('/peers/<host>/<port>')(self.servidorPeerToPeer.index)
        self.init_PeerToPeer()

    def dht_insert(self, key, value):
        return self.servidorDht.insert_dht(key, value, self.servidorPeerToPeer.get_peers())

    def init_PeerToPeer(self):
        self.servidorPeerToPeer.start_PeerToPeer_Server()

    def run(self):
        self.b.run(host='localhost', port=self.myPort)

