# Main.py - MDM

from pprint import pprint  # pretty-printer
from collections import defaultdict
from gensim import corpora
import pandas as pd
from smart_open import open

# Para remover stop words
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from bs4 import BeautifulSoup
import string

import os

nltk.download('stopwords')


# Gerando o Corpus
def read_csv(file_name):
    for chunk in pd.read_csv(file_name, chunksize=1,delimiter=';',header=None):
        yield chunk

os.remove('corpus.txt')
f = open('corpus.txt','a+')
for i,row in enumerate(read_csv('dados.csv')):
    html = row.iat[0, 5]
    soup = BeautifulSoup(html, "html.parser")
    text = soup.text.lower()
    out = text.translate(str.maketrans('', '', string.punctuation))
    text_tokens = word_tokenize(out)
    tokens_without_sw = [word for word in text_tokens if word.lower() not in stopwords.words('portuguese')]
    final = ' '.join(tokens_without_sw)
    f.write(final + '\n')


