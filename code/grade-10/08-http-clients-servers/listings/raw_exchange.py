import socket

from serve import running

REQUEST = b"GET /hello HTTP/1.1\r\nHost: 127.0.0.1\r\nConnection: close\r\n\r\n"

with running(42084):
    with socket.create_connection(("127.0.0.1", 42084)) as s:
        s.sendall(REQUEST)
        reply = b""
        while chunk := s.recv(4096):
            reply += chunk
    for line in reply.split(b"\r\n"):
        if not line.startswith(b"Date:"):
            print(line)
