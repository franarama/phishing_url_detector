import re
from gib_detect_train import train
from gib_detect import check
from word_decomposer import WordDecomposer
from malicious_analysis import MaliciousnessAnalysis


def get_words(url):
    return re.findall(r'\w+\b', url)[1:]


class DataPreprocessing:
    def __init__(self, url):
        self.url = url
        self.brand_name_count = 0
        self.keyword_count = 0
        self.random_word_count = 0
        self.word_list = []
        self.similar_word_list = []
        self.found_word_list = []

    def main(self):
        # train the gibberish detector
        train()
        words = get_words(self.url)
        for word in words:
            if word.lower() in open('../input/brands.txt').read().lower():
                self.brand_name_count += 1
            elif word.lower() in open('../input/keywords.txt').read().lower():
                self.keyword_count += 1
            else:
                is_random = check(word)
                if is_random:
                    self.random_word_count += 1
                else:
                    if len(word) <= 7:
                        self.word_list.append(word)
                    else:
                        # create a word decomposer object
                        wd = WordDecomposer()
                        # add list from word decomposer to the word list to be analyzed
                        self.word_list.extend(wd.analyze(word))
                    # create malicious analysis object
                    ma = MaliciousnessAnalysis
                    self.found_word_list, self.similar_word_list = ma.analyze(word)
