import pandas as pd
import re
import regex
import signal
import time

class TimeoutError (RuntimeError):
    pass

def handler (signum, frame):
    raise Exception()
    # pass

signal.signal (signal.SIGALRM, handler)

# replacing the values of the attributes with placeholders

# de-lexicalized the values of the attributes which seem to take a value from an open set of values
# name, price range, customer rating, near

#  price range and customer rating is more challenging than the others because both attributes have more value variations in the meaning representations and the natural language texts than the other attributes do

# locate trainset and annotations
trainset = pd.read_csv("e2e-dataset/trainset.csv")
annotations = trainset.iloc[:,0]
texts = trainset.iloc[:,1]

# create empty dataframe
d = {}
ts = pd.DataFrame(data=trainset)

#types = ["name", "priceRange", "near", "customer rating"]
types = ["name", "eatType", "familyFriendly", "priceRange", "food", "near", "area", "customer rating"]

print(len(ts))


# #for all types
for x in types:
    # over the whole dataframe
    for i in range(3000,3010): #len(ts)
        signal.alarm(15)
        try:
            # store the mr value in between brackets (e.g. for type name: name["The Vaults"] => "The Vaults")
            name = re.search(x + '\[([^]]+)\]', ts.iloc[i,0])
            # familyFriendly is boolean, so we should create a matching string
            # customer rating is not always the whole string but just numbers, so first try to find it on numbers
            if name:
                name = name.group(1)
                if x == "familyFriendly":
                    name = "family friendly"
                elif x == "customer rating":
                    numbers = [int(s) for s in name.split() if s.isdigit()]
                    if numbers:
                        # remove double numbers
                        numbers = set(numbers)
                        numbers = [str(n) for n in numbers]
                        numbers = " ".join(numbers)
                        found_numbers = regex.search(r"(?i)(?:"+ numbers +")", ts.iloc[i, 1])
                        if found_numbers:
                            name = numbers

                found_name = regex.search(r"(?i)(?:"+ name +")", ts.iloc[i, 1])
                # replace that best match
                if found_name:
                    found_name = found_name.group(0)
                    ts.iloc[i,1] = re.sub(str(found_name), x + "_x", ts.iloc[i,1], flags=re.IGNORECASE, count=1)
                else:
                    # look for the best match in the ref (e.g. for priceRange: £20-25, £20-£25 is also fine)
                    # ?b: best match with error {e<=x}
                    # i?: ignore case
                    # \w+: include whole words (e.g. went wrong with match on "tart at", had to include "start at")
                    e = len(name) - len(name.split())
                    found_name = regex.search(r"(?b)(?i)(?:\w+" + name + "\w+){e<=" + str(e) + "}", ts.iloc[i, 1])
                    if found_name:
                        found_name = found_name.group(0)
                        ts.iloc[i, 1] = re.sub(str(found_name), x + "_x", ts.iloc[i, 1], flags=re.IGNORECASE, count=1)
                # replace the value in between brackets in the mr
                ts.iloc[i,0] = re.sub(str(name), x + "_x", ts.iloc[i,0], flags=re.IGNORECASE, count=1)
        except Exception:
            print("took too long", i)
            ts.iloc[i,1] = "XXX"
            continue
        # print(ts.iloc[[i]])

ts.to_csv(r'delexicalized/delex4.csv')