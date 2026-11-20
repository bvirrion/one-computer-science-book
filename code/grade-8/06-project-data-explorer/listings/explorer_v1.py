MENU = """1. loans by genre
2. the ten most borrowed books
3. books never borrowed
4. loans still out on a date
0. quit"""


def main():
    print(MENU)
    choice = ""
    while choice != "0":
        choice = input("choice: ").strip()
        if choice in ["1", "2", "3", "4"]:
            print("question", choice, "is not ready yet")
        elif choice != "0":
            print("please type a number from 0 to 4")
    print("goodbye")


if __name__ == "__main__":
    main()
