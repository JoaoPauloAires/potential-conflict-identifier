import os
import nltk
import threading
import hashlib
from dictionaryNorms import *
from multiprocessing.pool import ThreadPool

norm_sentences = open('norm_sentences.txt', 'w')
common_sentences = open('common_sentences.txt', 'w')
dictionary = dic()

def generate_data():
	directory = '/home/lsa/Dropbox/PUCRS/Dissertation/Corpus/xibinCorpus/noHTML/'
	listDir = os.listdir(directory)
	threadList = []
	sent_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')	

	for dir in listDir:
	    print dir
	    listFiles = os.listdir(directory+dir)
	    for file in listFiles:
	        print "\t " + file + " " + str(listFiles.index(file) + 1) + "/" + str(len(listFiles))
	        f = open(directory+dir+"/"+file, 'r').read().split()[1:-1]
	        f = ' '.join(f)
	        sents = sent_tokenizer.tokenize(f)
	        for s in sents:
	            t = threading.Thread(target = verify, args = (s,))
	            t.start()

def verify(sentence):
	sentence = cleanSent(sentence)
	key = hashlib.md5(sentence).digest()

	if dictionary.has_key(key):
		norm_sentences.write(sentence + "\n")
	else:
		common_sentences.write(sentence + "\n")

def cleanSent(sent):
    lSent = sent.split()

    for s in lSent:
        if '--' in s:
            lSent.pop(lSent.index(s))    
    if len(lSent) > 1:
        if lSent[1] in ['and', 'or', 'will', 'of', 'and/or']:
            return ' '.join(lSent)
        elif '(' in lSent[0] or '.' in lSent[0]:
            return ' '.join(lSent[1:])
    return ' '.join(lSent)

if __name__ == "__main__":
    generate_data()