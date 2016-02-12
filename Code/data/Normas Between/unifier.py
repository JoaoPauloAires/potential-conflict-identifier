import os
import nltk

sent_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
files = [f for f in os.listdir('.') if f[-4:] == '.txt']
output = open('all_sentences.txt', 'w')

for f in files:
	sents = sent_tokenizer.tokenize(open(f, 'r').read())
	for sent in sents:
		output.write(sent + "\n")

output.close()