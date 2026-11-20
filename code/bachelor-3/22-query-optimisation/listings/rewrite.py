"""rewrite.py -- a relational-algebra tree for the library's late-loans report,
rewritten by pushing selections down, and both trees run on the town's tables:
the results are equal and the intermediate results shrink."""

import town

TABLES = {t: town.load(t) for t in ("loans", "books", "members", "people")}
PREDICATES = {  # name: (columns used, test)
    "late": (
        {"return_date", "due_date"},
        lambda t: t["return_date"] is None or t["return_date"] > t["due_date"],
    ),
    "mystery": ({"genre"}, lambda t: t["genre"] == "mystery"),
}


def columns(node):
    if node[0] == "table":
        return set(TABLES[node[1]][0])
    if node[0] == "join":
        return columns(node[3]) | columns(node[4])
    return columns(node[2])


def push(node):
    """Move every selection as far down as its columns allow."""
    if node[0] == "table":
        return node
    if node[0] == "join":
        return ("join", node[1], node[2], push(node[3]), push(node[4]))
    child = push(node[2])
    if node[0] == "select" and child[0] == "join":
        used = PREDICATES[node[1]][0]
        for side in (3, 4):
            if used <= columns(child[side]):
                parts = list(child)
                parts[side] = push(("select", node[1], child[side]))
                return tuple(parts)
    return (node[0], node[1], child)


def run(node, sizes):
    """Evaluate in memory, recording the size of every intermediate result."""
    if node[0] == "table":
        rows = TABLES[node[1]]
    elif node[0] == "select":
        rows = [t for t in run(node[2], sizes) if PREDICATES[node[1]][1](t)]
    elif node[0] == "project":
        rows = [{c: t[c] for c in node[1]} for t in run(node[2], sizes)]
    else:
        index = {}
        for s in run(node[4], sizes):
            index.setdefault(s[node[2]], []).append(s)
        rows = [
            {**r, **s} for r in run(node[3], sizes) for s in index.get(r[node[1]], [])
        ]
    sizes.append((node, len(rows)))
    return rows


def show(node, sizes, depth=0):
    size = next(n for nd, n in sizes if nd is node)
    label = {
        "table": lambda: node[1],
        "select": lambda: f"select {node[1]}",
        "project": lambda: "project " + ", ".join(node[1]),
        "join": lambda: f"join {node[1]} = {node[2]}",
    }[node[0]]()
    print(f"{'  ' * depth}{label}  [{size} rows]")
    for child in node[2:] if node[0] != "join" else node[3:]:
        if isinstance(child, tuple):
            show(child, sizes, depth + 1)


QUERY = (
    "project",
    ("title", "last_name", "due_date"),
    (
        "select",
        "mystery",
        (
            "select",
            "late",
            (
                "join",
                "person_id",
                "person_id",
                (
                    "join",
                    "member_id",
                    "member_id",
                    (
                        "join",
                        "book_id",
                        "book_id",
                        ("table", "loans"),
                        ("table", "books"),
                    ),
                    ("table", "members"),
                ),
                ("table", "people"),
            ),
        ),
    ),
)

if __name__ == "__main__":
    results = []
    for title, tree in (("as written", QUERY), ("selections pushed down", push(QUERY))):
        sizes = []
        rows = run(tree, sizes)
        print(
            f"{title}: {sum(n for nd, n in sizes if nd[0] != 'table')} "
            "intermediate rows in all"
        )
        show(tree, sizes)
        results.append(sorted(tuple(sorted(r.items())) for r in rows))
    print("same result:", results[0] == results[1], f"({len(results[0])} rows)")
