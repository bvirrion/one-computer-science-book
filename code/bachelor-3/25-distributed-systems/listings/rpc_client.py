"""rpc_client.py -- the client stub: bank.deposit("bakery", 10) becomes a request
line with a fresh id, sent until a reply with that id comes back or the retries run
out. Every step is printed."""

import json
import socket


class Stub:
    def __init__(self, port, name, timeout=0.5, retries=3):
        self.sock = socket.create_connection(("127.0.0.1", port))
        self.sock.settimeout(timeout)
        self.buf, self.name, self.retries, self.n = b"", name, retries, 0

    def readline(self):
        while b"\n" not in self.buf:
            self.buf += self.sock.recv(4096)
        line, _, self.buf = self.buf.partition(b"\n")
        return line

    def __getattr__(self, method):
        def call(*args):
            self.n += 1
            req = {"id": f"{self.name}-{self.n}", "method": method, "args": list(args)}
            line = (json.dumps(req) + "\n").encode()  # marshal
            for attempt in range(1, self.retries + 1):
                print(f"  send {req['id']} {method}{tuple(args)} (attempt {attempt})")
                self.sock.sendall(line)
                try:
                    reply = json.loads(self.readline())  # unmarshal
                    while reply["id"] != req["id"]:  # a late reply to an earlier try
                        reply = json.loads(self.readline())
                except TimeoutError:
                    print(f"  no reply to {req['id']} in time")
                    continue
                print(f"  reply {reply['id']}: {reply['result']}")
                return reply["result"]
            raise TimeoutError(f"{req['id']}: no reply after {self.retries} attempts")

        return call

    def close(self):
        self.sock.close()
