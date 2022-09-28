import converter


def test_cyrillic_converter():
    cases = _read_test_cases()
    for case in cases:
        assert converter.to_cyrillic(case[0]) == case[1]


def test_latin_converter():
    cases = _read_test_cases()
    print(cases)
    for case in cases:
        assert converter.to_latin(case[1]).lower() == case[0].lower()


def test_letter_coverage():
    """
    Check if all letters are present in a test set.
    """
    latin_alphabet = [
        "a",
        "â",
        "b",
        "c",
        "ç",
        "d",
        "e",
        "f",
        "g",
        "ğ",
        "h",
        "ı",
        "i",
        "j",
        "k",
        "l",
        "m",
        "n",
        "ñ",
        "o",
        "ö",
        "p",
        "q",
        "r",
        "s",
        "ş",
        "t",
        "u",
        "ü",
        "v",
        "y",
        "z",
    ]
    cyrillic_alphabet = [
        "а",
        "б",
        "в",
        "г",
        "гъ",
        "д",
        "е",
        "ё",
        "ж",
        "з",
        "и",
        "й",
        "к",
        "къ",
        "л",
        "м",
        "н",
        "нъ",
        "о",
        "п",
        "р",
        "с",
        "т",
        "у",
        "ф",
        "х",
        "ц",
        "ч",
        "дж",
        "ш",
        "щ",
        "ъ",
        "ы",
        "ь",
        "э",
        "ю",
        "я",
    ]
    cases = _read_test_cases()
    missing_letters = []
    latin_cases = " ".join([case[0] for case in cases]).lower()
    for letter in sorted(latin_alphabet, key=lambda x: len(x), reverse=True):
        if letter not in latin_cases:
            missing_letters.append(letter)
        latin_cases = latin_cases.replace(letter, "")
    cyrillic_cases = " ".join([case[1] for case in cases]).lower()
    for letter in sorted(cyrillic_alphabet, key=lambda x: len(x), reverse=True):
        if letter not in cyrillic_cases:
            missing_letters.append(letter)
        cyrillic_cases = cyrillic_cases.replace(letter, "")
    if len(missing_letters) > 0:
        raise Exception(f"'{missing_letters}' not found in test dataset!")


def _read_test_cases():
    with open("tests/rosetta.csv") as file:
        text = file.read()

    rows = text.split("\n")
    for i in range(0, len(rows)):
        rows[i] = rows[i].split("|")
    return rows
