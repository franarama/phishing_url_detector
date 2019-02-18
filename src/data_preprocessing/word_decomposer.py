import enchant


# returns a list of substrings for a given string
def get_all_substrings(str_to_check):
    length = len(str_to_check)
    return [str_to_check[i: j] for i in range(length) for j in range(i + 1, length + 1)]


class WordDecomposer:
    def __init__(self):
        self.dict = enchant.Dict('en_US')
        self.word_list = []

    # TODO: remove false positives
    def analyze(self, compound_word):
        word_no_digits = ''.join([i for i in compound_word if not i.isdigit()])
        if self.dict.check(word_no_digits):
            self.word_list.append(word_no_digits)
        else:
            substrings = get_all_substrings(word_no_digits)
            substrings_reduced = [s for s in substrings if len(s) > 3]
            substrings_reduced.sort(key=len)
            for sub_word in substrings_reduced:
                if self.dict.check(sub_word):
                    self.word_list.append(sub_word)
        return self.word_list
