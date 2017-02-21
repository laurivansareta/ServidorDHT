import hashlib


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
        return m.zfill(4)

    def __init__(self, k):
        self.p = self.gerar_hash(k)
        self.h = {}
        print("CHAVE " + self.p)
        print(type(self.h))
        print("\n")

        for sk in self.subkeys(self.p):
            self.h[sk + '0'] = None

        for sk in self.subkeys(self.p):
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
