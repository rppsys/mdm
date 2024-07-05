from pprint import pprint  # pretty-printer
from collections import defaultdict
from gensim import corpora
from smart_open import open  # for transparently opening remote files
import nltk
from nltk.corpus import stopwords

class MyCorpus:
    def __iter__(self):
        for line in open('corpus.txt'):
            yield dictionary.doc2bow(line.lower().split())

stoplist = stopwords.words('portuguese')

dictionary = corpora.Dictionary(line.lower().split() for line in open('corpus.txt'))
stop_ids = [dictionary.token2id[stopword]  for stopword in stoplist if stopword in dictionary.token2id]
once_ids = [tokenid for tokenid, docfreq in dictionary.dfs.items() if docfreq == 1]
dictionary.filter_tokens(stop_ids + once_ids)  # remove stop words and words that appear only once
dictionary.compactify()  # remove gaps in id sequence after words that were removed
print(dictionary)

# Aqui eu tenho o dictionary
corpus = [dictionary.doc2bow(text) for text in open('corpus.txt')]
num_topics = 2

# Create the LSI model
lsi_model = LsiModel(corpus, num_topics=num_topics, id2word=dictionary)
topics = lsi_model.print_topics(num_topics=num_topics)
print(topics)

# Transform the corpus into the LSI topic space
corpus_lsi = lsi_model[corpus]

# Print the topic distribution for each document and identify the dominant topic
for doc_index, doc in enumerate(corpus_lsi):
    print(f"Document {doc_index}:")
    for topic_num, weight in doc:
        print(f"  Topic {topic_num}: {weight:.3f}")
    # Find the dominant topic for this document
    dominant_topic = max(doc, key=lambda x: abs(x[1]))
    print(f"  Dominant topic: {dominant_topic[0]} with weight {dominant_topic[1]:.3f}")

