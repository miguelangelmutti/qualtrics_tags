import json
import pandas as pd

file = open('./Json/General 2023 v2.json')
data = json.load(file);

operations = []
for operation in data["operations"]:
        if operation["operation"] == "insert_topic":
            operations.append(operation["topic"])
        #print(operation["topic"])
df = pd.DataFrame(operations)
df.to_csv('topics.csv',sep=";")
