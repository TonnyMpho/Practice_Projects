#!/usr/bin/env python3
""" Password Generator """
import string
import random


def generate_password(length: int=8, numbers: bool=True, symbols: bool=True) -> str:
    """
    function that generates strong and random passwords
    based on requirements
    """
    letters: str = string.ascii_letters
    digits: str = string.digits
    punctuations: str = string.punctuation

    if numbers:
        letters += digits
    if symbols:
        letters += punctuations

    password: str = ""
    valid_password: bool = False
    while not valid_password:
        password = ""
        for _ in range(length):
            password += random.choice(letters)

        valid_password = True
        if symbols:
            if not any(c in punctuations for c in password):
                valid_password = False
        if numbers:
            if not any(c in digits for c in password):
                valid_password = False

    return password


if __name__ == "__main__":

    length: int = int(input("Please specify the length of your password not less than 8  "))
    if length < 8:
        length = int(input("Please enter a number > 8  "))

    numbers: str = input("Should your password contain numbers? Yes/No  ")
    symbols: str = input("Should your password contain special characters? Yes/No  ")

    print()
    if numbers.upper() == "YES" and symbols.upper() == "YES":
        print(generate_password(length, True, True))
    elif numbers.upper() == "YES":
        print(generate_password(length, True, False))
    elif symbols.upper() == "YES":
        print(generate_password(length, False, True))
    else:
        print(generate_password(length,False, False))
