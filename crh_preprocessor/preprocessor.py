import re

mapping = {
    "n\u0303": "\xf1",
    "g\u0306": "\u011f",
    "i\u0307": "i",
    "u\u0308": "\xfc",
    "o\u0308": "\xf6",
    "\xe7": "\u04ab",
    "c\u0327": "\u04ab",
    "s\u0327": "\u015f",
    "a\u0302": "\xe2",
    "w": "v",
    "x": "ks"
}
 

def preprocess(text):
    text = text.lower()  # always treat lowercase
    text = " " + text + " "

    for symbol in mapping.keys():
        text = re.sub(symbol, mapping[symbol], text)

    separators = "?!" # TODO: add proper symbols to tts
    for symbol in separators:
        text = text.replace(symbol, ".")

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
    