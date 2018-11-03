import requests
import os
import json

# api
number = 1000
url = "http://www.politifact.com/api/statements/truth-o-meter/json?n=" + str(number)

fileName = os.path.join(os.path.dirname(__file__), "data", "statements.json")

r = requests.get(url)
statements = r.json()

with open(fileName, "w+") as f:
    json.dump(statements, f)
