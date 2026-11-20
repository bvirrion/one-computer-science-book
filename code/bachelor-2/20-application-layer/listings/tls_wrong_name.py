"""tls_wrong_name.py: the same certificate, presented for another name."""
import socket
import ssl
import threading

server_ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
server_ctx.load_cert_chain("cert.pem", "key.pem")
listener = socket.create_server(("127.0.0.1", 44206))


def serve():
    conn, _ = listener.accept()
    try:
        server_ctx.wrap_socket(conn, server_side=True)
    except ssl.SSLError:
        pass                                     # the client gave up


threading.Thread(target=serve, daemon=True).start()
client_ctx = ssl.create_default_context(cafile="cert.pem")
with socket.create_connection(("127.0.0.1", 44206)) as raw:
    try:
        client_ctx.wrap_socket(raw, server_hostname="mail.brenmoor.test")
        print("connected (this must not happen)")
    except ssl.SSLCertVerificationError as e:
        print("refused:", e.verify_message)
