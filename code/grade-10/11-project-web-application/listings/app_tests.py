"""Milestone 4: start the real server in its own process and request every route."""
import socket
import subprocess
import sys
import time
import unittest
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import urlopen

PORT = 42116
BASE = f"http://127.0.0.1:{PORT}"


def get(path, form=None):
    """Return (status, text); a form is sent with POST, and redirects are followed."""
    data = urlencode(form).encode() if form is not None else None
    try:
        with urlopen(BASE + path, data=data, timeout=5) as response:
            return response.status, response.read().decode("utf-8")
    except HTTPError as error:  # 4xx and 5xx arrive as exceptions
        return error.code, error.read().decode("utf-8")


class AppTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        command = [sys.executable, "server.py", "app_m3", str(PORT)]
        cls.server = subprocess.Popen(command, stdout=subprocess.DEVNULL)
        for _ in range(100):  # wait until the server accepts connections
            try:
                socket.create_connection(("127.0.0.1", PORT), timeout=1).close()
                return
            except OSError:
                time.sleep(0.05)

    @classmethod
    def tearDownClass(cls):
        cls.server.terminate()
        cls.server.wait()

    def test_home_lists_every_book(self):
        status, text = get("/")
        self.assertEqual(status, 200)
        self.assertEqual(text.count("<li>"), 80)

    def test_book_page(self):
        status, text = get("/book/7")
        self.assertEqual(status, 200)
        self.assertIn("<h1>The Silent Kingdom</h1>", text)

    def test_missing_pages(self):
        for path in ["/book/999", "/book/x", "/book", "/shop"]:
            self.assertEqual(get(path)[0], 404, path)

    def test_style(self):
        self.assertIn("font-family", get("/style.css")[1])

    def test_search_escapes(self):
        status, text = get("/search?q=%3Cscript%3E")
        self.assertIn("&lt;script&gt;", text)
        self.assertNotIn("<script>", text)

    def test_reserve_then_redirect(self):
        status, text = get("/reserve", {"book": "9", "member": "3"})
        self.assertEqual(status, 200)  # urlopen followed the 303 to /book/9
        self.assertIn("Reserved by: 3", text)

    def test_reserve_refused(self):
        self.assertEqual(get("/reserve", {"book": "9", "member": "0"})[0], 400)
        self.assertEqual(get("/reserve", {"book": "81", "member": "3"})[0], 400)


if __name__ == "__main__":
    unittest.main()
