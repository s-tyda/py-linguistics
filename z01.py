import sys
import unicodedata


class LanguageDetector:
    dictionaries: dict[str, list[str]]
    query: list[str]

    def __init__(self, languages: list[str]):
        self._initialize_dictionaries(languages)

    def _initialize_dictionaries(self, languages: list[str]) -> None:
        dictionaries = {}
        for lang in languages:
            try:
                with open(f"resources/{lang}.txt", encoding="utf-8") as file:
                    data = file.read().splitlines()
                    dictionaries[lang] = data
            except FileNotFoundError:
                print(f"Can't find dictionary for language {lang}. Skipped.")
        self.dictionaries = dictionaries

    @staticmethod
    def _remove_special_chars(string: str) -> str:
        return "".join(x for x in string if x.isalnum())

    @staticmethod
    def remove_redundant_spaces(string: str) -> str:
        return " ".join(string.split())

    def _process_query(self, query: str) -> None:
        query = self.remove_redundant_spaces(query)
        query = query.replace("ł", "l")  # "ł" don't work in normalizer below
        query = unicodedata.normalize("NFD", query)
        query = query.encode("ascii", "ignore").decode("ascii")
        self.query = [
            self._remove_special_chars(word) for word in query.split()
        ]

    def _get_language_scores(
        self, dictionary: list[str], max_length: int
    ) -> tuple[float, float, float, float]:
        dict_length = len(dictionary)
        return (
            (
                sum(
                    [
                        (max_length - dictionary.index(word)) / max_length
                        for word in self.query
                        if word in dictionary
                    ]
                )
                / len(self.query)
            ),
            (
                sum(
                    [
                        (max_length - dictionary.index(word)) / max_length
                        for word in self.query
                        if word in dictionary
                    ]
                )
            ),
            (
                sum(
                    [
                        (dict_length - dictionary.index(word)) / dict_length
                        for word in self.query
                        if word in dictionary
                    ]
                )
                / len(self.query)
            ),
            (
                sum(
                    [
                        (dict_length - dictionary.index(word)) / dict_length
                        for word in self.query
                        if word in dictionary
                    ]
                )
            ),
        )

    def _calculate_scores(self) -> None:
        max_length = max(
            [len(self.dictionaries[lang]) for lang in self.dictionaries]
        )
        scores = {
            language: self._get_language_scores(
                self.dictionaries[language], max_length
            )
            for language in self.dictionaries
        }
        scores = dict(sorted(scores.items(), key=lambda x: -x[1][0]))
        self.scores = scores

    def detect_language(self, query: str) -> str:
        self._process_query(query)
        self._calculate_scores()
        return self.get_prediction()

    def print_scores(self) -> None:
        print(f"{'lang':^8}|{'s1':^6}|{'s2':^6}|{'s3':^6}|{'s4':^6}")
        print("------------------------------------")
        for lang, scores in self.scores.items():
            print(
                f"{lang + ':':8} {scores[0]:.4f} {scores[1]:.4f} "
                f"{scores[2]:.4f} {scores[3]:.4f}"
            )

    def get_prediction(self) -> str:
        return next(iter(self.scores))


if __name__ == "__main__":
    language_names = [
        "polish",
        "slovak",
        "french",
        "german",
        "english",
        "spanish",
    ]

    output_dict = {
        "polish": "P",
        "slovak": "S",
        "french": "F",
        "german": "N",
        "english": "A",
        "spanish": "H",
    }

    detector = LanguageDetector(language_names)

    if len(sys.argv) > 1:
        texts = sys.argv[1:]
    else:
        text = input("Type some text\n").strip()
        if not text:
            print("Text length must be greater than 0!")
            exit(-1)
        texts = [text]

    for text in texts:
        prediction = detector.detect_language(text)
        # print(output_dict[prediction])
        detector.print_scores()
