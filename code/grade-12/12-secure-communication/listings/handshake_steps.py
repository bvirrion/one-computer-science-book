"""The steps of a secure connection, simplified, between two objects in one program."""
import hashlib
import random

from mini_rsa import sign, verify
from toy_certificate import check_chain, mid_cert, root_pub, site_cert, site_priv
from xor_stream import key_stream, xor_bytes

P, G = 2**61 - 1, 3
rng = random.Random(8446)                        # real code uses the secrets module

# 1. The client says hello and sends its Diffie-Hellman share.
a = rng.randrange(2, P - 1)
hello = ("client hello", pow(G, a, P))
print("client -> server:", hello)

# 2. The server answers with its share, its certificates, and a signature of the talk.
b = rng.randrange(2, P - 1)
answer = ("server hello", pow(G, b, P))
transcript = f"{hello}{answer}"
proof = sign(site_priv, transcript)              # only the site's private key can
print("server -> client:", answer, "+ 2 certificates + signature", proof)

# 3. The client checks the chain up to the root it trusts, then the signature.
site_key = tuple(int(x) for x in site_cert[0].split("|")[1].strip("()").split(","))
print("client: chain valid:", check_chain(site_cert, mid_cert, root_pub),
      "| signature valid:", verify(site_key, transcript, proof))

# 4. Both compute the shared secret, and a session key from it.
client_key = hashlib.sha256(str(pow(answer[1], a, P)).encode()).hexdigest()
server_key = hashlib.sha256(str(pow(hello[1], b, P)).encode()).hexdigest()
print("session keys equal:", client_key == server_key,
      "| key:", client_key[:16] + "...")

# 5. From now on, everything is encrypted with the session key (a toy cipher here).
request = b"GET /catalogue HTTP/1.1"
sent = xor_bytes(request, key_stream(client_key, len(request)))
print("on the wire:", sent.hex(" "))
print("server reads:", xor_bytes(sent, key_stream(server_key, len(sent))).decode())
