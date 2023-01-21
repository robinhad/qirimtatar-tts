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
    "x": "ks",
}

zero = {
    0: "sıfır",
}

numbers_map = {
    1: "bir",
    2: "eki",
    3: "üç",
    4: "dört",
    5: "beş",
    6: "altı",
    7: "yedi",
    8: "sekiz",
    9: "doquz",
    10: "on",
    20: "yigirmi",
    30: "otuz",
    40: "qırq",
    50: "elli",
    60: "altmış",
    70: "yetmiş",
    80: "seksen",
    90: "doqsan",
    100: "yüz",
    1000: "biñ",
    1_000_000: "million",
    1_000_000_000: "milliard",
}


def spell_numbers(numbers: str) -> str:
    numbers_map_with_zero = {**numbers_map, **zero}
    for i in range(0, 10):
        numbers = numbers.replace(str(i), numbers_map_with_zero[i] + " ")
    return numbers.strip()


def num2word(n):
    if n in numbers_map:
        return numbers_map[n]
    elif n < 100:
        tens = (n // 10) * 10
        units = n % 10
        if units == 0:
            return ""
        return (numbers_map[tens] + " " + numbers_map[units]).strip()
    elif n < 1000:
        hundreds = n // 100
        rest = n % 100
        return (
            num2word(hundreds) + " " + numbers_map[100] + " " + num2word(rest)
        ).strip()
    elif n < 1_000_000:
        thousands = n // 1_000
        rest = n % 1_000
        return (
            num2word(thousands) + " " + numbers_map[1_000] + " " + num2word(rest)
        ).strip()
    elif n < 1_000_000_000:
        millions = n // 1_000_000
        rest = n % 1_000_000
        return (
            num2word(millions) + " " + numbers_map[1_000_000] + " " + num2word(rest)
        ).strip()
    elif n < 1_000_000_000_000:
        billions = n // 1_000_000_000
        rest = n % 1_000_000_000
        return (
            num2word(billions) + " " + numbers_map[1_000_000_000] + " " + num2word(rest)
        ).strip()
    else:
        return spell_numbers(str(n))


def preprocess(text):
    text = text.lower()  # always treat lowercase
    text = " " + text + " "

    for symbol in mapping.keys():
        text = re.sub(symbol, mapping[symbol], text)

    separators = "?!"  # TODO: add proper symbols to tts
    for symbol in separators:
        text = text.replace(symbol, ".")

    while True:
        groups_match = re.search("((\d,)+){2,}", text)
        if groups_match is not None:
            text = text.replace(
                groups_match.string[groups_match.start() : groups_match.end()],
                " ".join(
                    groups_match.string[
                        groups_match.start() : groups_match.end()
                    ].split(",")
                ),
            )
            continue

        number_match = re.search("(\-|\+)?(\d)+((\.|,)?\d+)?", text)
        if number_match is None:
            break

        number = number_match.string[number_match.start() : number_match.end()]
        number_to_replace = number
        prefix = ""

        if number.startswith("-"):
            prefix = "minus "
            number = number.replace("-", "", 1)
        elif number.startswith("+"):
            prefix = "plüs "
            number = number.replace("+", "", 1)

        if "." in number:
            number = number.split(".")
            number = prefix + " noqta ".join(
                (
                    num2word(int(number[0]))
                    if int(number[0]) != 0
                    else spell_numbers(number[0]),
                    spell_numbers(number[1]),
                )
            )
            text = text.replace(number_to_replace, number, 1)
            continue
        elif "," in number:
            number = number.split(",")
            number = prefix + " virgül ".join(
                (
                    num2word(int(number[0]))
                    if int(number[0]) != 0
                    else spell_numbers(number[0]),
                    spell_numbers(number[1]),
                )
            )
            text = text.replace(number_to_replace, number, 1)
            continue

        if number.startswith("0"):
            text = text.replace(number_to_replace, prefix + spell_numbers(number), 1)
            continue

        text = text.replace(number_to_replace, prefix + num2word(int(number)), 1)

    return text.strip()
