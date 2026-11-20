from load_weather import read_table

loans = read_table("loans.csv")
books = read_table("books.csv")
out = [loan for loan in loans if loan["return_date"] is None]

comparisons = 0
result = []
for loan in out:              # nested-loop join: every pair is compared
    for book in books:
        comparisons += 1
        if loan["book_id"] == book["book_id"]:
            result.append((loan["out_date"], book["title"]))
print(len(out), "books still out; the first two:")
print(result[:2])
print(comparisons, "comparisons")
