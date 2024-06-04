#!/usr/bin/env python3
""" Password Generator """
import argparse
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
    length: int = 8
    numbers: bool
    symbols: bool

    parser = argparse.ArgumentParser(
            description='Tool that generates a strong random password')

    parser.add_argument('-l', '--length', type=int, help='Password length not < 8')
    parser.add_argument('-n', '--numbers', action='store_true', help='include numbers')
    parser.add_argument('-s', '--symbols', action='store_true', help='include symbols')

    args = parser.parse_args()

    if args.length:
        if args.length < 8:
            print("Length must be greater than 8")
            exit()
        length = args.length
    numbers = args.numbers
    symbols = args.symbols

    print()
    print(generate_password(length, numbers, symbols))
