"""tls13_trace.py -- the shape of a TLS 1.3 full handshake (RFC 8446, figure 1), run
between two Python objects: ephemeral Diffie--Hellman, a key schedule with HKDF, a
certificate chain, a signature over the transcript, and Finished MACs. The structure
of TLS 1.3, simplified: no record layer, no real encodings, toy groups and keys."""

import hashlib
import hmac
import random
import sys
from pathlib import Path

import schnorr
from toy_cert import check_chain, make_cert

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "exercises"))
from ex12_hkdf import expand, extract  # noqa: E402

P, Q, G = schnorr.P, schnorr.Q, schnorr.G
rng = random.Random(28)


def derive(secret, label, transcript):
    """Derive-Secret: a secret bound to a label and to the hash of the transcript."""
    th = hashlib.sha256(b"".join(m for _, _, m in transcript)).digest()
    return expand(secret, b"tls13 " + label.encode() + th, 32)


def finished_mac(secret, transcript):
    th = hashlib.sha256(b"".join(m for _, _, m in transcript)).digest()
    return hmac.new(expand(secret, b"tls13 finished", 32), th, hashlib.sha256).digest()


def handshake(eve=False):
    t = []  # the transcript: (sender, name, bytes), in order
    a = rng.randrange(1, Q)  # the client's ephemeral secret
    t.append(("client", "ClientHello + key_share", pow(G, a, P).to_bytes(128, "big")))
    b = rng.randrange(1, Q)  # the server's ephemeral secret
    t.append(("server", "ServerHello + key_share", pow(G, b, P).to_bytes(128, "big")))
    if eve:  # Eve swaps the server's share for her own on its way to the client
        e = rng.randrange(1, Q)
        client_view = t[:1] + [("server", t[1][1], pow(G, e, P).to_bytes(128, "big"))]
    else:
        client_view = list(t)
    early = extract(b"", bytes(32))
    shared_s = pow(int.from_bytes(t[0][2], "big"), b, P).to_bytes(128, "big")
    hs = extract(derive(early, "derived", []), shared_s)  # handshake secret
    s_hs = derive(hs, "s hs traffic", t)
    t.append(("server", "{EncryptedExtensions}", b"no extensions"))
    t.append(("server", "{Certificate}", repr(CHAIN).encode()))
    th = hashlib.sha256(b"".join(m for *_, m in t)).digest()
    # the server's long-term key signs the transcript so far
    r, s = schnorr.sign(LIB_X, th, rng)
    sig = r.to_bytes(128, "big") + s.to_bytes(20, "big")
    t.append(("server", "{CertificateVerify}", sig))
    t.append(("server", "{Finished}", finished_mac(s_hs, t)))
    # The client: the same computation on what it received
    client_view += t[2:]
    shared_c = pow(int.from_bytes(client_view[1][2], "big"), a, P).to_bytes(128, "big")
    hs_c = extract(derive(early, "derived", []), shared_c)
    checks = {"chain": check_chain(CHAIN, ANCHORS, "2026-11-20") == "ok"}
    signed = hashlib.sha256(b"".join(m for *_, m in client_view[:4])).digest()
    got = client_view[4][2]
    sig_c = int.from_bytes(got[:128], "big"), int.from_bytes(got[128:], "big")
    checks["signature"] = schnorr.verify(CHAIN[0]["body"]["key"], signed, sig_c)
    checks["server Finished"] = hmac.compare_digest(
        client_view[5][2],
        finished_mac(derive(hs_c, "s hs traffic", client_view[:2]), client_view[:5]),
    )
    # The client answers with its own Finished; both derive the application secrets
    c_hs = derive(hs_c, "c hs traffic", client_view[:2])
    t.append(("client", "{Finished}", finished_mac(c_hs, client_view)))
    client_view.append(t[-1])
    master_s = extract(derive(hs, "derived", []), bytes(32))
    master_c = extract(derive(hs_c, "derived", []), bytes(32))
    app_s = derive(master_s, "s ap traffic", t[:6])
    app_c = derive(master_c, "s ap traffic", client_view[:6])
    return t, checks, app_s == app_c


root_x, root_y = schnorr.keygen(rng)
LIB_X, lib_y = schnorr.keygen(rng)
ANCHORS = {"Root CA": root_y}
CHAIN = [make_cert("library.example", lib_y, "Root CA", root_x, ca=False)]

t, checks, same = handshake()
for sender, name, data in t:
    arrow = "-->" if sender == "client" else "<--"
    print(f"{arrow} {name:26} {len(data):5} bytes")
print("client checks:", checks)
print("same application secret on both sides:", same)
t, checks, same = handshake(eve=True)
print("with Eve's key share, client checks:", checks)
print("same application secret on both sides:", same)
