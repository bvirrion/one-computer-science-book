"""arp_sim.py: three hosts on a link resolve IP addresses to MAC addresses."""

LIFETIME = 60                                  # seconds an entry stays in a cache


class Host:
    def __init__(self, name, ip, mac):
        self.name, self.ip, self.mac, self.cache = name, ip, mac, {}

    def lookup(self, ip, now):
        entry = self.cache.get(ip)
        if entry and now - entry[1] < LIFETIME:
            return entry[0]
        return None


def send(link, sender, ip, now):
    mac = sender.lookup(ip, now)
    if mac:
        print(f"t={now:3}  {sender.name}: {ip} is {mac} (cache), frame sent")
        return
    print(f"t={now:3}  {sender.name}: broadcast 'who has {ip}? tell {sender.ip}'")
    for h in link:
        if h is sender:
            continue
        if h.ip == ip:                         # the target learns the sender too
            h.cache[sender.ip] = (sender.mac, now)
            print(f"        {h.name}: reply '{ip} is at {h.mac}' to {sender.name}")
            sender.cache[ip] = (h.mac, now)
        else:
            print(f"        {h.name}: not mine, ignored")
    print(f"        {sender.name}: frame sent to {sender.lookup(ip, now)}")


if __name__ == "__main__":
    a = Host("A", "10.0.0.1", "02:00:00:00:00:01")
    b = Host("B", "10.0.0.2", "02:00:00:00:00:02")
    c = Host("C", "10.0.0.3", "02:00:00:00:00:03")
    link = [a, b, c]
    send(link, a, "10.0.0.3", 0)
    send(link, a, "10.0.0.3", 5)
    send(link, c, "10.0.0.1", 9)
    send(link, a, "10.0.0.3", 70)
