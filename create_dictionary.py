import imp
import itertools
from collections import Counter
from pkgutil import ImpImporter

import nltk

nltk.download("brown")
nltk.download("words")

perm = set(
    ["".join(v) for v in itertools.permutations("abcdefghijklmnopqrstuvwxyz", 5)]
)

# small dictionary
with open("5_characters_dictionary.txt", "w") as f:
    words = [
        k
        for (_, k) in sorted(
            [(v, k) for k, v in Counter(nltk.corpus.brown.words()).items()]
        )[::-1][:60000]
        if len(k) == 5 and k in perm
    ]
    f.write("\n".join(words))


# large dictionary
with open("5_characters_dictionary_large.txt", "w") as f:
    words = [
        k
        for (_, k) in sorted(
            [
                (v, k)
                for k, v in Counter(
                    nltk.corpus.brown.words() + nltk.corpus.words.words()
                ).items()
            ]
        )[::-1]
        if len(k) == 5 and k in perm
    ]
    f.write("\n".join(words))
