"""ex6_detect.py -- deadlock detection with several instances of each resource: which
processes can never finish, whatever order the others run in?"""


def deadlocked(available, alloc, request):
    """Processes whose current request can never be met: simulate the luckiest future,
    where any process whose request fits finishes and frees what it holds."""
    work, finished = list(available), [False] * len(alloc)
    progress = True
    while progress:
        progress = False
        for i, req in enumerate(request):
            if not finished[i] and all(r <= w for r, w in zip(req, work)):
                work = [w + a for w, a in zip(work, alloc[i])]
                finished[i] = progress = True
    return [i for i, f in enumerate(finished) if not f]
