"""Exercise 9: the two intermediate states of the refactoring, between
refactor_before.py and refactor_after.py; the same tests pass on all four."""


def fine(late, rate, cap):  # step 1: extract the fine computation
    fine = late * rate
    return fine if cap is None else min(fine, cap)


def report_step1(loans, today, rate, cap, grace, currency):
    lines, total = [], 0
    for title, reader, due in loans:
        late = (today - due).days - grace
        if late > 0:
            total += fine(late, rate, cap)
            lines.append(
                f"{reader:6} {title:24} {late:3} days "
                f"{fine(late, rate, cap) / 100:6.2f} {currency}"
            )
    lines.sort()
    lines.append(f"{'total':40} {total / 100:6.2f} {currency}")
    return "\n".join(lines)


def line(
    reader, title, late, cents, currency
):  # step 2: extract one line of the report
    return f"{reader:6} {title:24} {late:3} days {cents / 100:6.2f} {currency}"


def report_step2(loans, today, rate, cap, grace, currency):
    lines, total = [], 0
    for title, reader, due in loans:
        late = (today - due).days - grace
        if late > 0:
            total += fine(late, rate, cap)
            lines.append(line(reader, title, late, fine(late, rate, cap), currency))
    lines.sort()
    lines.append(f"{'total':40} {total / 100:6.2f} {currency}")
    return "\n".join(lines)
