import json

from load_weather import read_table

loans = read_table("loans.csv")
member = {"member_id": 8, "loans": []}
for loan in loans:
    if loan["member_id"] == 8 and loan["out_date"] < "2025-04-01":
        member["loans"].append({"book": loan["book_id"], "out": loan["out_date"],
                                "back": loan["return_date"]})
text = json.dumps(member, indent=2)
print(text)
print(json.loads(text) == member)
