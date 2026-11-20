"""Exercises of the chapter on network protocols."""
import ipaddress


def network_address(cidr):                       # exercise 1
    return str(ipaddress.ip_interface(cidr).network.network_address)


def hosts(prefix):                       # exercise 2: minus network and broadcast
    return 2 ** (32 - prefix) - 2


def same_network(a, b, prefix):                  # exercise 5
    m = (2**32 - 1) ^ (2**(32 - prefix) - 1)
    return int(ipaddress.ip_address(a)) & m == int(ipaddress.ip_address(b)) & m


def network_with_or(a, prefix):                  # exercise 6: the bug
    m = (2**32 - 1) ^ (2**(32 - prefix) - 1)
    return str(ipaddress.ip_address(int(ipaddress.ip_address(a)) | m))


def lookup(table, address):                      # exercise 7
    a = ipaddress.ip_address(address)
    fits = [(ipaddress.ip_network(d), hop) for d, hop in table
            if a in ipaddress.ip_network(d)]
    return max(fits, key=lambda f: f[0].prefixlen)[1] if fits else None


def receiver(frames, check_bit=True):            # exercises 10 and 14
    expected, delivered = 0, []
    for bit, data in frames:
        if bit == expected or not check_bit:
            delivered.append(data)
            expected = 1 - bit
    return delivered


def window_time(n, w, rtt):                      # exercise 13: one packet per tick
    """Ticks to send n packets with at most w unacknowledged; an ack comes rtt after."""
    acks, tick, sent = [], 0, 0
    while sent < n:
        acks = [a for a in acks if a > tick]     # acks arrived by now free the window
        if len(acks) < w:
            acks.append(tick + 1 + rtt)
            sent += 1
        tick += 1
    return max(acks)                             # when the last ack comes back


def subnets(cidr, parts):                        # exercise 15
    net = ipaddress.ip_network(cidr)
    return [str(s) for s in net.subnets(prefixlen_diff=(parts - 1).bit_length())]


if __name__ == "__main__":
    print(network_address("192.168.10.37/24"), hosts(26))
    print(same_network("192.0.2.37", "192.0.2.64", 26))
    print(network_with_or("192.0.2.37", 26))
    frames = [(0, "a"), (0, "a"), (1, "b")]
    print(receiver(frames), receiver(frames, check_bit=False))
    print(receiver([(0, "a"), (1, "b"), (0, "a"), (0, "c")]))
    print([window_time(10, w, 4) for w in (1, 2, 5)])
    print(subnets("192.0.2.0/24", 4))
