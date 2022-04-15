import string
import sys
import os
import unicodedata
from typing import Dict


languages = {
    "english": {
        "a": 0.07760667871979869,
        "b": 0.01735991067835707,
        "c": 0.039820676600109954,
        "d": 0.041736331124851936,
        "e": 0.12305529893845535,
        "f": 0.014588445996112014,
        "g": 0.02705153564080911,
        "h": 0.023531945522866,
        "i": 0.08169869814838955,
        "j": 0.0028338084685532276,
        "k": 0.007974337030508783,
        "l": 0.05095754388152413,
        "m": 0.027742984907136097,
        "n": 0.07514693296909448,
        "o": 0.059526980690429096,
        "p": 0.02802636575399142,
        "q": 0.0022840496256539013,
        "r": 0.07345231550489965,
        "s": 0.07781071292953452,
        "t": 0.06898623335845977,
        "u": 0.03482183846158206,
        "v": 0.012820149511734802,
        "w": 0.009946667724621829,
        "x": 0.0033949025453267664,
        "y": 0.01552360279073458,
        "z": 0.0023010524764652206,
    },
    "french": {
        "a": 0.07342859622226722,
        "b": 0.012684041537705013,
        "c": 0.04204390963524341,
        "d": 0.027306123629631772,
        "e": 0.15809493506117844,
        "f": 0.014361748286135779,
        "g": 0.014491915189031269,
        "h": 0.009444331954528361,
        "i": 0.08779034450840299,
        "j": 0.0028636718637007896,
        "k": 0.0015041508779034451,
        "l": 0.04628156547395216,
        "m": 0.03006855456885829,
        "n": 0.07875097625177171,
        "o": 0.05992016429955743,
        "p": 0.030878481964652454,
        "q": 0.006812067918197333,
        "r": 0.07934395880940673,
        "s": 0.07619102716149374,
        "t": 0.07710219548176217,
        "u": 0.044849729542101764,
        "v": 0.015677880304301294,
        "w": 0.0009400942986896531,
        "x": 0.005278991061872668,
        "y": 0.00292152382054323,
        "z": 0.0009690202771108733,
    },
    "german": {
        "a": 0.06691102852585315,
        "b": 0.02346892022603472,
        "c": 0.033990055829897,
        "d": 0.02421558146243785,
        "e": 0.161363674930849,
        "f": 0.020804697177959918,
        "g": 0.038113662203668824,
        "h": 0.049126915440614975,
        "i": 0.06090379948751888,
        "j": 0.002816949210066351,
        "k": 0.020176822956439106,
        "l": 0.045783909450355514,
        "m": 0.02470769909552173,
        "n": 0.0919581190924672,
        "o": 0.03258158122486382,
        "p": 0.01282899760729013,
        "q": 0.00042423933886541433,
        "r": 0.07619338526022841,
        "s": 0.061955913047905105,
        "t": 0.07205280931290196,
        "u": 0.04040455463354206,
        "v": 0.009757504793904529,
        "w": 0.01311748035771861,
        "x": 0.0009672656926131446,
        "y": 0.004412089124200309,
        "z": 0.010962344516282306,
    },
    "polish": {
        "a": 0.10663722867750777,
        "b": 0.01499733454104571,
        "c": 0.04603931669898241,
        "d": 0.03239594095418713,
        "e": 0.08632784673375131,
        "f": 0.003920347594718146,
        "g": 0.013313141892051272,
        "h": 0.011067551693392021,
        "i": 0.07770874317713272,
        "j": 0.018771435715262935,
        "k": 0.032188365389605185,
        "l": 0.048148095730076286,
        "m": 0.03392445192974511,
        "n": 0.053285590953479484,
        "o": 0.0745290629378547,
        "p": 0.035094423293752446,
        "q": 0.0001085054087587453,
        "r": 0.05235150091286072,
        "s": 0.0509126248401904,
        "t": 0.032792221577479935,
        "u": 0.02643757872539168,
        "v": 0.0010331601964419662,
        "w": 0.03974128536450741,
        "x": 0.00033023385274400744,
        "y": 0.04082162182562709,
        "z": 0.0671223893834534,
    },
    "slovak": {
        "a": 0.10642280160241675,
        "b": 0.017748079070072895,
        "c": 0.03088264267419715,
        "d": 0.03909174492677481,
        "e": 0.09113745320811716,
        "f": 0.003070204242464044,
        "g": 0.003414986537072306,
        "h": 0.02400341498653707,
        "i": 0.0742595389768175,
        "j": 0.01594207657450581,
        "k": 0.032934918237341564,
        "l": 0.04997701451369278,
        "m": 0.03369015564457871,
        "n": 0.061617521507847904,
        "o": 0.08189400407171472,
        "p": 0.03557824916267157,
        "q": 3.2836409010310635e-05,
        "r": 0.052177053917383594,
        "s": 0.052275563144414526,
        "t": 0.05874433571944572,
        "u": 0.037417088067248964,
        "v": 0.03992907335653773,
        "w": 0.0012313653378866487,
        "x": 0.0006895645892165233,
        "y": 0.025185525710908256,
        "z": 0.030652787811124977,
    },
    "spanish": {
        "a": 0.12855548517479565,
        "b": 0.016559587367659036,
        "c": 0.04857780593008174,
        "d": 0.04313335143124303,
        "e": 0.12023044671673755,
        "f": 0.008113896178324738,
        "g": 0.016016650076916116,
        "h": 0.010376134889753566,
        "i": 0.07396012427231322,
        "j": 0.0063191868005911984,
        "k": 0.0021868307543812023,
        "l": 0.04070521521430941,
        "m": 0.03287786927276566,
        "n": 0.06883238319307454,
        "o": 0.08934334751002926,
        "p": 0.02646819292371731,
        "q": 0.003423521249962296,
        "r": 0.08415528006515248,
        "s": 0.07113986667873194,
        "t": 0.05236328537387265,
        "u": 0.030298917141736798,
        "v": 0.014176695924954002,
        "w": 0.0011612825385334661,
        "x": 0.0020510964316954724,
        "y": 0.005007088347962477,
        "z": 0.003966458540705215,
    },
}


