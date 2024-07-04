# Main.py - MDM
import os
import json
from pprint import pprint  # pretty-printer
from collections import defaultdict
from gensim import corpora
from gensim.corpora import Dictionary
import pandas as pd
from smart_open import open

# Para remover stop words e fazer todo tipo de tratamento
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from bs4 import BeautifulSoup
import string
from unidecode import unidecode
nltk.download('stopwords')
nltk.download('punkt')

# Modelo
from gensim.models import LsiModel

# Gerando o Corpus
def read_csv(file_name):
    for chunk in pd.read_csv(file_name, chunksize=1,delimiter=';',header=None):
        yield chunk


def saveDoc(filename,content):
    with open(filename, "w") as f:
        f.write(content)
    print('{} gerado!'.format(filename))
    f.close()

def createDocs(filenameDocs,filenameData):
    os.remove(filenameDocs)
    f = open(filenameDocs,'a+')
    for i,row in enumerate(read_csv(filenameData)):
        print('Lendo documento #{}'.format(i))
        html = row.iat[0, 5]
        soup = BeautifulSoup(html, "html.parser")
        text_with_spaces = soup.get_text(separator=' ')
        text = text_with_spaces.lower()
        nopunct = text.translate(str.maketrans('', '', string.punctuation))
        out = unidecode(nopunct)
        text_tokens = word_tokenize(out)
        tokens_without_sw = [word for word in text_tokens if word.lower() not in stopwords.words('portuguese')]
        final = ' '.join(tokens_without_sw)
        f.write(final + '\n')
    print('Docs {} gerado!'.format(filenameDocs))


def returnDictionary(filenameDocs,filenameDict):
    with open(filenameDocs) as f:
        documents = [line.strip().split() for line in f]
    dictionary = corpora.Dictionary(documents)
    stop_ids = [dictionary.token2id[stopword] for stopword in stopwords.words('portuguese') if stopword in dictionary.token2id]
    once_ids = [tokenid for tokenid, docfreq in dictionary.dfs.items() if docfreq == 1]
    dictionary.filter_tokens(stop_ids + once_ids)
    dictionary.compactify()
    dictionary.save(filenameDict)
    print('Dictionary {} gerado!'.format(filenameDict))
    return dictionary


def returnCorpus(filenameDocs,filenameDict,filenameCorpus):
    with open(filenameDocs) as f:
        documents = [line.strip().split() for line in f]
    dictionary =  Dictionary.load(filenameDict)
    corpus = [dictionary.doc2bow(document) for document in documents]
    corpora.MmCorpus.serialize(filenameCorpus, corpus)
    print('Corpus {} gerado!'.format(filenameCorpus))
    return corpus

def createLSI(corpus,num_topics,dictionary,filenameLSI):
    lsi_model = LsiModel(corpus, num_topics=num_topics, id2word=dictionary)
    lsi_model.save(filenameLSI)
    print('Modelo lsi {} gerado!'.format(filenameLSI))
    return lsi_model

def saveJsonTopics(filenameLSI,num_topics,filenameTopics):
    lsi_model = LsiModel.load(filenameLSI)  # Load LSI model from disk
    topics = lsi_model.print_topics(num_topics=num_topics)
    with open(filenameTopics, 'w') as outfile:
        json.dump(topics, outfile)
    print('Tópicos {} gerado!'.format(filenameTopics))

filenameData = 'amostra.csv'
filenameDocs = 'docs.txt'
filenameDict = 'dictionary.dict'
filenameCorpus = 'corpus.mm'
filenameLSI = 'lsi_model.model'
filenameJsonTopics = 'topics.json'


createDocs(filenameDocs,filenameData)
dictionary = returnDictionary(filenameDocs,filenameDict)
corpus = returnCorpus(filenameDocs,filenameDict,filenameCorpus)
lsiModel = createLSI(corpus,30,dictionary,filenameLSI)

saveJsonTopics(filenameLSI,30,filenameJsonTopics)


