import requests
import json
import threading
import time


class PeerToPeerServer:
    def __init__(self, port, peers):
        self.myPort = port
        self.peers = peers
        self.hostLocal = 'localhost'
        self.urlLocal = 'http://'

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