class LanguageDetector:
    languages: Dict[str, Dict[str, float]]
    query: str

    def __init__(self, languages: Dict[str, Dict[str, float]]):
        self.languages = languages

    @staticmethod
    def _remove_special_chars(string: str) -> str:
        return "".join(x for x in string if x.isalnum())

    @staticmethod
    def remove_redundant_spaces(string: str) -> str:
        return " ".join(string.split())

    def _process_query(self, query: str) -> None:
        query = self.remove_redundant_spaces(query)
        query = query.replace("ł", "l")
        query = query.replace("ß", "ss")
        query = query.replace("Œ", "oe")
        query = unicodedata.normalize("NFD", query)
        query = query.encode("ascii", "ignore").decode("ascii").lower()
        self.query = "".join(
            [self._remove_special_chars(word) for word in query.split()]
        )

    def _get_language_score(self, dictionary: Dict[str, float]) -> float:
        statistics = {
            char: self.query.count(char) / len(self.query)
            for char in string.ascii_lowercase
        }

        MSE = sum(
            [
                (a - b) ** 2
                for a, b in zip(dictionary.values(), statistics.values())
            ]
        ) / len(dictionary.values())

        return MSE

    def _calculate_scores(self) -> None:
        scores = {
            language: self._get_language_score(self.languages[language])
            for language in self.languages
        }
        scores = dict(sorted(scores.items(), key=lambda x: x[1]))
        self.scores = scores

    def detect_language(self, query: str) -> str:
        self._process_query(query)
        self._calculate_scores()
        return self.get_prediction()

    def print_scores(self) -> None:
        print(f"{'lang':^8}|{'score':>6}")
        print("---------------")
        for lang, score in self.scores.items():
            print(f"{lang + ':':8} {score:.4f}")

    def get_prediction(self) -> str:
        return next(iter(self.scores))

    def run_tests(self) -> None:
        for filename in os.listdir("test"):
            with open(f"test/{filename}", encoding='utf-8') as file:
                data = file.read()
                prediction = self.detect_language(data)
                print(filename)
                print(prediction)
                self.print_scores()
                print()


if __name__ == "__main__":
    output_dict = {
        "polish": "P",
        "slovak": "S",
        "french": "F",
        "german": "N",
        "english": "A",
        "spanish": "H",
    }

    detector = LanguageDetector(languages)

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
        print(output_dict[prediction])
    #     detector.print_scores()
