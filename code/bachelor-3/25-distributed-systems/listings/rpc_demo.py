"""rpc_demo.py -- a bank server on 127.0.0.1:45101 and, in front of it on 45102, a
proxy that loses the second reply it carries. A client deposits 10 three times
through the proxy, first against an at-least-once server, then an at-most-once one."""

import socket
import threading

from rpc_client import Stub
from rpc_server import Server


def proxy(listen, target, lose):
    """Forward one connection both ways; drop the replies numbered in `lose`."""
    srv = socket.create_server(("127.0.0.1", listen))

    def run():
        client, _ = srv.accept()
        upstream = socket.create_connection(("127.0.0.1", target))
        threading.Thread(target=pump, args=(client, upstream, ()), daemon=True).start()
        pump(upstream, client, lose)

    def pump(src, dst, lose):
        for n, line in enumerate(src.makefile("rb"), start=1):
            if n not in lose:
                dst.sendall(line)

    threading.Thread(target=run, daemon=True).start()
    return srv


def demo(at_most_once, lose=(2,), port=45101, calls=3):
    server = Server(port, at_most_once).start()
    front = proxy(port + 1, port, lose)
    bank = Stub(port + 1, "c")
    for _ in range(calls):
        bank.deposit("bakery", 10)
    result = server.bank.executed, server.bank.balance("bakery")
    bank.close()
    front.close()
    server.shutdown()
    server.server_close()
    return result


if __name__ == "__main__":
    for mode, at_most_once in (("at-least-once", False), ("at-most-once", True)):
        print(f"-- {mode} server")
        executed, balance = demo(at_most_once)
        print(f"deposits executed: {executed}, balance: {balance}")
