import mdm

filenameRaw = 'raw.csv'
filenameGood = 'good.csv'
filenameDocs = 'docs.txt'
filenameMeta = 'meta.json'
filenameDict = 'dictionary.dict'
filenameCorpus = 'corpus.mm'
filenameLSI = 'lsi_model.model'
filenameJsonTopics = 'topics.json'
filenameSelect = 'select.json'

mdm.createNovoCSV(filenameRaw,filenameGood)
mdm.createDocs(filenameDocs,filenameGood,filenameMeta,1000)
mdm.createDictionary(filenameDocs,filenameDict)
mdm.createCorpus(filenameDocs,filenameDict,filenameCorpus)
mdm.createLSI(filenameCorpus,filenameDict,30,filenameLSI)
mdm.createJsonTopics(filenameLSI,30,filenameJsonTopics)
mdm.topicoDominante(filenameLSI,filenameCorpus,filenameMeta,filenameSelect)