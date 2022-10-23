from .cyr_to_lat import mappings
import re


def transliterate(text: str):
    text = text.lower()  # always treat lowercase
    text = " " + text + " "

    for mapping in mappings:
        text = re.sub(mapping[0], mapping[1], text)

    return text[1:-1]
