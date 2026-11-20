from urllib.parse import quote, unquote, urlencode

print(quote("café & co"))
print(urlencode({"title": "café & co", "page": 2}))
print(unquote("caf%C3%A9%20%26%20co"))
