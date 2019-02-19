import pandas as pd

class DecisionTreeMain:
    def __init__(self, phishing_csv_path, legitimate_csv_path):
        self.phishing_csv_path = phishing_csv_path
        self.legitimate_csv_path = legitimate_csv_path

    def main(self):
        phishing_urls = pd.read_csv(self.phishing_csv_path)
        legitimate_urls = pd.read_csv(self.legitimate_csv_path)

        