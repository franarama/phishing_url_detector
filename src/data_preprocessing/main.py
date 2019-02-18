import re


def get_words(url):
    return re.findall(r'\w+\b', url)[1:]


class DataPreprocessing:
    def __init__(self, url):
        self.url = url
        self.brand_name_count = 0
        self.keyword_count = 0

    def main(self):
        word_list = get_words(self.url)
        for word in word_list:
            if word in open('../input/brands.txt').read():
                self.brand_name_count += 1
            elif word in open('../input/keywords.txt').read():
                self.keyword_count += 1
            else:
