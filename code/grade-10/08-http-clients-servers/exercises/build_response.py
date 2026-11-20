"""Exercises 6 and 8: a response built by hand, and the bytes of a request."""


def response_buggy(status, reason, body):
    head = f"HTTP/1.1 {status} {reason}\r\nContent-Type: text/plain\r\n"
    return head.encode() + body                      # no blank line, no length


def response(status, reason, body):
    head = (f"HTTP/1.1 {status} {reason}\r\nContent-Type: text/plain\r\n"
            f"Content-Length: {len(body)}\r\n\r\n")
    return head.encode() + body


def request_bytes(method, path, headers, body=b""):
    lines = [f"{method} {path} HTTP/1.1"] + [f"{k}: {v}" for k, v in headers]
    return len(("\r\n".join(lines) + "\r\n\r\n").encode()) + len(body)
