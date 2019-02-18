# File for performing feature extraction on given urls
from urllib.parse import urlparse
import urllib.request
from urllib.error import HTTPError
import re
import pandas as pd
from bs4 import BeautifulSoup
import tldextract


class FeatureExtraction:
    def __init__(self):
        pass

    def get_protocol(self, url):
        return urlparse(url).scheme

    def get_domain(self, url):
        return urlparse(url).netloc

    def get_path(self, url):
        return urlparse(url).path

    def get_suffix(self, url):
        return tldextract.extract(url).suffix

    def get_words(self, url):
        return re.findall(r'\w+\b', url)[1:]

    # checks URL length, phishing urls typically have greater length
    def long_url(self, url):
        if len(url) < 54:
            return 0  # legitimate
        elif 54 <= len(url) <= 75:
            return 2  # suspicious
        else:
            return 1  # phishing

    # check number of subdomains in URL, more than 3 likely phishing
    def sub_domains(self, url):
        if self.get_domain(url).count(".") < 3:
            return 0  # legitimate
        elif url.count(".") == 3:
            return 2  # suspicious
        else:
            return 1  # phishing

    # check Alexa rank
    def alexa_rank(self, url):
        try:
            rank = \
                BeautifulSoup(urllib.request.urlopen("http://data.alexa.com/data?cli=10&dat=s&url=" + url).read(),
                              "xml").find("REACH")['RANK']
        except TypeError:
            return 1
        except HTTPError:
            return 2
        rank = int(rank)
        if rank < 100000:
            return 0
        else:
            return 2

    def random_chars(self, url):
        word_list = self.get_words(self.get_path(url))
        bad_count = 0
        for word in word_list:
            if word.isalnum() or not re.match("^[a-zA-Z0-9_]*$", word):
                bad_count += 1
        if bad_count > 1:
            return 1
        else:
            return 0

    def known_tld(self, url):
        suffix = self.get_suffix(url)
        if suffix in open('../input/known_tld.txt').read():
            return 1
        else:
            return 0


class FeMain:
    def __init__(self, input_phishing_path, input_legitimate_path, output_folder_path):
        self.input_phishing_path = input_phishing_path
        self.input_legitimate_path = input_legitimate_path
        self.output_folder_path = output_folder_path
        self.output_phishing_file = open("{path}{name}.csv".format(path=self.output_folder_path,
                                                                   name='phishing-urls'), 'w')
        self.output_legitimate_file = open("{path}{name}.csv".format(path=self.output_folder_path,
                                                                     name='legitimate-urls'), 'w')

    def main(self, bool_phishing):
        if bool_phishing:
            input_data_path = self.input_phishing_path
            output_file = self.output_phishing_file
        else:
            input_data_path = self.input_legitimate_path
            output_file = self.output_legitimate_file

        raw_data = pd.read_csv(input_data_path, header=None, names=['urls'])

        # features
        protocol = []
        domain = []
        path = []
        url_length = []
        sub_domains = []
        alexa_rank = []
        random_chars = []
        known_tld = []

        # create feature extraction object
        fe = FeatureExtraction()

        for i in range(0, len(raw_data["urls"])):
            url = raw_data["urls"][i]
            protocol.append(fe.get_protocol(url))
            path.append(fe.get_path(url))
            domain.append(fe.get_domain(url))
            url_length.append(fe.long_url(url))
            sub_domains.append(fe.sub_domains(url))
            alexa_rank.append(fe.alexa_rank(url))
            random_chars.append(fe.random_chars(url))
            known_tld.append(fe.known_tld(url))
            print('Extracting features for ', i, ':', url)

        label = [1 if bool_phishing is True else 0 for i in range(0, len(raw_data["urls"]))]

        d = {'Protocol': pd.Series(protocol), 'Domain': pd.Series(domain), 'Path': pd.Series(path),
             'URL Length': pd.Series(url_length), 'Num Subdomains': pd.Series(sub_domains),
             'Alexa Rank': pd.Series(alexa_rank), 'Random chars': pd.Series(random_chars),
             'Known TLD': pd.Series(known_tld), 'Label': pd.Series(label)}
        data = pd.DataFrame(d)

        data.to_csv(output_file, index=False, encoding='UTF-8')



