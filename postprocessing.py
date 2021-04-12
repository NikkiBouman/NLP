import pandas as pd
import re
import regex
import itertools

tp = pd.read_csv("post-processed/to-process.csv")
tp = tp.iloc[:,1]
# create empty dataframe
d = {}
tp = pd.DataFrame(data=tp)

types = ["name_x", "eattype_x", "familyfriendly_x", "pricerange_x", "food_x", "near_x", "area_x", "customer rating_x"]

def remove_all_dup(words):
    return " ".join(sorted(set(words), key=words.index))

def remove_dup_attributes(words):
    k = []
    for i in words:
        if (i not in types or i in types and (s.count(i) > 1 and (i not in k) or s.count(i) == 1)):
            k.append(i)
    return ' '.join(k)

def remove_dup_consec(words):
    res = [k for k, g in itertools.groupby(words)]
    return ' '.join(res)

for a in range(len(tp)):
    s = tp.iloc[a,0]
    words = str(s).split()
    tp.iloc[a,0] = remove_dup_attributes(words)
tp.to_csv(r'post-processed\post.csv')

