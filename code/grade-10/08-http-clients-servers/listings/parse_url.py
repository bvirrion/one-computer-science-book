from urllib.parse import parse_qs, urlsplit

address = ("http://library.brenmoor.example:8080"
           "/books/search?title=forest&genre=nature#top")
url = urlsplit(address)
print("scheme:  ", url.scheme)
print("host:    ", url.hostname)
print("port:    ", url.port)
print("path:    ", url.path)
print("query:   ", url.query, "->", parse_qs(url.query))
print("fragment:", url.fragment)
print(urlsplit("https://library.brenmoor.example/").port)
