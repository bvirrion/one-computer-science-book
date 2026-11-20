"""A chain of toy certificates: each one signed by the key of the one above it."""
from mini_rsa import make_keys, sign, verify

root_pub, root_priv = make_keys(1009, 1013, 65537)        # the authority's keys
mid_pub, mid_priv = make_keys(2003, 2011, 65537)          # an intermediate's
site_pub, site_priv = make_keys(3001, 3011, 65537)        # the web site's


def certificate(name, public, issuer, issuer_private):
    """A name bound to a public key, signed by the issuer."""
    body = f"{name}|{public}|issued by {issuer}"
    return body, sign(issuer_private, body)


mid_cert = certificate("Toy Intermediate", mid_pub, "Toy Root", root_priv)
site_cert = certificate("library.example", site_pub, "Toy Intermediate", mid_priv)


def check_chain(site_cert, mid_cert, trusted_root):
    """The browser knows only the root's public key."""
    ok_mid = verify(trusted_root, *mid_cert)
    mid_key = tuple(int(x) for x in mid_cert[0].split("|")[1].strip("()").split(","))
    ok_site = verify(mid_key, *site_cert)
    return ok_mid and ok_site


if __name__ == "__main__":
    print("site certificate:", site_cert[0], " signature", site_cert[1])
    print("chain accepted:", check_chain(site_cert, mid_cert, root_pub))
    fake_pub, _ = make_keys(4001, 4003, 65537)            # an attacker's key
    forged = (f"library.example|{fake_pub}|issued by Toy Intermediate", site_cert[1])
    print("forged certificate accepted:", check_chain(forged, mid_cert, root_pub))
