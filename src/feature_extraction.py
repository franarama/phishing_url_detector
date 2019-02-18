# File for performing feature extraction on given urls
from urllib.parse import urlparse
import urllib.request
from urllib.error import HTTPError
import pandas as pd
from bs4 import BeautifulSoup
import tldextract
from data_preprocessing.main import DataPreprocessing


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

    def get_subdomain(self, url):
        return tldextract.extract(url).subdomain

    # checks URL length, phishing urls typically have greater length
    def url_length(self, url):
        if len(url) < 54:
            return 0  # legitimate
        elif 54 <= len(url) <= 75:
            return 2  # suspicious
        else:
            return 1  # phishing

    def domain_length(self, url):
        domain_length = len(self.get_domain(url))
        if domain_length < 10:
            return 0
        elif 10 <= domain_length < 17:
            return 2
        else:
            return 1

    def subdomain_length(self, url):
        subdomain_length = len(self.get_subdomain(url))
        if subdomain_length < 10:
            return 0
        elif 10 <= subdomain_length < 17:
            return 2
        else:
            return 1

    def path_length(self, url):
        path_length = len(self.get_path(url))
        if path_length < 2:
            return 0
        elif 2 <= path_length < 15:
            return 2
        else:
            return 1

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

    def known_tld(self, url):
        suffix = self.get_suffix(url)
        if suffix in open('../input/known_tld.txt').read():
            return 1
        else:
            return 0

    def brand_name_count(self, count):
        return 1 if count > 1 else 0

    def similar_brand_count(self, count):
        return 0 if count < 1 else 0

    def brand_check(self, url):
        domain = self.get_domain(url)
        return 0 if domain in open('../input/brands.txt').read() else 1

    def random_word_count(self, count):
        if count <= 2:
            return 0
        elif count == 3:
            return 2
        else:
            return 1

    def keyword_count(self, count):
        return 0 if count < 2 else 1

    def similar_keyword_count(self, count):
        return 0 if count < 1 else 1

    def other_word_count(self, count):
        return 0 if count < 2 else 1

    def raw_word_count(self, count):
        return 0 if count < 4 else 1

    def random_domain(self, bool_rand):
        return 1 if bool_rand else 0


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
        subdomain = []
        path = []
        domain_length = []
        subdomain_length = []
        path_length = []
        url_length = []
        num_sub_domains = []
        alexa_rank = []
        known_tld = []
        brand_name_count = []
        similar_brand_count = []
        brand_check = []
        random_word_count = []
        random_domain_check = []
        keyword_count = []
        similar_keyword_count = []
        other_word_count = []
        raw_word_count = []

        # create feature extraction object
        fe = FeatureExtraction()
        dp = DataPreprocessing()

        for i in range(0, len(raw_data["urls"])):
            url = raw_data["urls"][i]
            protocol.append(fe.get_protocol(url))
            path.append(fe.get_path(url))
            domain.append(fe.get_domain(url))
            subdomain.append(fe.get_subdomain(url))
            url_length.append(fe.url_length(url))
            subdomain_length.append(fe.subdomain_length(url))
            path_length.append(fe.path_length(url))
            domain_length.append(fe.domain_length(url))
            num_sub_domains.append(fe.sub_domains(url))
            alexa_rank.append(fe.alexa_rank(url))
            known_tld.append(fe.known_tld(url))

            # from the data preprocessing module
            dp.main(url)
            brand_name_count.append(fe.brand_name_count(dp.brand_name_count))
            similar_brand_count.append(fe.similar_brand_count(len(dp.similar_brand_list)))
            similar_keyword_count.append(fe.similar_keyword_count(len(dp.similar_keyword_list)))
            brand_check.append(fe.brand_check(url))
            random_word_count.append(fe.random_word_count(dp.random_word_count))
            random_domain_check.append(fe.random_domain(dp.has_random_domain))
            keyword_count.append(fe.keyword_count(dp.keyword_count))
            other_word_count.append(fe.other_word_count(len(dp.found_word_list)))
            raw_word_count.append(fe.raw_word_count(dp.raw_word_count))

            print('Extracting features for ', i, ':', url)

        label = [1 if bool_phishing is True else 0 for i in range(0, len(raw_data["urls"]))]

        d = {'Protocol': pd.Series(protocol), 'Domain': pd.Series(domain), 'Path': pd.Series(path),
             'Subdomain': pd.Series(subdomain), 'URL Length': pd.Series(url_length),
             'Domain length': pd.Series(domain_length), 'Subdomain length': pd.Series(subdomain_length),
             'Path length': pd.Series(path_length), 'Num Subdomains': pd.Series(num_sub_domains),
             'Alexa Rank': pd.Series(alexa_rank), 'Known TLD': pd.Series(known_tld),
             'Brand count': pd.Series(brand_name_count), 'Similar brand count': pd.Series(similar_brand_count),
             'Similar keyword count': pd.Series(similar_keyword_count), 'Brand check': pd.Series(brand_check),
             'Random word count': pd.Series(random_word_count), 'Random domain': pd.Series(random_domain_check),
             'Keyword count': pd.Series(keyword_count), 'Other word count': pd.Series(other_word_count),
             'Raw word count': pd.Series(raw_word_count), 'Label': pd.Series(label)}

        data = pd.DataFrame(d)
        data.to_csv(output_file, index=False, encoding='UTF-8')



