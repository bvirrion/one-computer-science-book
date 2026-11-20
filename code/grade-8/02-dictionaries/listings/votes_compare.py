from ballots import BALLOTS, CANDIDATES, many_ballots
from votes_dict import count_once
from votes_list import count_per_candidate


def compare(ballots, candidates):
    results, by_list = count_per_candidate(ballots, candidates)
    counts, by_dict = count_once(ballots)
    print(len(ballots), "ballots,", len(candidates), "candidates:", by_list,
          "names looked at with lists,", by_dict, "with a dictionary")


names = []
for i in range(20):
    names.append("C" + str(i + 1))
compare(BALLOTS, CANDIDATES)
compare(many_ballots(400, names), names)
