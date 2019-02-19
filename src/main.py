from src.feature_extraction import FeMain
from src.random_forest import RandomForestMain
from src.decision_tree import DecisionTreeMain

import os

os.makedirs('../extracted_csv_files/', exist_ok=True)

# path constants
INPUT_PHISHING_PATH = '../raw_datasets/data_phishing_1000.txt'
INPUT_LEGITIMATE_PATH = '../raw_datasets/data_legitimate_1000.txt'
OUTPUT_PATH = '../extracted_csv_files/'

# comment out
# instantiate feature extraction main object
# fe = FeMain(INPUT_PHISHING_PATH, INPUT_LEGITIMATE_PATH, OUTPUT_PATH)

# comment out
# run feature extraction on raw phishing URLs data file
# fe.main(bool_phishing=True)
# run feature extraction on raw legitimate URLs data file
# fe.main(bool_phishing=False)

# '../extracted_csv_files/phishing-urls.csv', '../extracted_csv_files/legitimate-urls.csv'
# # run random forest on generated output files
# rf = RandomForestMain('../extracted_csv_files/phishing-urls.csv', '../extracted_csv_files/legitimate-urls.csv')
# dt = DecisionTreeMain('../extracted_csv_files/phishing-urls.csv', '../extracted_csv_files/legitimate-urls.csv')



# run random forest on generated output files
# instantiate feature extraction main object
fe = FeMain(INPUT_PHISHING_PATH, INPUT_LEGITIMATE_PATH, OUTPUT_PATH)

# run feature extraction on raw phishing URLs data file
fe.main(bool_phishing=True)
# run feature extraction on raw legitimate URLs data file
fe.main(bool_phishing=False)

# run random forest on generated output files
rf = RandomForestMain(fe.output_phishing_file.name, fe.output_legitimate_file.name)
dt = DecisionTreeMain(fe.output_phishing_file.name, fe.output_legitimate_file.name)
rf.main()
dt.main()
