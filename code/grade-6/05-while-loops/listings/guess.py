secret = int(input("Player 1, the secret number (1 to 100): "))
print("\n" * 3)          # push the secret up, out of sight
guesses = 1
guess = int(input("Player 2, your guess: "))
while guess != secret:
    if guess < secret:
        print("Higher!")
    else:
        print("Lower!")
    guesses = guesses + 1
    guess = int(input("Your guess: "))
print(f"Found in {guesses} guesses!")
