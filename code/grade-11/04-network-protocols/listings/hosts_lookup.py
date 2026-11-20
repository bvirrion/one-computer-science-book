"""Names to addresses from a local table, in the format of a hosts file."""
HOSTS = """\
# address       names
192.0.2.10      library.example  library
192.0.2.11      mail.example
198.51.100.7    town.example
"""


def parse(text):
    table = {}
    for line in text.splitlines():
        line = line.split("#")[0].strip()      # a # starts a comment
        if line:
            address, *names = line.split()
            for name in names:
                table[name] = address
    return table


table = parse(HOSTS)
for name in ["library", "town.example", "school.example"]:
    print(name, "->", table.get(name, "unknown here: ask the name system"))
