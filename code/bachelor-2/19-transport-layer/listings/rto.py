"""rto.py: the retransmission timeout estimated from round-trip samples (in ms)."""
ALPHA, BETA, K, MIN_RTO = 1 / 8, 1 / 4, 4, 1000


def estimate(samples):
    srtt = rttvar = None
    for r in samples:
        if srtt is None:                         # the first measurement
            srtt, rttvar = r, r / 2
        else:                                    # rttvar first, with the old srtt
            rttvar = (1 - BETA) * rttvar + BETA * abs(srtt - r)
            srtt = (1 - ALPHA) * srtt + ALPHA * r
        computed = srtt + K * rttvar
        yield r, srtt, rttvar, computed, max(computed, MIN_RTO)


if __name__ == "__main__":
    for samples in ([100, 120, 90, 110, 400, 100, 105], [800, 800, 1600, 800]):
        print(" sample    srtt  rttvar  srtt+4var    rto")
        for row in estimate(samples):
            print("".join(f"{v:8.1f}" if i else f"{v:7}" for i, v in enumerate(row)))
