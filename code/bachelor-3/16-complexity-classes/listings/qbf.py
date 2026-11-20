"""qbf.py -- a true quantified Boolean formula is a game. The first player (exists)
wins the game "take 1 or 2 tokens; who takes the last one wins" from m tokens if:
there is a first move such that for every reply there is a move ... that wins."""
calls = 0


def value(quantifiers, phi, bits=()):
    """Evaluate Q1 x1 Q2 x2 ... phi(x): depth n, one branch stored at a time."""
    global calls
    calls += 1
    if len(bits) == len(quantifiers):
        return phi(bits)
    branches = (value(quantifiers, phi, bits + (b,)) for b in (False, True))
    return any(branches) if quantifiers[len(bits)] == "E" else all(branches)


def first_player_wins(m):
    """phi(x): x_i = True means move i takes 2 tokens. True if the first player takes
    the last token within m moves."""
    def phi(bits):
        tokens = m
        for i, two in enumerate(bits):
            tokens -= min(2 if two else 1, tokens)
            if tokens == 0:
                return i % 2 == 0  # moves 0, 2, 4, ... are the first player's
        return False
    return phi


if __name__ == "__main__":
    for m in range(1, 13):
        calls = 0
        quantifiers = "EA" * (m // 2) + "E" * (m % 2)  # exists, for all, exists, ...
        wins = value(quantifiers, first_player_wins(m))
        winner = "first" if wins else "second"
        print(f"{m:>2} tokens: {quantifiers:<12} {winner} player wins; "
              f"{calls:>5} calls, depth {m}")
