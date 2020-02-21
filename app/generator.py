from string import ascii_letters, digits
from random import sample


def generate_code(prefix):
    random = ''.join(sample(ascii_letters + digits, 12)) + chr(29)
    return f'{prefix}{random}'


def get_codes(count, prefix):
    codes = set()
    while len(codes) < count:
        codes.add(generate_code(prefix))

    return codes
