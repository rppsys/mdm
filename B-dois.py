import gensim
from gensim import corpora
from gensim.models import LsiModel
from pprint import pprint
import nltk
from nltk.corpus import stopwords

# Define your stop list
stoplist = stopwords.words('portuguese')

# Step 1: Read the Corpus
# Load the tokenized text data
with open('corpus.txt') as f:
    documents = [line.strip().split() for line in f]

# Step 2: Create the Dictionary
# Create the dictionary from the pre-tokenized documents
dictionary = corpora.Dictionary(documents)

# Step 3: Filter Stop Words and Rare Words
# List of stop word IDs
stop_ids = [dictionary.token2id[stopword] for stopword in stoplist if stopword in dictionary.token2id]

# List of word IDs that appear only once
once_ids = [tokenid for tokenid, docfreq in dictionary.dfs.items() if docfreq == 1]

# Filter out stop words and rare words
dictionary.filter_tokens(stop_ids + once_ids)

# Step 4: Compactify the Dictionary
# Remove gaps in the ID sequence after filtering
dictionary.compactify()

print(dictionary)

# Step 5: Create the Corpus
# Convert the documents to the bag-of-words format
corpus = [dictionary.doc2bow(document) for document in documents]

# Print the corpus
print(corpus)

# Number of topics
num_topics = 2

# Train the LSI model
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

