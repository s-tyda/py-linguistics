DICT_NAMES = {
    'angielski': 'english.txt',
    'francuski': 'french.txt',
    'niemiecki': 'german.txt',
    'polski': 'polish.txt',
    'slowacki': 'slovak.txt',
    'hiszpanski': 'spanish.txt'
}
if __name__ == '__main__':
    for lang in DICT_NAMES:
        print(lang)
        lang_dict_f = open(DICT_NAMES[lang], 'r')
        lang_dict = lang_dict_f.read().splitlines()
        lang_dict_f.close()

        sum_len = 0
        for word in lang_dict:
            sum_len += len(word)
        avg_len = sum_len/len(lang_dict)
        alfa_statistics = {}
        for c_n in range(ord('a'), ord('z') + 1):
            alfa_statistics[chr(c_n)] = 0

        merged_dict = ''.join(lang_dict)
        for c in merged_dict:
            alfa_statistics[c] += 1

        for key in alfa_statistics:
            alfa_statistics[key] /= len(merged_dict)

        chars = alfa_statistics.keys()
        vals = alfa_statistics.values()
        print({'wl':avg_len, 'as':alfa_statistics})
