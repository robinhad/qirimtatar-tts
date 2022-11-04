import re

mappings = [
    ["\u0069\u0307", "i"],  # ["i̇", "i"], handle i with dot, first occurence is two separate symbols
]

def preprocess(text):
    text = text.lower()  # always treat lowercase
    text = " " + text + " "

    for mapping in mappings:
        text = re.sub(mapping[0], mapping[1], text)

    numbers = {
        "0": "sıfır",
        "1": "bir",
        "2": "eki",
        "3": "üç",
        "4": "dört",
        "5": "beş",
        "6": "altı",
        "7": "yedi",
        "8": "sekiz",
        "9": "doquz",
    }

    for number in numbers.keys():
        text = text.replace(number, numbers[number] + " ")

    return text[1:-1]
    