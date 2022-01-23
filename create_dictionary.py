import itertools
from collections import Counter

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
    words = set(words)

    # combine dictionary extracted from "/usr/share/dict/words" in Mac
    with open("5_characters_dictionary_mac.txt") as f2:
        f.write(
            "\n"
            + "\n".join([w for w in f2.read().rstrip().rsplit("\n") if w not in words])
        )
