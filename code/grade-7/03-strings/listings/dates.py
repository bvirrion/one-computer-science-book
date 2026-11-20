def two(n):
    """n as two digits: 7 gives "07", 12 gives "12"."""
    return ("0" + str(n))[-2:]


def date_string(day, month, year):
    return two(day) + two(month) + str(year)


def is_palindrome(s):
    return s == s[::-1]


def days_in_month(month, year):
    days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    if month == 2 and year % 4 == 0 and (year % 100 != 0 or year % 400 == 0):
        return 29
    return days[month - 1]


if __name__ == "__main__":
    print(date_string(2, 2, 2020), is_palindrome(date_string(2, 2, 2020)))
    print(date_string(12, 2, 2021), is_palindrome(date_string(12, 2, 2021)))
