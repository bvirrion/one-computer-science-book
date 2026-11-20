"""directory_client.py: ask the directory service. Usage: port request..."""
import socket
import struct
import sys


def recv_all(sock, n):
    data = b""
    while len(data) < n:                          # recv may return part of n
        part = sock.recv(n - len(data))
        if not part:
            raise ConnectionError("the server closed the connection early")
        data += part
    return data


def ask(port, request):
    with socket.create_connection(("127.0.0.1", port)) as sock:
        body = request.encode()
        sock.sendall(struct.pack("!I", len(body)) + body)    # !I: 4 bytes, big-endian
        (n,) = struct.unpack("!I", recv_all(sock, 4))
        return recv_all(sock, n).decode()


if __name__ == "__main__":
    port = int(sys.argv[1])
    for request in sys.argv[2:]:
        print(f"{request!r:22} -> {ask(port, request)}")
