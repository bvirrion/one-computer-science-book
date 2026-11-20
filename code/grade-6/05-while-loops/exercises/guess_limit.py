secret = int(input("Player 1, the secret number (1 to 100): "))
print("\n" * 3)
guesses = 1
guess = int(input("Player 2, your guess: "))
while guess != secret and guesses < 7:
    if guess < secret:
        print("Higher!")
    else:
        print("Lower!")
    guesses = guesses + 1
    guess = int(input("Your guess: "))
if guess == secret:
    print(f"Found in {guesses} guesses!")
else:
    print("Seven guesses: player 1 wins. The number was", secret)
