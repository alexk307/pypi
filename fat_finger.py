from random import randint


KEYBOARD = [
    ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p'],
    ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l'],
    ['z', 'x', 'c', 'v', 'b', 'n', 'm']
]


def generate_fat_finger(token):
    letter = token[randint(0, len(token)-1)]
    for row in KEYBOARD:
        if letter in row:
            try:
                # TODO randomize movement better
                return token.replace(letter, row[row.index(letter)+1], 1)
            except IndexError:
                return token.replace(letter, row[row.index(letter) - 1], 1)


if __name__ == '__main__':
    print generate_fat_finger('alex')
