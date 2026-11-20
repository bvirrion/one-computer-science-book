import csv

with open("loans.csv", encoding="utf-8") as f:
    loans = list(csv.DictReader(f))

out = []
for loan in loans:
    if loan["return_date"] == "":
        out.append(loan)
print(len(loans), "loans,", len(out), "still out")
for loan in out[:3]:
    print("book", loan["book_id"], "lent on", loan["out_date"], "due", loan["due_date"])
