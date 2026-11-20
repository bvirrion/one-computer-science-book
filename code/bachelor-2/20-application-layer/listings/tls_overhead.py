"""tls_overhead.py: bytes on the wire for a message, after the handshake."""
import ssl

server_ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
server_ctx.load_cert_chain("cert.pem", "key.pem")
client_ctx = ssl.create_default_context(cafile="cert.pem")
c_in, c_out, s_in, s_out = (ssl.MemoryBIO() for _ in range(4))
client = client_ctx.wrap_bio(c_in, c_out, server_hostname="www.brenmoor.test")
server = server_ctx.wrap_bio(s_in, s_out, server_side=True)


def pump():                                      # carry bytes between the two ends
    s_in.write(c_out.read())
    c_in.write(s_out.read())


for _ in range(4):                               # the handshake, flight by flight
    for end in (client, server):
        try:
            end.do_handshake()
        except ssl.SSLWantReadError:
            pass
    pump()
print("handshake done:", client.version(), client.cipher()[0])
print("  message   on the wire   records   extra bytes per record")
for n in (1, 100, 1000, 16384, 16385, 100_000):
    client.write(b"x" * n)
    wire = len(c_out.read())                     # what would cross the network
    records = -(-n // 16384)                     # at most 2^14 bytes per record
    print(f"{n:9} {wire:13} {records:9} {(wire - n) / records:14.0f}")
