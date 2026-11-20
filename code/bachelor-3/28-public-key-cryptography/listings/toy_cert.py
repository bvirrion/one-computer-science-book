"""toy_cert.py -- a toy certificate format: a subject, its public key, an issuer, a
validity period and a flag saying whether it may sign certificates, signed by the
issuer with schnorr.py. A three-certificate chain is checked against a trust anchor;
then a forged leaf is checked. Real certificates are X.509, checked by a library."""

import json
import random

import schnorr

rng = random.Random(28)


def make_cert(subject, y, issuer, issuer_x, ca, not_after="2027-12-31"):
    body = {
        "subject": subject,
        "key": y,
        "issuer": issuer,
        "ca": ca,
        "not_before": "2026-01-01",
        "not_after": not_after,
    }
    data = json.dumps(body, sort_keys=True).encode()  # one canonical byte string
    return {"body": body, "sig": schnorr.sign(issuer_x, data, rng)}


def check_chain(chain, anchors, today):
    """chain[0] is the server's certificate, each signed by the next; the last must be
    signed by a trust anchor. Return "ok" or the reason for refusing."""
    for i, cert in enumerate(chain):
        body = cert["body"]
        if not body["not_before"] <= today <= body["not_after"]:
            return f"{body['subject']}: expired or not yet valid"
        if i + 1 < len(chain):
            issuer = chain[i + 1]["body"]
            if issuer["subject"] != body["issuer"] or not issuer["ca"]:
                return f"{body['subject']}: issuer is not a CA in the chain"
            y = issuer["key"]
        elif body["issuer"] in anchors:
            y = anchors[body["issuer"]]
        else:
            return f"{body['subject']}: no trust anchor named {body['issuer']}"
        data = json.dumps(body, sort_keys=True).encode()
        if not schnorr.verify(y, data, cert["sig"]):
            return f"{body['subject']}: bad signature"
    return "ok"


if __name__ == "__main__":
    root_x, root_y = schnorr.keygen(rng)  # the root CA: its key is in every client
    mid_x, mid_y = schnorr.keygen(rng)
    lib_x, lib_y = schnorr.keygen(rng)
    anchors = {"Root CA": root_y}
    mid = make_cert("Regional CA", mid_y, "Root CA", root_x, ca=True)
    leaf = make_cert("library.example", lib_y, "Regional CA", mid_x, ca=False)
    print("library's chain:", check_chain([leaf, mid], anchors, "2026-11-20"))
    print("checked in 2028:", check_chain([leaf, mid], anchors, "2028-01-01"))

    eve_x, eve_y = schnorr.keygen(rng)
    forged = {"body": dict(leaf["body"], key=eve_y), "sig": leaf["sig"]}  # Eve's key
    print("leaf with Eve's key:", check_chain([forged, mid], anchors, "2026-11-20"))
    self_made = make_cert("Regional CA", eve_y, "Root CA", eve_x, ca=True)
    fake_leaf = make_cert("library.example", eve_y, "Regional CA", eve_x, ca=False)
    print(
        "Eve's own chain:", check_chain([fake_leaf, self_made], anchors, "2026-11-20")
    )
    print(
        "library's leaf used as a CA:",
        check_chain(
            [
                make_cert("town.example", eve_y, "library.example", lib_x, ca=False),
                leaf,
                mid,
            ],
            anchors,
            "2026-11-20",
        ),
    )
