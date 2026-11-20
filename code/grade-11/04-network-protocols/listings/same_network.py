import ipaddress

net = ipaddress.ip_network("192.0.2.0/26")
print(net, "mask", net.netmask, "->", net.num_addresses, "addresses")
print("first", net.network_address, "last", net.broadcast_address)
for a in ["192.0.2.37", "192.0.2.64", "198.51.100.7"]:
    print(a, "in", net, ":", ipaddress.ip_address(a) in net)
host = ipaddress.ip_interface("192.0.2.37/24")
print(host, "belongs to the network", host.network)
