"""Each layer wraps what the layer above gives it in its own header (toy headers)."""
import ipaddress


def transport(data, src_port, dst_port):
    return src_port.to_bytes(2, "big") + dst_port.to_bytes(2, "big") + data


def network(segment, src, dst):
    return ipaddress.ip_address(src).packed + ipaddress.ip_address(dst).packed + segment


def mac(text):
    return bytes.fromhex(text.replace(":", ""))


def link(packet, src_mac, dst_mac):
    return mac(dst_mac) + mac(src_mac) + bytes([0x08, 0x00]) + packet


def show(name, data, header):
    print(f"{name:12}{data[:header].hex(' '):42}| {len(data) - header} bytes inside")


message = b"GET / HTTP/1.1\r\n\r\n"
segment = transport(message, 49152, 80)
packet = network(segment, "192.0.2.10", "198.51.100.7")
frame = link(packet, "02:00:00:00:00:0a", "02:00:00:00:00:01")
show("link", frame, 14)
show("network", packet, 8)
show("transport", segment, 4)
print(f"{'application':12}{message}")
print("frame:", len(frame), "bytes, of which", len(frame) - len(message), "of headers")
