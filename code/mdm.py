# Main.py - MDM
import os
import json
from pprint import pprint  # pretty-printer
from collections import defaultdict
from gensim import corpora
from gensim.corpora import Dictionary
import pandas as pd
from smart_open import open
import operator

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

def createDocs(filenameDocs,filenameData,filenameMeta,limite):
    if os.path.exists(filenameDocs):
        os.remove(filenameDocs)
    f = open(filenameDocs,'a+')
    ddMeta = {}
    for i,row in enumerate(read_csv(filenameData)):
        if i % (limite/10) == 0:
            print('Lendo documento #{}'.format(i))
        # Texto
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

        # Meta dados
        dMeta = {}
        dMeta['c0'] = str(row.iat[0, 0])
        dMeta['c1'] = str(row.iat[0, 1])
        dMeta['c2'] = str(row.iat[0, 2])
        dMeta['c3'] = str(row.iat[0, 3])
        dMeta['c4'] = str(row.iat[0, 4])
        dMeta['c6'] = str(row.iat[0, 6])
        ddMeta[i] = dMeta
        if i > limite:
            break
    f.close()
    print('Docs {} gerado!'.format(filenameDocs))

    # Metadados
    if os.path.exists(filenameMeta):
        os.remove(filenameMeta)
    with open(filenameMeta, 'w') as outfile:
        json.dump(ddMeta, outfile)
    print('Meta {} gerado!'.format(filenameMeta))

def loadMeta(filenameMeta):
    with open(filenameMeta) as json_file:
        ddMeta = json.load(json_file)
    return ddMeta

def createDictionary(filenameDocs,filenameDict):
    with open(filenameDocs) as f:
        documents = [line.strip().split() for line in f]
    dictionary = corpora.Dictionary(documents)
    stop_ids = [dictionary.token2id[stopword] for stopword in stopwords.words('portuguese') if stopword in dictionary.token2id]
    once_ids = [tokenid for tokenid, docfreq in dictionary.dfs.items() if docfreq == 1]
    dictionary.filter_tokens(stop_ids + once_ids)
    dictionary.compactify()
    dictionary.save(filenameDict)
    print('Dictionary {} gerado!'.format(filenameDict))

def loadDictionary(filenameDict):
    dictionary = Dictionary.load(filenameDict)
    return dictionary

def createCorpus(filenameDocs,filenameDict,filenameCorpus):
    with open(filenameDocs) as f:
        documents = [line.strip().split() for line in f]
    dictionary =  Dictionary.load(filenameDict)
    corpus = [dictionary.doc2bow(document) for document in documents]
    corpora.MmCorpus.serialize(filenameCorpus, corpus)
    print('Corpus {} gerado!'.format(filenameCorpus))

def loadCorpus(filenameCorpus):
    corpus = corpora.MmCorpus(filenameCorpus)
    return corpus

def createLSI(filenameCorpus,filenameDict,num_topics,filenameLSI):
    corpus = corpora.MmCorpus(filenameCorpus)
    dictionary = Dictionary.load(filenameDict)
    lsi_model = LsiModel(corpus, num_topics=num_topics, id2word=dictionary)
    lsi_model.save(filenameLSI)
    print('Modelo lsi {} gerado!'.format(filenameLSI))

def loadLSI(filenameLSI):
    lsi = LsiModel.load(filenameLSI)  # Load LSI model from disk
    return lsi

def createJsonTopics(filenameLSI,num_topics,filenameJsonTopics):
    lsi = LsiModel.load(filenameLSI)  # Load LSI model from disk
    topics = lsi.print_topics(num_topics=num_topics)
    with open(filenameJsonTopics, 'w') as outfile:
        json.dump(topics, outfile)
    print('Tópicos {} gerado!'.format(filenameJsonTopics))


def topicoDominante(filenameLSI,filenameCorpus,filenameMeta):
    # Carrega
    lsi = LsiModel.load(filenameLSI)
    corpus = corpora.MmCorpus(filenameCorpus)
    with open(filenameMeta) as json_file:
        ddMeta = json.load(json_file)

    corpus_lsi = lsi[corpus]
    for index, doc in enumerate(corpus_lsi):
        dominant_topic = max(doc, key=lambda x: x[1])
        ddMeta[str(index)]['dominante'] = str(dominant_topic[0])
        ddMeta[str(index)]['dominante_peso'] = str(dominant_topic[1])
    with open(filenameMeta, 'w') as outfile:
        json.dump(ddMeta, outfile)
    print('Meta {} atualizado!'.format(filenameMeta))

