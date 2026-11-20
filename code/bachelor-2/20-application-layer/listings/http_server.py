"""http_server.py: an HTTP/1.1 server on a socket, with persistent connections."""
import socket
import threading

PAGES = {"/": b"<h1>Brenmoor</h1>\n<p>Welcome to the town of Brenmoor.</p>\n",
         "/library": b"<h1>Library</h1>\n<p>Open 9:00 to 18:00.</p>\n",
         "/harbour": b"<h1>Harbour</h1>\n<p>Ferries every hour.</p>\n"}
stats = {"connections": 0, "requests": 0}


def handle(conn):
    stats["connections"] += 1
    reader = conn.makefile("rb")
    while True:
        line = reader.readline().decode()        # GET /library HTTP/1.1
        if not line:
            break                                # the client closed
        method, path, version = line.split()
        headers = {}
        while (h := reader.readline().decode().strip()):
            key, value = h.split(":", 1)
            headers[key.lower()] = value.strip()
        stats["requests"] += 1
        body = PAGES.get(path)
        status = "200 OK" if body else "404 Not Found"
        body = body or b"<h1>Not found</h1>\n"
        close = headers.get("connection") == "close" or version == "HTTP/1.0"
        head = (f"HTTP/1.1 {status}\r\nContent-Type: text/html\r\n"
                f"Content-Length: {len(body)}\r\n"
                + ("Connection: close\r\n" if close else "") + "\r\n").encode()
        conn.sendall(head if method == "HEAD" else head + body)
        if close:
            break
    conn.close()


def serve(port):
    server = socket.socket()
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(("127.0.0.1", port))
    server.listen()

    def loop():
        while True:
            conn, _ = server.accept()
            threading.Thread(target=handle, args=(conn,), daemon=True).start()
    threading.Thread(target=loop, daemon=True).start()
    return server
