SUFFIXES = {
        "verb": ["i", "as", "is", "os", "us", "u"],
        "adjective": ["a", "aj", "an", "ajn"],
        "noun": ["o", "oj", "on", "ojn"],
        "adverb": ["e"]
    }


def calculate_score(w: str) -> str:
    for part in SUFFIXES:
        if any(w.endswith(suf) for suf in SUFFIXES[part]):
            return part
    return "other"


if __name__ == "__main__":
    output_dict = {
        "noun": "rzeczownik",
        "adverb": "przysłówek",
        "adjective": "przymiotnik",
        "verb": "czasownik",
        "other": "inna",
    }

    text = input()
    prediction = calculate_score(text)
    print(output_dict[prediction])
