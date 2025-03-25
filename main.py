import json
import os

for file in os.listdir("./data"):
    with open("./data/" + file) as f:
        json_file = json.load(f)
        print(json_file["data"])