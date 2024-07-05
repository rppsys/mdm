import gensim
from gensim import corpora
from gensim.models import LsiModel
from pprint import pprint

# Sample documents
documents = [
    "Human machine interface for lab abc computer applications",
    "A survey of user opinion of computer system response time",
    "The EPS user interface management system",
    "System and human system engineering testing of EPS",
    "Relation of user perceived response time to error measurement",
    "The generation of random binary unordered trees",
    "The intersection graph of paths in trees",
    "Graph minors IV Widths of trees and well quasi ordering",
    "Graph minors A survey",
]

# Tokenize the documents
texts = [[word for word in document.lower().split()] for document in documents]

# Create a dictionary representation of the documents
dictionary = corpora.Dictionary(texts)

# Create a corpus: List of bags of words
corpus = [dictionary.doc2bow(text) for text in texts]

# Number of topics
num_topics = 2

# Create the LSI model
lsi_model = LsiModel(corpus, num_topics=num_topics, id2word=dictionary)

# Print the topics
topics = lsi_model.print_topics(num_topics=num_topics)
pprint(topics)

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

