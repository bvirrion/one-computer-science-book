import socket
import subprocess
import sys
import time
from contextlib import contextmanager


@contextmanager
def running(port):
    """Run library_site.py on 127.0.0.1:port in its own process, then stop it."""
    server = subprocess.Popen([sys.executable, "library_site.py", str(port)],
                              stdout=subprocess.PIPE, text=True)
    for _ in range(100):  # wait until it accepts connections
        try:
            socket.create_connection(("127.0.0.1", port), timeout=1).close()
            break
        except OSError:
            time.sleep(0.05)
    try:
        yield server
    finally:
        server.terminate()
        log = server.communicate()[0]
        print(log, end="")
