import random

# Pick a random number from 1 to 100
secret = random.randint(1, 100)

print("I'm thinking of a number from 1 to 100. Guess it!")

while True:
    guess = int(input("Your guess: "))

    if guess < secret:
        print("Too low. Try again.")
    elif guess > secret:
        print("Too high. Try again.")
    else:
        print("You got it!")
        break
