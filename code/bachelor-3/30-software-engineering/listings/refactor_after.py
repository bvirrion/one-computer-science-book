"""The same report after three refactoring steps, each run against the same tests:
extract fine(), extract line(), then introduce the parameter object FinePolicy."""

from dataclasses import dataclass


@dataclass(frozen=True)
class FinePolicy:
    rate: int = 20  # cents a day
    cap: int | None = None  # at most this many cents, if set
    grace: int = 0  # days before a fine starts
    currency: str = "EUR"

    def fine(self, late):
        fine = late * self.rate
        return fine if self.cap is None else min(fine, self.cap)


def line(reader, title, late, cents, currency):
    return f"{reader:6} {title:24} {late:3} days {cents / 100:6.2f} {currency}"


def fines_report(loans, today, policy):
    lines, total = [], 0
    for title, reader, due in loans:
        late = (today - due).days - policy.grace
        if late > 0:
            total += policy.fine(late)
            lines.append(line(reader, title, late, policy.fine(late), policy.currency))
    lines.sort()
    lines.append(f"{'total':40} {total / 100:6.2f} {policy.currency}")
    return "\n".join(lines)
