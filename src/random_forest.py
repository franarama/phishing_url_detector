import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix, accuracy_score

legitimate_urls = pd.read_csv("../extracted_csv_files/legitimate-urls.csv")
phishing_urls = pd.read_csv("../extracted_csv_files/phishing-urls.csv")

# have to merge the two files together
urls = legitimate_urls.append(phishing_urls)

# drop unnecessary columns
urls = urls.drop(urls.columns[[0, 3, 5]], axis=1)

# shuffling the rows in the dataset so that when splitting the train and test set are equally distributed
urls = urls.sample(frac=1).reset_index(drop=True)

urls_without_labels = urls.drop('label', axis=1)
labels = urls['label']

data_train, data_test, labels_train, labels_test = \
    train_test_split(urls_without_labels, labels, test_size=0.30, random_state=110)

random_forest_classifier = RandomForestClassifier()
random_forest_classifier.fit(data_train, labels_train)

prediction_label = random_forest_classifier.predict(data_test)
confusionMatrix = confusion_matrix(labels_test, prediction_label)

print(confusionMatrix)

accuracy = accuracy_score(labels_test, prediction_label)
print(accuracy)