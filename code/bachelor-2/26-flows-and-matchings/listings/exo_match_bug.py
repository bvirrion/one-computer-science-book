"""exo_match_bug.py: a matching search that marks slots once for all readers."""
from matching import max_matching

ADJ = {"Ada": ["Mon", "Tue"], "Ben": ["Mon"], "Cy": ["Tue", "Wed", "Thu"],
       "Dee": ["Wed", "Fri"], "Eve": ["Mon", "Wed"]}


def try_match(u, match, seen):
    for v in ADJ[u]:
        if v in seen:
            continue
        seen.add(v)
        if v not in match or try_match(match[v], match, seen):
            match[v] = u
            return True
    return False


match, seen = {}, set()
for u in ADJ:
    try_match(u, match, seen)
print("one set of marks:", len(match), sorted((u, v) for v, u in match.items()))
print("fresh marks     :", len(max_matching(ADJ)))
