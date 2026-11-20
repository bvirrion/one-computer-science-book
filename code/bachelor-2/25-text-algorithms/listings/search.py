"""search.py: one phrase looked for in the town archive by three algorithms."""
from boyer_moore import boyer_moore
from kmp import kmp
from naive import naive
from text_gen import archive

text = archive()
print(f"archive: {len(text)} characters, {text.count(chr(10))} lines")
for pattern in ["returned Seven Forest", "On 2025-12-1"]:
    print(f"looking for {pattern!r}, {len(pattern)} letters")
    for name, matcher in [("naive", naive), ("Boyer-Moore", boyer_moore), ("KMP", kmp)]:
        found, comparisons = matcher(text, pattern)
        print(f"   {name:12} {len(found):3} occurrences, first at {found[0]:5},"
              f" {comparisons:6} comparisons ({comparisons / len(text):.2f} a letter)")
