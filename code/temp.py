filenameData = 'dados.csv'
filenameDocs = 'docs.txt'
filenameMeta = 'meta.txt'
filenameDict = 'dictionary.dict'
filenameCorpus = 'corpus.mm'
filenameLSI = 'lsi_model.model'
filenameJsonTopics = 'topics.json'


createDocs(filenameDocs,filenameData,filenameMeta)
dictionary = returnDictionary(filenameDocs,filenameDict)
corpus = returnCorpus(filenameDocs,filenameDict,filenameCorpus)
lsiModel = createLSI(corpus,30,dictionary,filenameLSI)
saveJsonTopics(filenameLSI,30,filenameJsonTopics)
topicoDominante(lsiModel,corpus)
