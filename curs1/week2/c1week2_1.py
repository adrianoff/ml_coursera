import re
from string import lower
import numpy as np
from scipy.spatial.distance import cosine

f = open('sentences.txt', 'r')

lines = []
for line in f:
    lines.append(lower(line))

split_array = []
for line in lines:
    words = re.split("[^a-z]", line)
    pure_words = []
    for word in words:
        if word != '':
            pure_words.append(word)

    split_array.append(pure_words)


all_words = []
for arr_item in split_array:
    for word in arr_item:
        if word not in all_words:
            all_words.append(word)

a = np.zeros([22, 254])

i = j = 0
for sentence in split_array:
    j = 0
    for word in all_words:
        a[i, j] = sentence.count(word)
        j += 1
    i += 1

print round(cosine(a[0], a[0]), 6)
for i in range(1, 21):
    print i, round(cosine(a[0], a[i]), 6)


pass