"""robot_problem.py: a delivery robot on the town map, then a rival that tries to
catch it, then alpha-beta on noughts and crosses."""
from games import attractor
from state_space import astar
from tictactoe import moves, score, to_move
from town_map import PLACES, ROADS, straight

# Part I-II: start at the Bus Depot, deliver to the Library, the Museum and the
# Hospital in any order. A state is (place, deliveries still to make).
DEPOT, STOPS = 16, frozenset({3, 12, 8})


def successors(state):
    place, todo = state
    for nxt, d in ROADS.get(place, []):
        yield (nxt, todo - {nxt}), d


def h(state):  # the farthest stop left, in a straight line: admissible
    place, todo = state
    return max((straight(place, s) for s in todo), default=0)


start = (DEPOT, STOPS)
for name, heur in [("uniform cost", lambda s: 0), ("A*, farthest stop", h)]:
    path, cost, expanded = astar(start, lambda s: not s[1], successors, heur)
    print(f"{name:17}: {cost} m, {expanded} states expanded;",
          "route", "-".join(str(p) for p, _ in path))

# Part III: the robot (player 0) must reach the Library; the rival (player 1) wins by
# being on the robot's place. They move in turn along the roads, robot first.
GOAL = 3
nbr = {p: set() for p in PLACES}  # on foot, every road goes both ways
for u in ROADS:
    for v, _ in ROADS[u]:
        nbr[u].add(v)
        nbr[v].add(u)
owner, succ, caught, home = {}, {}, [], []
for r in PLACES:
    for v in PLACES:
        for turn in (0, 1):
            pos = (r, v, turn)
            owner[pos] = turn
            if r == v:
                succ[pos] = [pos]
                caught.append(pos)
            elif r == GOAL:
                succ[pos] = [pos]
                home.append(pos)
            elif turn == 0:
                succ[pos] = [(q, v, 1) for q in nbr[r]]
            else:
                succ[pos] = [(r, q, 0) for q in nbr[v]]
robot, plan = attractor(owner, succ, home, 0)
rival, _ = attractor(owner, succ, caught, 1)
print(f"{len(owner)} positions: robot wins from {len(robot)}, rival from {len(rival)},"
      f" neither from {len(owner) - len(robot) - len(rival)}")
for r, v in [(16, 2), (16, 1), (27, 9)]:
    pos = (r, v, 0)
    who = "robot" if pos in robot else "rival" if pos in rival else "neither"
    line = f"robot at {PLACES[r]}, rival at {PLACES[v]}: {who} wins"
    if who == "robot":
        line += f", first move to {PLACES[plan[pos][0]]}, {robot[pos]} moves in all"
    elif who == "rival":
        line += f" after {rival[pos]} moves in all"
    print(line)


# Part IV: alpha-beta on noughts and crosses from the empty board.
def alphabeta(b, alpha, beta, count):
    ms = moves(b)
    if not ms:
        count[0] += 1
        return score(b)
    if to_move(b) == "x":
        for m in ms:
            alpha = max(alpha, alphabeta(m, alpha, beta, count))
            if alpha >= beta:
                break
        return alpha
    for m in ms:
        beta = min(beta, alphabeta(m, alpha, beta, count))
        if alpha >= beta:
            break
    return beta


count = [0]
print("noughts and crosses: alpha-beta value", alphabeta("." * 9, -2, 2, count),
      f"after {count[0]} finished games of 255168")
