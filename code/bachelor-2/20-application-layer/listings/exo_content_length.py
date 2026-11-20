"""exo_content_length.py: a server that promises 12 bytes and sends 10 (exercise 6)."""
import http.client
import socket
import threading

listener = socket.create_server(("127.0.0.1", 44204))


def serve():
    conn, _ = listener.accept()
    conn.recv(1024)
    conn.sendall(b"HTTP/1.1 200 OK\r\nContent-Length: 12\r\n\r\n0123456789")
    threading.Event().wait(5)                    # keeps the connection open


threading.Thread(target=serve, daemon=True).start()
conn = http.client.HTTPConnection("127.0.0.1", 44204, timeout=1)
conn.request("GET", "/")
reply = conn.getresponse()
try:
    reply.read()
except TimeoutError:
    print("no answer after 1 s: the client is still waiting for 2 bytes")
