import requests
import bottle
import json
import threading
import time
import sys

peers = sys.argv[2:]
myPort1 = sys.argv[1]
hostLocal1 = 'localhost'
urlLocal = 'http://'

@bottle.route('/peers/<hostLocal>/<myPort>')
def index(hostLocal,myPort):
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

        #print(peers)

t = threading.Thread(target=client)
t.start()

bottle.run(host=hostLocal1, port=int(myPort1))
