"""ethernet_frame.py: an Ethernet frame built byte by byte, carrying an ARP request."""
import zlib

BROADCAST = bytes([0xFF] * 6)
MY_MAC = bytes([0x02, 0, 0, 0, 0, 0x01])       # 0x02: locally administered
MY_IP, ASKED_IP = bytes([10, 0, 0, 1]), bytes([10, 0, 0, 2])


def mac(b):
    return ":".join(f"{x:02x}" for x in b)


def arp_request(sender_mac, sender_ip, target_ip):
    return (
        (1).to_bytes(2, "big")                 # hardware: Ethernet
        + (0x0800).to_bytes(2, "big")          # protocol: IPv4
        + bytes([6, 4])                        # address lengths
        + (1).to_bytes(2, "big")               # operation: request
        + sender_mac + sender_ip + bytes(6) + target_ip    # target MAC: unknown
    )


def ethernet(dst, src, ethertype, payload):
    body = dst + src + ethertype.to_bytes(2, "big") + payload.ljust(46, b"\0")
    return body + zlib.crc32(body).to_bytes(4, "little")   # the frame check


if __name__ == "__main__":
    frame = ethernet(BROADCAST, MY_MAC, 0x0806, arp_request(MY_MAC, MY_IP, ASKED_IP))
    for off in range(0, len(frame), 16):
        print(f"{off:04x}  {frame[off:off + 16].hex(' ')}")
    dst, src, kind = mac(frame[0:6]), mac(frame[6:12]), frame[12:14].hex()
    print(f"{len(frame)} bytes: destination {dst}, source {src}")
    print(f"type {kind}, payload 46 bytes (28 of ARP), check {frame[-4:].hex()}")
    b = frame[6]
    print(f"source's first byte {b:02x}: group bit {b & 1}, local bit {b >> 1 & 1}")
    sent = int.from_bytes(frame[-4:], "little")
    print("receiver's check:", zlib.crc32(frame[:-4]) == sent)
