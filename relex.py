import pandas as pd
import re

trainset = pd.read_csv("e2e-dataset/trainset.csv")
delex = pd.read_csv("delexicalized/delex.csv")
mr = trainset.iloc[:, 0]
ref = delex.iloc[:, 2]

types = ["name", "eatType", "familyFriendly", "priceRange", "food", "near", "area", "customer rating"]

for i in range(20):
    for x in types:
        name = re.search(x + '\[([^]]+)\]', mr[i])
        if name:
            name = name.group(1)
            if x == "familyFriendly":
                if name == "yes":
                    name = "family friendly"
                else:
                    name = "not family friendly"
            ref[i] = re.sub(str(x + "_x"), name, ref[i])
ref.to_csv(r'relexicalized\relex.csv')
