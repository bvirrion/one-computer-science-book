"""chunked.py: decode a body sent with Transfer-Encoding: chunked (exercise 5)."""


def dechunk(data):
    """Return (body, bytes used); raise ValueError if the coding is cut short."""
    body, pos = b"", 0
    while True:
        end = data.find(b"\r\n", pos)
        if end < 0:
            raise ValueError("no size line")
        size = int(data[pos:end].split(b";")[0], 16)   # hex; extensions ignored
        pos = end + 2
        if size == 0:                            # the last chunk; then an empty line
            if data[pos:pos + 2] != b"\r\n":
                raise ValueError("no final empty line")
            return body, pos + 2
        if data[pos + size:pos + size + 2] != b"\r\n":
            raise ValueError("chunk shorter than its size")
        body += data[pos:pos + size]
        pos += size + 2
