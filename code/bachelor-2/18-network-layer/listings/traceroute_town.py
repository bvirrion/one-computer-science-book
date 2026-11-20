"""traceroute_town.py: time to live 1, 2, 3 ... across the town's routers."""
from link_state import dijkstra
from town_network import load

g, names = load()
laptop_at, server_at = "3", "30"               # the Library's router; a far place's


def address(place):
    return f"198.51.100.{place}"


def send(ttl):
    """Forward hop by hop; return who answers and why."""
    here = laptop_at
    while True:
        ttl -= 1                               # every router takes one off
        if here == server_at:
            return here, "reply from the server"
        if ttl == 0:
            return here, "time exceeded"       # the packet dies; the router says where
        here = dijkstra(g, here)[1][server_at]  # next hop on a shortest path


print(f"from {address(laptop_at)} ({names[laptop_at]}) to the server at "
      f"{address(server_at)} ({names[server_at]})")
for ttl in range(1, 30):
    who, what = send(ttl)
    print(f"{ttl:2}  {address(who):15} {names[who]:18} {what}")
    if what.startswith("reply"):
        break
