# capture: scratch
import csv

with open("loans.csv", encoding="utf-8") as f:
    loans = list(csv.DictReader(f))

returned = 0
for loan in loans:
    if loan["return_date"] != "":
        returned = returned + 1

with open("report.txt", "w", encoding="utf-8") as f:
    f.write("Brenmoor library, loans of 2025\n")
    f.write("loans: " + str(len(loans)) + "\n")
    f.write("returned: " + str(returned) + "\n")
    f.write("still out: " + str(len(loans) - returned) + "\n")

with open("report.txt", encoding="utf-8") as f:
    print(f.read(), end="")
