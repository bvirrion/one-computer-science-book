"""Exercise 5: the parameters of an address's query, one value each."""


def query_params(url):
    """Return a dict name -> value of the query of url (the part after ?, before #)."""
    query = url.split("#")[0].partition("?")[2]
    params = {}
    for pair in query.split("&"):
        if pair:
            name, _, value = pair.partition("=")
            params[name] = value
    return params
