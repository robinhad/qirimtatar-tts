import re

mappings = [
    ["\u0069\u0307", "i"],  # ["i̇", "i"], handle i with dot, first occurence is two separate symbols
]

def preprocess(text):
    text = text.lower()  # always treat lowercase
    text = " " + text + " "

    for mapping in mappings:
        text = re.sub(mapping[0], mapping[1], text)

    return text[1:-1]
    