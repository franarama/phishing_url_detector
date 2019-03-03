from feature_extraction import FeMain
from random_forest import RandomForestMain
from decision_tree import DecisionTreeMain
from logistic_reg import LogisticRegMain
from naive_bayes import NaiveBayesMain
from adaboost import AdaBoostMain
import os

os.makedirs('../extracted_csv_files/', exist_ok=True)

# path constants
INPUT_PHISHING_PATH = '../raw_datasets/data_phishing_37175.csv'
INPUT_LEGITIMATE_PATH = '../raw_datasets/data_legitimate_36400.csv'
OUTPUT_PATH = '../extracted_csv_files/'

# QUICK WAY

# # # run random forest on generated output files
# rf = RandomForestMain('../extracted_csv_files/phishing-urls.csv', '../extracted_csv_files/legitimate-urls.csv')
# dt = DecisionTreeMain('../extracted_csv_files/phishing-urls.csv', '../extracted_csv_files/legitimate-urls.csv')
# lr = LogisticRegMain('../extracted_csv_files/phishing-urls.csv', '../extracted_csv_files/legitimate-urls.csv')
# nb = NaiveBayesMain('../extracted_csv_files/phishing-urls.csv', '../extracted_csv_files/legitimate-urls.csv')
# ab = AdaBoostMain('../extracted_csv_files/phishing-urls.csv', '../extracted_csv_files/legitimate-urls.csv')

# LONG WAY
# run random forest on generated output files
# instantiate feature extraction main object
fe = FeMain(INPUT_PHISHING_PATH, INPUT_LEGITIMATE_PATH, OUTPUT_PATH)

# run feature extraction on raw phishing URLs data file
fe.main(bool_phishing=True)
# run feature extraction on raw legitimate URLs data file
fe.main(bool_phishing=False)

# run algorithms on generated output files
rf = RandomForestMain(fe.output_phishing_file.name, fe.output_legitimate_file.name)
dt = DecisionTreeMain(fe.output_phishing_file.name, fe.output_legitimate_file.name)
lr = LogisticRegMain(fe.output_phishing_file.name, fe.output_legitimate_file.name)
nb = NaiveBayesMain(fe.output_phishing_file.name, fe.output_legitimate_file.name)
ab = AdaBoostMain(fe.output_phishing_file.name, fe.output_legitimate_file.name)

rf.main()
dt.main()
lr.main()
nb.main()
ab.main()
