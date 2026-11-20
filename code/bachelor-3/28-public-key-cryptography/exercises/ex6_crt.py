"""Exercise 6: RSA decryption with the Chinese remainder theorem. Compute m modulo p
and modulo q with half-size exponents, then recombine (Garner's formula)."""


def decrypt_crt(priv, c, power=pow):
    p, q, d = priv["p"], priv["q"], priv["d"]
    mp = power(c % p, d % (p - 1), p)  # m mod p, by Fermat: exponents work mod p - 1
    mq = power(c % q, d % (q - 1), q)
    h = pow(q, -1, p) * (mp - mq) % p
    return mq + h * q  # = mq mod q, and = mp mod p
