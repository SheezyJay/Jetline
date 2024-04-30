def validate(fruits):
    if 'apple' in fruits:
        fruits.remove('apple')
    return fruits


def export(fruits):
    with open('output/fruits.txt', 'w') as file:
        for fruit in fruits:
            file.write(fruit + '\n')
