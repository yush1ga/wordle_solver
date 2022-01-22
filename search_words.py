import itertools
from collections import Counter

import Levenshtein
from tqdm import tqdm

with open("5_characters_dictionary.txt") as f:
    dictionary = f.read().rstrip().split("\n")
print("num of words:", len(dictionary))

frequency = sorted([(v, k) for k, v in Counter("".join(dictionary)).items()])[::-1]
print("character frequency", frequency)
top = "".join(sorted([v for _, v in frequency[:15]]))
print(top)

min_dist = (1e9, 1e9)
min_combinations = []
for v in tqdm(itertools.combinations(dictionary, 3)):
    joined_part = "".join(sorted(v[0]) + sorted(v[1]) + +sorted(v[2]))
    joined_all = "".join(sorted("".join(v)))
    dist = (
        Levenshtein.distance(top, joined_all),
        Levenshtein.distance(top, joined_part),
    )
    if dist == min_dist:
        if dist == 0:
            print(v)
        min_combinations.append(v)
    elif dist < min_dist:
        print("update dist", dist)
        min_dist = dist
        print(v)
        min_combinations = [v]
print(min_dist, min_combinations)
