import os
import json
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn import preprocessing
from sklearn.datasets import fetch_20newsgroups

categories = ['alt.atheism', 'soc.religion.christian', 'comp.graphics', 'sci.med']
twenty_train = fetch_20newsgroups(subset='train', categories=categories, shuffle=True, random_state=42)
print(twenty_train.target)

class Statement(object):
    ruling = ""
    statement = ""
    speaker = ""
    party = ""

    def __init__(self, ruling, statement, speaker, party):
        self.ruling = ruling
        self.statement = statement
        self.speaker = speaker
        self.party = party

data = os.path.join(os.path.dirname(__file__), "data", "statements.json")

with open(data, 'r') as json_file:
   statements = json.load(json_file)

statementList = []
justStatements = []
justClassifiers = []
for rawStatement in statements:
    html = BeautifulSoup(rawStatement["statement"], "lxml")
    htmlText = html.get_text()
    htmlText = htmlText.replace('"', '').rstrip("\n\r")
    statementList.append(Statement(rawStatement["ruling"]["ruling"], htmlText, rawStatement["speaker"]["first_name"] + " " + rawStatement["speaker"]["last_name"], rawStatement["speaker"]["party"]["party"]))
    justStatements.append(htmlText)
    justClassifiers.append(rawStatement["ruling"]["ruling"])

# Count Vectorizer
count_vect = CountVectorizer()
X_train_counts = count_vect.fit_transform(justStatements)

encoder = preprocessing.LabelEncoder()
Y_train = encoder.fit_transform(justClassifiers)

# Frequencies
tfidf_transformer = TfidfTransformer()
X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)

# naive bayes
clf = MultinomialNB().fit(X_train_tfidf, Y_train)

# a test
classifiers = ["Pants on Fire!", "False", "Mostly True", "True", "Half-True", "Mostly False"]

docs_new = ["We don’t discuss recusals but there is no reason to think that is the case", "Ginsburg was hospitalized after falling at her office at the court", "The earth is a globe"]
X_new_counts = count_vect.transform(docs_new)
X_new_tfidf = tfidf_transformer.transform(X_new_counts)

predicted = clf.predict(X_new_tfidf)

for doc, category in zip(docs_new, predicted):
    print('%r => %s' % (doc, category))


