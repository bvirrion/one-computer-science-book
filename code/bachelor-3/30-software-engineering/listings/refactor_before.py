"""The fines report as the desk has printed it for years: one long function."""


def fines_report(loans, today, rate, cap, grace, currency):
    lines = []
    total = 0
    for title, reader, due in loans:
        late = (today - due).days - grace
        if late > 0:
            fine = late * rate
            if cap is not None and fine > cap:
                fine = cap
            total += fine
            lines.append(
                f"{reader:6} {title:24} {late:3} days {fine / 100:6.2f} {currency}"
            )
    lines.sort()
    lines.append(f"{'total':40} {total / 100:6.2f} {currency}")
    return "\n".join(lines)
