"""traceroute_town.py: time to live 1, 2, 3 ... across the town's routers."""
from link_state import dijkstra
from town_network import load

g, names = load()
laptop_at, server_at = "3", "30"               # the Library's network; a far place's
LAPTOP, SERVER = "203.0.113.25", "203.0.113.241"   # in the /29s of places 3 and 30


def address(place):
    return f"198.51.100.{place}"


def send(ttl):
    """Forward hop by hop; return who answers and why."""
    here = laptop_at                           # the laptop's own router comes first
    while True:
        ttl -= 1                               # every router takes one off
        if ttl == 0:
            return here, "time exceeded"       # the packet dies; the router says where
        if here == server_at:
            return None, "reply from the server"   # delivered on the café's own network
        here = dijkstra(g, here)[1][server_at]  # next hop on a shortest path


print(f"from {LAPTOP} ({names[laptop_at]}) to the server at {SERVER} "
      f"({names[server_at]})")
for ttl in range(1, 30):
    who, what = send(ttl)
    if who is None:
        print(f"{ttl:2}  {SERVER:15} {'server':18} {what}")
        break
    print(f"{ttl:2}  {address(who):15} {names[who]:18} {what}")
