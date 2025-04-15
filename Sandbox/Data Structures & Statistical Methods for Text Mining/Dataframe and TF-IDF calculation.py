### Libraries

import numpy as np
import pandas as pd

### Data

corpus = ("data science is one of the most important fields of science",
          "this is one of the best data science courses",
          "data scientists analyze data")

### Development

#1# text split & duplicates removal
words_set = set()

for doc in corpus:
    words = doc.split(" ")
    words_set = words_set.union(set(words))

print("The number of words in the corpus:", len(words_set))
print("The words in the corpus: \n", words_set)


#2# DataFrame creation & Term Frequency computation
n_docs = len(corpus)  # Number of documents in the corpus
n_words_set = len(words_set)    # Number of unique words in the corpus

df_tf = pd.DataFrame(np.zeros((n_docs, n_words_set)), columns=words_set)

for i in range(n_docs):
    words = corpus[i].split(" ")    # Words in the document
    for w in words:
        df_tf[w][i] += 1 / len(words)

print(df_tf)


#3# Inverse Document Frequency computation
print("IDF of: ")

idf = {}

for w in words_set:
    k = 0   # number of documents in the corpus containing this word

    for i in range(n_docs):
        if w in corpus[i].split():
            k += 1

    idf[w] = np.log10(n_docs / k)

    print(f"{w:>15}: {idf[w]:>10}")


#4# Wrapping up
df_tf_idf = df_tf.copy()

for w in words_set:
    for i in range(n_docs):
        df_tf_idf[w][i] = df_tf[w][i] * idf[w]

print(df_tf_idf)



##### Important to notice

## This is an outdated dataframe. The example works in a narrow, temporary sense
## because pandas tries to be forgiving - future versions of the library raise an error.
## Dataframes do not support columns as set.















