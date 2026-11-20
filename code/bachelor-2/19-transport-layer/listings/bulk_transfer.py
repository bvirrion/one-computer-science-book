"""bulk_transfer.py: 256 MiB over TCP on 127.0.0.1, small and large receive buffers."""
import socket
import threading
import time

TOTAL, PORT = 256 * 2**20, 44192


def receive(server, rcvbuf, result):
    conn, _ = server.accept()
    got = 0
    while chunk := conn.recv(65536):
        got += len(chunk)
    conn.close()
    result.append(got)


for rcvbuf in (4096, 65536, None):
    server = socket.socket()
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    if rcvbuf:                                   # set before listen: accept inherits it
        server.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, rcvbuf)
    server.bind(("127.0.0.1", PORT))
    server.listen(1)
    result = []
    t = threading.Thread(target=receive, args=(server, rcvbuf, result))
    t.start()
    block = bytes(65536)
    start = time.perf_counter()
    with socket.create_connection(("127.0.0.1", PORT)) as c:
        for _ in range(TOTAL // len(block)):
            c.sendall(block)
    t.join()
    seconds = time.perf_counter() - start
    server.close()
    label = f"{rcvbuf} bytes" if rcvbuf else "the system's default"
    print(f"receive buffer {label:20} {result[0] / seconds / 1e6:8.0f} MB/s")
