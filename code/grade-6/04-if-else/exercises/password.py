password = input("New password: ")
if len(password) >= 12:
    print("Long enough.")
else:
    print("Too short:", 12 - len(password), "more characters needed.")
