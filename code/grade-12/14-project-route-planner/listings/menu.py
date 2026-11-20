"""Milestone 4: a text interface to the planner."""
from planner import RoutePlanner


def minutes(seconds):
    return f"{seconds // 60} min {seconds % 60:02} s"


def main():
    planner = RoutePlanner()
    while True:
        choice = input("1 route, 2 places, 3 close a road, 4 quit: ").strip()
        if choice == "1":
            start, end = input("from: ").strip(), input("to: ").strip()
            try:
                path, seconds = planner.route(start, end)
            except ValueError as e:
                print("sorry:", e)
                continue
            roads = len(path) - 1
            print(minutes(seconds), "over", roads, "road" if roads == 1 else "roads")
            print("  " + " > ".join(path))
        elif choice == "2":
            print(", ".join(sorted(planner.ids)))
        elif choice == "3":
            planner.close_road(int(input("road number: ")))
            print("closed:", sorted(planner.closed))
        elif choice == "4":
            return
        else:
            print("please type 1, 2, 3 or 4")


main()
