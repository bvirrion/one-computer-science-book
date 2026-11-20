def is_palindrome(s):
    s = s.lower().replace(" ", "")
    return s == s[::-1]


for text in ["level", "Kayak", "Never odd or even", "Python"]:
    print(text, is_palindrome(text))
