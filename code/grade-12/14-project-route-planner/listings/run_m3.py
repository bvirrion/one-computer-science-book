from planner import RoutePlanner

planner = RoutePlanner()
for start, end in [("Station", "Library"), ("Allotments", "Sports Hall")]:
    print(f"{start} to {end}:")
    for criterion in ["time", "distance"]:
        path, _ = planner.route(start, end, criterion)
        seconds = planner.cost_of(path, "time")
        metres = planner.cost_of(path, "distance")
        print(f"  by {criterion:8}: {seconds:>3} s {metres:>5} m  " + " > ".join(path))
there = planner.route("Town Square", "Library")[1]
back = planner.route("Library", "Town Square")[1]
print(f"Town Square to Library {there} s, back {back} s (road 1 is one-way)")
