vowels = {
    "a": "a",
    "ą": "ɔ",
    "e": "ɛ",
    "ę": "ɛ",
    "i": "i",
    "o": "ɔ",
    "u": "u",
    "ó": "u",
    "y": "ɨ",
}

sonors = {
    "j": "j",
    "m": "m",
    "n": "n",
    "ń": "ɲ",
    "ni": "ɲ",
    "r": "r",
    "l": "l",
    "ł": "w",
}

voice_voice = {
    "b": "b",
    "d": "d",
    "g": "ɡ",
    "w": "v",
    "z": "z",
    "dź": "d͡ʑ",
    "dzi": "d͡ʑ",
    "ź": "ʑ",
    "zi": "ʑ",
    "dz": "d͡z",
    "dż": "d͡ʐ",
    "ż": "ʐ",
    "rz": "ʐ",
    "h": "ɣ",
    "ch": "ɣ",
    "v": "v",
    "q": "kv",
    "x": "ks",
}

voice_voiceless = {
    "b": "p",
    "d": "t",
    "g": "k",
    "w": "f",
    "z": "s",
    "dź": "t͡ɕ",
    "dzi": "t͡ɕ",
    "ź": "ɕ",
    "zi": "ɕ",
    "dz": "t͡s",
    "dż": "d͡ʐ",
    "ż": "ʂ",
    "rz": "ʂ",
    "h": "x",
    "ch": "x",
    "v": "f",
    "q": "kf",
    "x": "ks",
}

voiceless_voiceless = {
    "p": "p",
    "t": "t",
    "k": "k",
    "f": "f",
    "s": "s",
    "ć": "t͡ɕ",
    "ci": "t͡ɕ",
    "ś": "ɕ",
    "si": "ɕ",
    "c": "t͡s",
    "cz": "t͡ʂ",
    "sz": "ʂ",
}

voiceless_voice = {
    "p": "b",
    "t": "d",
    "k": "ɡ",
    "f": "v",
    "s": "z",
    "ć": "d͡ʑ",
    "ci": "d͡ʑ",
    "ś": "ʑ",
    "si": "ʑ",
    "c": "d͡z",
    "cz": "d͡ʐ",
    "sz": "ʐ",
}

w_nasals = (
    "w",
    "z",
    "ź",
    "zi",
    "rz",
    "ż",
    "ś",
    "si",
    "ch",
    "h",
    "f",
    "s",
    "sz",
)
n_nasals = ("d", "g", "dz", "c", "k", "t", "cz", "dż")
m_nasals = ("b", "p")
ni_nasals = ("dź", "dzi", "ci", "ć")
consonants_soft = ("dzi", "zi", "ci", "si", "ni")


def transcript(w: str) -> str:
    w = w.lower().strip()

    digraphs = {
        "dzi": "A",
        "dź": "B",
        "rz": "C",
        "dż": "D",
        "ch": "E",
        "sz": "F",
        "cz": "G",
        "dz": "H",
        "zi": "I",
        "ci": "J",
        "si": "K",
        "ni": "L",
    }
    for key, val in digraphs.items():
        w = w.replace(key, val)

    redigraphs = {value: key for (key, value) in digraphs.items()}
    w = [redigraphs[char] if char in redigraphs else char for char in w]

    result = w.copy()

    posit_vowel = [-1] + [i for i in range(len(w)) if w[i] in vowels]
    posit_sonor = [i for i in range(len(w)) if w[i] in sonors]

    j = posit_vowel[-1]
    if posit_sonor and posit_sonor[-1] > posit_vowel[-1]:
        j = posit_sonor[-1]

    i = len(w) - 1
    while i > j:
        if w[i] in voice_voiceless:
            result[i] = voice_voiceless[w[i]]
        elif w[i] in voiceless_voiceless:
            result[i] = voiceless_voiceless[w[i]]
        elif w[i] in sonors:
            result[i] = sonors[w[i]]
        i -= 1

    while posit_vowel:
        i, k = j, j
        j = posit_vowel.pop()
        voice = None
        while i > j:
            if w[i] in consonants_soft:
                if w[i] in ("dzi", "zi"):
                    voice = True
                    if i < len(w) - 1 and w[i + 1] in vowels:
                        result[i] = voice_voice[w[i]]
                    else:
                        result[i] = voice_voice[w[i]] + " i"
                elif i < len(w) - 1 and w[i] in ("ci", "si"):
                    voice = False
                    if w[i + 1] in vowels:
                        result[i] = voiceless_voiceless[w[i]]
                    else:
                        result[i] = voiceless_voiceless[w[i]] + " i"
                else:
                    voice = None
                    if i < len(w) - 1 and w[i + 1] in vowels:
                        result[i] = sonors[w[i]]
                    else:
                        result[i] = sonors[w[i]] + " i"
            elif w[i] in vowels:
                if i == 0 or w[i - 1] == " ":
                    result[i] = "ʔ " + vowels[w[i]]
                elif w[i] == "i" and i < len(w) - 1 and w[i + 1] == "i":
                    result[i] = "j"
                elif w[i] in "ąę":
                    if i is len(w) - 1:
                        if w[i] == "ą":
                            result[i] = vowels[w[i]] + " u̯"
                        else:
                            result[i] = vowels[w[i]]
                    elif w[i + 1] in n_nasals:
                        result[i] = vowels[w[i]] + " ŋ"
                    elif w[i + 1] in m_nasals:
                        result[i] = vowels[w[i]] + " m"
                    elif w[i + 1] in w_nasals:
                        result[i] = vowels[w[i]] + " u̯"
                    elif w[i + 1] in ni_nasals:
                        result[i] = vowels[w[i]] + " ɲ"
                    else:
                        result[i] = vowels[w[i]]
                else:
                    result[i] = vowels[w[i]]

            elif k != i:
                if w[i] in sonors:
                    voice = None
                    result[i] = sonors[w[i]]
                elif voice is None:
                    if w[i] in "w" and i > 0:
                        if w[i - 1] in "tks":
                            result[i] = voice_voiceless[w[i]]
                            voice = False
                        else:
                            result[i] = voice_voice[w[i]]
                            voice = True
                    elif w[i] in ("ż", "rz") and i > 0:
                        if w[i - 1] in "ae" or w[i - 1] in voiceless_voiceless:
                            result[i] = voice_voiceless[w[i]]
                            voice = False
                        else:
                            result[i] = voice_voice[w[i]]
                            voice = True
                    elif w[i] in voice_voice:
                        voice = True
                        result[i] = voice_voice[w[i]]
                    elif w[i] in voiceless_voiceless:
                        result[i] = voiceless_voiceless[w[i]]
                        voice = False
                else:
                    if voice is True and w[i] in voice_voice:
                        result[i] = voice_voice[w[i]]
                    elif voice is True and w[i] in voiceless_voice:
                        result[i] = voiceless_voice[w[i]]
                    elif voice is False and w[i] in voice_voiceless:
                        result[i] = voice_voiceless[w[i]]
                    elif voice is False and w[i] in voiceless_voiceless:
                        result[i] = voiceless_voiceless[w[i]]

            i -= 1

    result = list(filter(None, result))
    result = "".join(result).replace(" ", "")
    return result


if __name__ == "__main__":
    text = input()
    transcription = transcript(text)
    print(transcription)
