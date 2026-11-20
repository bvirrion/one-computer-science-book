"""rpc_server.py -- a bank's accounts behind a remote procedure call server on TCP.
A request is one line of JSON, {"id": ..., "method": ..., "args": [...]}, and so is
the reply, {"id": ..., "result": ...}. In at-most-once mode the server remembers
the reply to each request id and answers a repeated request from that memory."""

import json
import socketserver
import threading


class Bank:
    def __init__(self):
        self.accounts, self.executed = {}, 0

    def deposit(self, account, amount):
        self.executed += 1
        self.accounts[account] = self.accounts.get(account, 0) + amount
        return self.accounts[account]

    def balance(self, account):
        return self.accounts.get(account, 0)


class Handler(socketserver.StreamRequestHandler):
    def handle(self):
        srv = self.server
        for line in self.rfile:
            req = json.loads(line)  # unmarshal
            with srv.lock:
                if srv.at_most_once and req["id"] in srv.replies:
                    result = srv.replies[req["id"]]  # a duplicate: not executed again
                else:
                    result = getattr(srv.bank, req["method"])(*req["args"])
                    srv.replies[req["id"]] = result
            reply = json.dumps({"id": req["id"], "result": result}) + "\n"
            self.wfile.write(reply.encode())  # marshal


class Server(socketserver.ThreadingTCPServer):
    allow_reuse_address = daemon_threads = True

    def __init__(self, port, at_most_once):
        super().__init__(("127.0.0.1", port), Handler)
        self.bank, self.at_most_once = Bank(), at_most_once
        self.replies, self.lock = {}, threading.Lock()

    def start(self):
        threading.Thread(target=self.serve_forever, daemon=True).start()
        return self
