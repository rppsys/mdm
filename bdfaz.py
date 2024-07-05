import bdmdm

strTmp = 'tmp'
strData = 'data'
strDir = 'dir'

filenameRaw = '{}/raw.csv'.format(strData)
filenameGood = '{}/good.csv'.format(strDir)
filenameDocs = '{}/docs.txt'.format(strDir)
filenameMeta = '{}/meta.json'.format(strDir)
filenameDict = '{}/dictionary.dict'.format(strDir)
filenameCorpus = '{}/corpus.mm'.format(strDir)
filenameLSI = '{}/lsi_model.model'.format(strDir)
filenameJsonTopics = '{}/topics.json'.format(strDir)
filenameSelect = '{}/select.json'.format(strDir)

# Parâmetros Externos
filenameRep = 'listRep.json'

mdm.createNovoCSV(filenameRaw,filenameGood)
mdm.createDocs(filenameDocs,filenameGood,filenameMeta,filenameRep,5000,booSaveIntermediate=False,strPre='')
mdm.createDictionary(filenameDocs,filenameDict)
mdm.createCorpus(filenameDocs,filenameDict,filenameCorpus)
mdm.createLSI(filenameCorpus,filenameDict,30,filenameLSI)
mdm.createJsonTopics(filenameLSI,30,filenameJsonTopics)
mdm.topicoDominante(filenameLSI,filenameCorpus,filenameMeta,filenameSelect)
