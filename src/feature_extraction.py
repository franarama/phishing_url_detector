# File for performing feature extraction on given urls
from urllib.parse import urlparse
import urllib.request
from urllib.error import HTTPError
import re
import pandas as pd
from bs4 import BeautifulSoup


class FeatureExtraction:

    def __init__(self):
        pass

    def getProtocol(self, url):
        return urlparse(url).scheme

    def getDomain(self, url):
        return urlparse(url).netloc

    def getPath(self, url):
        return urlparse(url).path

    # check if domain has IP, likely phishing if it does
    def havingIP(self, url):
        match = re.search(
            '(([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\/)|'  # IPv4
            '((0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\/)'  # IPv4 in hexadecimal
            '(?:[a-fA-F0-9]{1,4}:){7}[a-fA-F0-9]{1,4}', url)  # Ipv6
        if match:
            return 1  # phishing
        else:
            return 0  # legitimate

    # checks URL length, phishing urls typically have greater length
    def long_url(self, url):
        if len(url) < 54:
            return 0  # legitimate
        elif 54 <= len(url) <= 75:
            return 2  # suspicious
        else:
            return 1  # phishing

    # checks for @ symbol
    def have_at_symbol(self, url):
        if "@" in url:
            return 1  # phishing
        else:
            return 0  # legitimate

    # check if // after protocol - likely phishing
    def redirection(self, url):
        if "//" in urlparse(url).path:
            return 1  # phishing
        else:
            return 0  # legitimate

    # check if domain has '-' symbol, likely phishing
    def prefix_suffix_separation(self, url):
        """If the domain has '-' symbol then it is considered as phishing site"""
        if "-" in urlparse(url).netloc:
            return 1  # phishing
        else:
            return 0  # legitimate

    # check number of dots in URL, more than 3 likely phishing
    def sub_domains(self, url):
        if url.count(".") < 3:
            return 0  # legitimate
        elif url.count(".") == 3:
            return 2  # suspicious
        else:
            return 1  # phishing

    # check for tiny URL, likely phishing
    def shortening_service(self, url):
        match = re.search('bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co|tinyurl|tr\.im|is\.gd|cli\.gs|'
                          'yfrog\.com|migre\.me|ff\.im|tiny\.cc|url4\.eu|twit\.ac|su\.pr|twurl\.nl|snipurl\.com|'
                          'short\.to|BudURL\.com|ping\.fm|post\.ly|Just\.as|bkite\.com|snipr\.com|fic\.kr|loopt\.us|'
                          'doiop\.com|short\.ie|kl\.am|wp\.me|rubyurl\.com|om\.ly|to\.ly|bit\.do|t\.co|lnkd\.in|'
                          'db\.tt|qr\.ae|adf\.ly|goo\.gl|bitly\.com|cur\.lv|tinyurl\.com|ow\.ly|bit\.ly|ity\.im|'
                          'q\.gs|is\.gd|po\.st|bc\.vc|twitthis\.com|u\.to|j\.mp|buzurl\.com|cutt\.us|u\.bb|yourls\.org|'
                          'x\.co|prettylinkpro\.com|scrnch\.me|filoops\.info|vzturl\.com|qr\.net|1url\.com|tweez\.me|v\.gd|tr\.im|link\.zip\.net',
                          url)
        if match:
            return 1  # phishing
        else:
            return 0  # legitimate

    # check Alexa rank
    def web_traffic(self, url):
        try:
            rank = \
                BeautifulSoup(urllib.request.urlopen("http://data.alexa.com/data?cli=10&dat=s&url=" + url).read(), "xml").find(
                    "REACH")['RANK']
        except TypeError:
            return 1
        except HTTPError:
            return 2
        rank = int(rank)
        if rank < 100000:
            return 0
        else:
            return 2


class FeMain:
    @staticmethod
    def main(input_data_path, bool_phishing):

        raw_data = pd.read_csv(input_data_path, header=None, names=['urls'])

        # features
        protocol = []
        domain = []
        path = []
        having_ip = []
        len_url = []
        having_at_symbol = []
        redirection_symbol = []
        prefix_suffix_separation = []
        sub_domains = []
        tiny_url = []
        web_traffic = []

        # object creation
        fe = FeatureExtraction()

        for i in range(0, len(raw_data["urls"])):
            url = raw_data["urls"][i]
            protocol.append(fe.getProtocol(url))
            path.append(fe.getPath(url))
            domain.append(fe.getDomain(url))
            having_ip.append(fe.havingIP(url))
            len_url.append(fe.long_url(url))
            having_at_symbol.append(fe.have_at_symbol(url))
            redirection_symbol.append(fe.redirection(url))
            prefix_suffix_separation.append(fe.prefix_suffix_separation(url))
            sub_domains.append(fe.sub_domains(url))
            tiny_url.append(fe.shortening_service(url))
            web_traffic.append(fe.web_traffic(url))

        label = [1 if bool_phishing is True else 0 for i in range(0, len(raw_data["urls"]))]

        d = {'Protocol': pd.Series(protocol), 'Domain': pd.Series(domain), 'Path': pd.Series(path),
             'Having_IP': pd.Series(having_ip), 'URL_Length': pd.Series(len_url),
             'Having_@_symbol': pd.Series(having_at_symbol), 'Redirection_//_symbol': pd.Series(redirection_symbol),
             'Prefix_suffix_separation': pd.Series(prefix_suffix_separation), 'Sub_domains': pd.Series(sub_domains),
             'tiny_url': pd.Series(tiny_url), 'web_traffic': pd.Series(web_traffic), 'label': pd.Series(label)}
        data = pd.DataFrame(d)

        if bool_phishing is True:
            csv_name = 'phishing-urls'
        else:
            csv_name = 'legitimate-urls'

        data.to_csv("../extracted_csv_files/{}.csv".format(csv_name), index=False, encoding='UTF-8')



