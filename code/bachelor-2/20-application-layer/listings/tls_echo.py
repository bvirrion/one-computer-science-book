"""tls_echo.py: an echo server and a client that checks who it is talking to."""
import socket
import ssl
import threading

server_ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
server_ctx.load_cert_chain("cert.pem", "key.pem")    # made by openssl just before
listener = socket.create_server(("127.0.0.1", 44205))


def serve():
    conn, _ = listener.accept()
    with server_ctx.wrap_socket(conn, server_side=True) as tls:
        tls.sendall(tls.recv(1024).upper())      # decrypted, answered, encrypted


threading.Thread(target=serve, daemon=True).start()
client_ctx = ssl.create_default_context(cafile="cert.pem")   # trust only this one
with socket.create_connection(("127.0.0.1", 44205)) as raw:
    with client_ctx.wrap_socket(raw, server_hostname="www.brenmoor.test") as tls:
        print("version:", tls.version())
        print("cipher: ", tls.cipher()[0])
        subject = dict(x[0] for x in tls.getpeercert()["subject"])
        print("server certificate for:", subject["commonName"], "(verified)")
        tls.sendall(b"hello from the library")
        print("echo:", tls.recv(1024).decode())
