import os
import json
from bs4 import BeautifulSoup
from collections import Counter
import pandas

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

# its broken for now
def make_matrix(statements, vocab):
    matrix = []
    for statement in statements:
        # Count each word in the headline, and make a dictionary.
        counter = Counter(statement.statement)
        # Turn the dictionary into a matrix row using the vocab.
        row = [counter.get(w, 0) for w in vocab]
        matrix.append(row)
    df = pandas.DataFrame(matrix)
    df.columns = unique_words
    return df

data = os.path.join(os.path.dirname(__file__), "data", "statements.json")

with open(data, 'r') as json_file:
   statements = json.load(json_file)

statementList = []
for rawStatement in statements:
    html = BeautifulSoup(rawStatement["statement"], "lxml")
    htmlText = html.get_text()
    htmlText = htmlText.replace('"', '').rstrip("\n\r")
    statementList.append(Statement(rawStatement["ruling"]["ruling"], htmlText, rawStatement["speaker"]["first_name"] + " " + rawStatement["speaker"]["last_name"], rawStatement["speaker"]["party"]["party"]))

# see https://www.dataquest.io/blog/natural-language-processing-with-python/
unique_words = []
for statement in statementList:
    unique_words.append(set(statement.statement.split(" ")))

#print(make_matrix(statementList, unique_words))
