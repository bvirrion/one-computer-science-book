"""caching_resolver.py: iterative resolution that remembers answers and referrals
for their lifetimes (exercise 9)."""
from dns_message import decode, query

ROOT_ADDRESS = "192.0.2.53"


class CachingResolver:
    def __init__(self, send, clock):
        self.send, self.clock, self.cache, self.queries = send, clock, {}, 0

    def lookup(self, key):
        hit = self.cache.get(key)
        return hit[1] if hit and hit[0] > self.clock() else None

    def keep(self, key, records):
        ttl = min(r[2] for r in records)         # the shortest lifetime decides
        self.cache[key] = (self.clock() + ttl, records)

    def resolve(self, name, rtype):
        if (hit := self.lookup((name, rtype))) is not None:
            return hit
        server, labels = ROOT_ADDRESS, name.split(".")
        for i in range(1, len(labels) + 1):      # the closest known zone cut
            known = self.lookup((".".join(labels[i:]), "glue"))
            if known:
                server = known[0][3]
                break
        while True:
            self.queries += 1
            reply = decode(self.send(server, query(self.queries, name, rtype)))
            if reply["answer"] or not reply["authority"]:
                if reply["answer"]:
                    self.keep((name, rtype), reply["answer"])
                return reply["answer"]
            ns = reply["authority"][0]
            glue = [g for g in reply["additional"] if g[0] == ns[3]]
            self.keep((ns[0], "glue"), glue)     # whom to ask for that zone
            server = glue[0][3]
