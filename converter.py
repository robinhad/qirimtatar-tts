def to_cyrillic(text):
    pass


def to_latin(text):
    text = text.lower()
    cyrillic_mapping = {
        "а": "a",
        "б": "b",
        "в": "v",
        "г": "g",
        "гъ": "ğ",
        "д": "d",
        "е": "e",
        "ё": "ö",
        "ж": "",
        "з": "z",
        "и": "i",
        "й": "y",
        "к": "k",
        "къ": "q",
        "л": "l",
        "м": "m",
        "н": "n",
        "нъ": "ñ",
        "о": "o",
        "п": "p",
        "р": "r",
        "с": "s",
        "т": "t",
        "у": "u",
        "ф": "f",
        "х": "h",
        "ц": "",
        "ч": "ç",
        "дж": "c",
        "ш": "ş",
        "щ": "",
        "ъ": "",
        "ы": "ı",
        "ь": "",
        "э": "e",
        "ю": "ü",
        "я": "ya",
        "ку": "kü",  #  non-letter replacements starts here
        "узю": "üzü",
        "ур": "ür",
        "ля": "lâ",
        "уту": "utu",
        "ие": "iye",
        "ко": "kö",
        "мю": "mü",
        "ол": "öl",
        "къу": "qu",
        "cю": "sü",
        "ёкъ": "yoq",
        "юв": "yuv",
        "уз": "üz",
    }

    for key in sorted(cyrillic_mapping.keys(), key=lambda x: len(x), reverse=True):
        text = text.replace(key, cyrillic_mapping[key])
    return text
